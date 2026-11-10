"""
ALPHANEXUS – Financial Q&A LCEL Chain
=====================================
LangChain prompt templates and execution pipelines for equity research synthesis.
"""

from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser

FINANCIAL_QA_PROMPT = PromptTemplate.from_template(
    """You are ALPHANEXUS, an evidence-grounded equity research assistant.

Context Documents:
{context}

Research Question: {question}

Provide an objective, fact-backed financial research answer adhering strictly to the facts above.
Use [Source N, Page P] inline bracket citations for every numerical assertion.
If facts are absent from the context, state clearly what could not be determined.
"""
)

