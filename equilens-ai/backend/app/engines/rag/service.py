import os
import uuid
from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session
from app.models.document import Document, DocumentChunk
from app.models.company import Company
from app.models.research import ResearchSession, ResearchMessage, Citation
from app.engines.rag.loaders.pdf_loader import PDFDocumentLoader
from app.engines.rag.loaders.docx_loader import DOCXDocumentLoader
from app.engines.rag.loaders.tabular_loader import TabularDocumentLoader
from app.engines.rag.preprocessor import DocumentPreprocessor
from app.engines.rag.chunker import DocumentChunker
from app.engines.rag.embeddings import embedding_engine
from app.engines.rag.vector_store import vector_store
from app.engines.rag.citations import CitationEngine
from app.engines.providers.gemini import GeminiProvider
from app.engines.providers.groq import GroqProvider
from app.core.config import settings
from app.core.logging import logger


class RAGService:
    """
    Core RAG Engine orchestrator for EquiLens AI.
    Handles end-to-end document ingestion, section-aware chunking,
    dense vector embedding generation, pgvector storage,
    semantic search, and citation-backed synthesis.
    """

    def __init__(self):
        self.pdf_loader = PDFDocumentLoader()
        self.docx_loader = DOCXDocumentLoader()
        self.tabular_loader = TabularDocumentLoader()
        self.preprocessor = DocumentPreprocessor()
        self.chunker = DocumentChunker(chunk_size=900, chunk_overlap=120)
        self.gemini_provider = GeminiProvider()
        self.groq_provider = GroqProvider()

    def ingest_document(
        self,
        db: Session,
        document_id: str,
        file_path_or_bytes: Any,
        filename: str,
        mime_type: str,
    ) -> Dict[str, Any]:
        doc_uuid = uuid.UUID(document_id) if isinstance(document_id, str) else document_id
        doc = db.query(Document).filter(Document.id == doc_uuid).first()
        if not doc:
            raise ValueError(f"Document {document_id} not found")

        doc.status = "PROCESSING"
        db.commit()

        try:
            # 1. Select appropriate loader based on filename / mime_type
            ext = os.path.splitext(filename)[1].lower()
            if ext == ".pdf" or "pdf" in mime_type:
                pages_data = self.pdf_loader.load(file_path_or_bytes)
            elif ext in [".docx", ".doc"]:
                pages_data = self.docx_loader.load(file_path_or_bytes)
            elif ext == ".csv":
                pages_data = self.tabular_loader.load_csv(file_path_or_bytes)
            elif ext in [".xlsx", ".xls"]:
                pages_data = self.tabular_loader.load_excel(file_path_or_bytes)
            else:
                if isinstance(file_path_or_bytes, bytes):
                    text_content = file_path_or_bytes.decode("utf-8", errors="ignore")
                else:
                    with open(file_path_or_bytes, "r", encoding="utf-8", errors="ignore") as f:
                        text_content = f.read()
                pages_data = [{"page_number": 1, "text": text_content, "tables": []}]

            # 2. Extract metadata & company info
            company = db.query(Company).filter(Company.id == doc.company_id).first()
            company_symbol = company.symbol if company else "STOCK"

            # 3. Create chunks preserving tables and headings
            chunks = self.chunker.chunk_document(
                pages_data=pages_data,
                company_id=str(doc.company_id),
                document_id=str(doc.id),
                company_symbol=company_symbol,
                financial_year=doc.financial_year or "FY24",
                document_type=doc.document_type or "Filing",
            )

            # 4. Generate embeddings (BAAI/bge-small-en-v1.5)
            contents_to_embed = [c["content"] for c in chunks]
            embeddings = embedding_engine.get_embeddings_batch(contents_to_embed)

            for chunk_data, emb in zip(chunks, embeddings):
                chunk_data["embedding"] = emb

            # 5. Persist chunks in vector database
            vector_store.delete_document_chunks(db, str(doc.id))
            inserted_count = vector_store.store_chunks(db, chunks)

            # 6. Update document status
            doc.status = "PROCESSED"
            doc.total_pages = len(pages_data)
            doc.total_chunks = inserted_count
            doc.error_message = None
            db.commit()

            return {
                "document_id": str(doc.id),
                "status": "PROCESSED",
                "pages_extracted": len(pages_data),
                "chunks_stored": inserted_count,
            }

        except Exception as e:
            logger.error(f"Ingestion failed for document {document_id}: {e}")
            doc.status = "FAILED"
            doc.error_message = str(e)
            db.commit()
            raise e

    def research_chat(
        self,
        db: Session,
        session_id: str,
        user_query: str,
        company_id: Optional[str] = None,
        financial_year: Optional[str] = None,
        document_type: Optional[str] = None,
        top_k: int = 5,
    ) -> Dict[str, Any]:
        sess_uuid = uuid.UUID(session_id) if isinstance(session_id, str) else session_id
        comp_uuid = uuid.UUID(company_id) if isinstance(company_id, str) and company_id else None

        # Save user message
        user_msg = ResearchMessage(
            session_id=sess_uuid,
            role="user",
            content=user_query,
            message_type="user_query",
        )
        db.add(user_msg)
        db.commit()

        # Step 1: Query embedding
        q_vec = embedding_engine.get_embedding(user_query)

        # Step 2: Semantic retrieval
        retrieved_chunks = vector_store.search_similar(
            db=db,
            query_embedding=q_vec,
            company_id=comp_uuid,
            financial_year=financial_year,
            document_type=document_type,
            top_k=top_k,
        )

        # Step 3: Context preparation
        context_text = CitationEngine.format_context_for_prompt(retrieved_chunks)

        system_instruction = (
            "You are EquiLens AI, a senior equity research analyst. "
            "Your objective is to provide objective, evidence-grounded financial intelligence. "
            "Strictly follow these research principles:\n"
            "1. Ground all quantitative claims in the provided source excerpts.\n"
            "2. When citing facts, reference the source brackets like [Source 1], [Source 2] with exact page and section numbers.\n"
            "3. Clearly distinguish: (a) Document Facts, (b) Calculated Metrics, and (c) Strategic Interpretations.\n"
            "4. Do not invent financial values or disclose speculation as confirmed fact.\n"
            "5. If information is not contained in the provided excerpts, explicitly declare that the filed documents do not specify it."
        )

        prompt = (
            f"Context Documents:\n{context_text}\n\n"
            f"Research Question: {user_query}\n\n"
            "Provide a thorough, structured equity research answer with inline citations."
        )

        # Step 4: LLM Generation
        llm_response = None
        if hasattr(self.gemini_provider, "api_key") and self.gemini_provider.api_key:
            resp = self.gemini_provider.generate(prompt=prompt, system_prompt=system_instruction)
            if not resp.error:
                llm_response = resp

        if not llm_response and hasattr(self.groq_provider, "api_key") and self.groq_provider.api_key:
            resp = self.groq_provider.generate(prompt=prompt, system_prompt=system_instruction)
            if not resp.error:
                llm_response = resp

        if not llm_response or not llm_response.content:
            # Evidence synthesis fallback when live LLM keys are absent
            if retrieved_chunks:
                synthesized_lines = [
                    f"### Evidence-Grounded Research Synthesis for: *{user_query}*\n",
                    "> **[Grounded Fact]** Based on official company filings and disclosures:\n",
                ]
                for idx, c in enumerate(retrieved_chunks[:3]):
                    clean_excerpt = c.get("clean_text", "")[:300].strip()
                    synthesized_lines.append(
                        f"- **[Source {idx + 1}]** *({c.get('document_title', 'Filing')} – Page {c.get('page_number', 'N/A')}, {c.get('section', 'General')})*:\n"
                        f"  \"{clean_excerpt}...\"\n"
                    )
                synthesized_lines.append(
                    "\n> **[Analytical Interpretation]**\n"
                    "The filing exhibits consistent operational disclosure. Verify revenue segments and margin line items against the quarterly footnotes."
                )
                final_content = "\n".join(synthesized_lines)
                msg_type = "fact_grounded"
                tokens = len(final_content.split())
            else:
                final_content = (
                    "No relevant passages were found in the uploaded company documents matching your query. "
                    "Please upload the corresponding Annual Report or Earnings Transcript in Document Intelligence."
                )
                msg_type = "synthesis"
                tokens = 25
        else:
            final_content = llm_response.content
            msg_type = "fact_grounded"
            tokens = llm_response.tokens_used

        # Step 5: Save assistant message
        asst_msg = ResearchMessage(
            session_id=sess_uuid,
            role="assistant",
            content=final_content,
            message_type=msg_type,
            token_count=tokens,
        )
        db.add(asst_msg)
        db.commit()

        # Step 6: Save and attach citations
        citations_data = CitationEngine.build_citations_from_retrieval(retrieved_chunks, asst_msg.id)
        saved_citations = []
        for cit in citations_data:
            doc_id_val = uuid.UUID(cit["document_id"]) if isinstance(cit["document_id"], str) else cit["document_id"]
            chunk_id_val = uuid.UUID(cit["document_chunk_id"]) if cit.get("document_chunk_id") and isinstance(cit["document_chunk_id"], str) else cit.get("document_chunk_id")

            citation_obj = Citation(
                message_id=asst_msg.id,
                document_id=doc_id_val,
                document_chunk_id=chunk_id_val,
                chunk_index=cit.get("chunk_index"),
                page_number=cit.get("page_number"),
                section=cit.get("section"),
                excerpt=cit["excerpt"],
                source_url=cit.get("source_url"),
                confidence_score=cit.get("confidence_score", 0.95),
            )
            db.add(citation_obj)
            cit["id"] = str(citation_obj.id)
            saved_citations.append(cit)
        db.commit()

        return {
            "message_id": str(asst_msg.id),
            "role": "assistant",
            "content": final_content,
            "message_type": msg_type,
            "tokens_used": tokens,
            "citations": saved_citations,
            "retrieved_count": len(retrieved_chunks),
        }


rag_service = RAGService()
