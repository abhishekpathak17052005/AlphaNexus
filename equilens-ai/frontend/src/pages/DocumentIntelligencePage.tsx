import React, { useState, useEffect, useRef } from 'react';
import {
  UploadCloud,
  FileText,
  FileSpreadsheet,
  CheckCircle2,
  Clock,
  AlertCircle,
  Trash2,
  Eye,
  RefreshCw,
  Plus,
  FileCode,
} from 'lucide-react';
import { Card, CardHeader, CardTitle, CardContent } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { Button } from '../components/ui/Button';
import { Modal } from '../components/ui/Modal';
import { api } from '../services/api';
import { DocumentItem, Company } from '../types';

export const DocumentIntelligencePage: React.FC = () => {
  const [documents, setDocuments] = useState<DocumentItem[]>([]);
  const [companies, setCompanies] = useState<Company[]>([]);
  const [selectedCompanyId, setSelectedCompanyId] = useState<string>('');
  const [docTitle, setDocTitle] = useState('');
  const [financialYear, setFinancialYear] = useState('FY24');
  const [documentType, setDocumentType] = useState('Annual Report');
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isUploading, setIsUploading] = useState(false);
  const [previewDoc, setPreviewDoc] = useState<DocumentItem | null>(null);
  const fileInputRef = useRef<HTMLInputElement>(null);

  const loadData = async () => {
    try {
      const [docs, comps] = await Promise.all([api.getDocuments(), api.getCompanies()]);
      setDocuments(docs);
      setCompanies(comps);
      if (comps.length > 0 && !selectedCompanyId) {
        setSelectedCompanyId(comps[0].id);
      }
    } catch (e) {
      console.error('Error loading documents:', e);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleFileDrop = (e: React.DragEvent) => {
    e.preventDefault();
    if (e.dataTransfer.files && e.dataTransfer.files[0]) {
      const file = e.dataTransfer.files[0];
      setSelectedFile(file);
      if (!docTitle) setDocTitle(file.name.replace(/\.[^/.]+$/, ''));
    }
  };

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      const file = e.target.files[0];
      setSelectedFile(file);
      if (!docTitle) setDocTitle(file.name.replace(/\.[^/.]+$/, ''));
    }
  };

  const handleUpload = async () => {
    if (!selectedFile || !selectedCompanyId || !docTitle.trim()) {
      alert('Please fill in title, select company, and choose a file.');
      return;
    }

    setIsUploading(true);
    const formData = new FormData();
    formData.append('company_id', selectedCompanyId);
    formData.append('title', docTitle.trim());
    formData.append('financial_year', financialYear);
    formData.append('document_type', documentType);
    formData.append('file', selectedFile);
    formData.append('auto_process', 'true');

    try {
      await api.uploadDocument(formData);
      setSelectedFile(null);
      setDocTitle('');
      if (fileInputRef.current) fileInputRef.current.value = '';
      await loadData();
    } catch (e: any) {
      alert(`Upload error: ${e.response?.data?.detail || e.message}`);
    } finally {
      setIsUploading(false);
    }
  };

  const handleReprocess = async (docId: string) => {
    try {
      await api.processDocument(docId);
      await loadData();
    } catch (e: any) {
      alert(`Processing error: ${e.message}`);
    }
  };

  const handleDelete = async (docId: string) => {
    if (!confirm('Are you sure you want to delete this document and its vector embeddings?')) return;
    try {
      await api.deleteDocument(docId);
      await loadData();
    } catch (e: any) {
      alert(`Delete error: ${e.message}`);
    }
  };

  const getStatusBadge = (status: string) => {
    switch (status) {
      case 'PROCESSED':
        return (
          <Badge variant="gain" size="xs">
            <CheckCircle2 className="w-3 h-3 mr-1" /> PROCESSED
          </Badge>
        );
      case 'PROCESSING':
        return (
          <Badge variant="brand" size="xs">
            <RefreshCw className="w-3 h-3 mr-1 animate-spin" /> PROCESSING
          </Badge>
        );
      case 'QUEUED':
      case 'UPLOADED':
        return (
          <Badge variant="neutral" size="xs">
            <Clock className="w-3 h-3 mr-1" /> QUEUED
          </Badge>
        );
      case 'FAILED':
        return (
          <Badge variant="loss" size="xs">
            <AlertCircle className="w-3 h-3 mr-1" /> FAILED
          </Badge>
        );
      default:
        return <Badge size="xs">{status}</Badge>;
    }
  };

  const totalPages = documents.reduce((sum, d) => sum + (d.total_pages || 0), 0);
  const totalChunks = documents.reduce((sum, d) => sum + (d.total_chunks || 0), 0);

  return (
    <div className="space-y-6">
      {/* Page Header */}
      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4 border-b border-slate-200 dark:border-slate-800 pb-4">
        <div>
          <h1 className="text-xl sm:text-2xl font-bold tracking-tight text-slate-900 dark:text-slate-100">
            Document Intelligence Engine
          </h1>
          <p className="text-xs sm:text-sm text-slate-500 dark:text-slate-400 mt-1">
            Ingest Annual Reports, Earnings Transcripts, and Financial Statements into pgvector
          </p>
        </div>
      </div>

      {/* Stats row */}
      <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 font-tabular">
        <Card className="p-4">
          <span className="text-xs text-slate-400 font-mono block">Total Filings Stored</span>
          <span className="text-2xl font-bold text-slate-900 dark:text-slate-100">{documents.length}</span>
        </Card>
        <Card className="p-4">
          <span className="text-xs text-slate-400 font-mono block">Pages Parsed</span>
          <span className="text-2xl font-bold text-cyan-500">{totalPages}</span>
        </Card>
        <Card className="p-4">
          <span className="text-xs text-slate-400 font-mono block">Vector Embeddings (384-d)</span>
          <span className="text-2xl font-bold text-emerald-500">{totalChunks}</span>
        </Card>
      </div>

      {/* Upload Zone */}
      <Card className="p-6">
        <CardTitle className="mb-4">Upload New Financial Document</CardTitle>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
          {/* Company Picker */}
          <div>
            <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
              Select Company *
            </label>
            <select
              value={selectedCompanyId}
              onChange={(e) => setSelectedCompanyId(e.target.value)}
              className="w-full rounded-md bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-xs px-3 py-2 text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/30"
            >
              {companies.map((c) => (
                <option key={c.id} value={c.id}>
                  {c.symbol} - {c.name}
                </option>
              ))}
            </select>
          </div>

          {/* Financial Year */}
          <div>
            <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
              Financial Year
            </label>
            <select
              value={financialYear}
              onChange={(e) => setFinancialYear(e.target.value)}
              className="w-full rounded-md bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-xs px-3 py-2 text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/30 font-mono"
            >
              <option value="FY25">FY25</option>
              <option value="FY24">FY24</option>
              <option value="FY23">FY23</option>
              <option value="FY22">FY22</option>
              <option value="FY21">FY21</option>
            </select>
          </div>

          {/* Doc Type */}
          <div>
            <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
              Document Classification
            </label>
            <select
              value={documentType}
              onChange={(e) => setDocumentType(e.target.value)}
              className="w-full rounded-md bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-xs px-3 py-2 text-slate-800 dark:text-slate-200 focus:outline-none focus:ring-2 focus:ring-brand-500/30"
            >
              <option value="Annual Report">Annual Report</option>
              <option value="Quarterly Results">Quarterly Results / Earnings</option>
              <option value="Earnings Call Transcript">Earnings Call Transcript</option>
              <option value="Investor Presentation">Investor Presentation</option>
              <option value="Credit Rating Note">Credit Rating Note</option>
              <option value="Board Meeting Disclosure">Board Meeting Disclosure</option>
            </select>
          </div>
        </div>

        {/* Document Title */}
        <div className="mb-4">
          <label className="block text-xs font-medium text-slate-700 dark:text-slate-300 mb-1">
            Document Title *
          </label>
          <input
            value={docTitle}
            onChange={(e) => setDocTitle(e.target.value)}
            placeholder="e.g., Reliance Industries Integrated Annual Report FY24"
            className="w-full rounded-md bg-white dark:bg-slate-900 border border-slate-300 dark:border-slate-800 text-xs sm:text-sm px-3 py-2 text-slate-900 dark:text-slate-100 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-brand-500/30"
          />
        </div>

        {/* Drag and Drop Zone */}
        <div
          onDragOver={(e) => e.preventDefault()}
          onDrop={handleFileDrop}
          onClick={() => fileInputRef.current?.click()}
          className="border-2 border-dashed border-slate-300 dark:border-slate-800 hover:border-cyan-500 rounded-xl p-8 text-center cursor-pointer transition-colors bg-slate-50/50 dark:bg-slate-900/30"
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".pdf,.docx,.doc,.xlsx,.xls,.csv"
            onChange={handleFileSelect}
            className="hidden"
          />
          <UploadCloud className="w-10 h-10 text-cyan-500 mx-auto mb-2 opacity-80" />
          {selectedFile ? (
            <div className="text-xs">
              <span className="font-semibold text-slate-900 dark:text-slate-100 block">{selectedFile.name}</span>
              <span className="text-slate-400 font-mono">
                {(selectedFile.size / (1024 * 1024)).toFixed(2)} MB • Ready to Upload & Ingest
              </span>
            </div>
          ) : (
            <div>
              <p className="text-xs sm:text-sm font-semibold text-slate-800 dark:text-slate-200">
                Click to browse or drag and drop financial filings
              </p>
              <p className="text-[11px] text-slate-400 mt-1">
                Supports PDF (text & financial tables), DOCX, XLSX, and CSV (Up to 100MB)
              </p>
            </div>
          )}
        </div>

        <div className="mt-4 flex justify-end">
          <Button
            variant="primary"
            onClick={handleUpload}
            isLoading={isUploading}
            disabled={!selectedFile || isUploading}
          >
            Upload & Vectorize Filing
          </Button>
        </div>
      </Card>

      {/* Uploaded Documents Table */}
      <Card>
        <CardHeader className="flex flex-row items-center justify-between">
          <CardTitle>Ingested Filings & Vector Status</CardTitle>
          <Button variant="ghost" size="xs" onClick={loadData}>
            <RefreshCw className="w-3.5 h-3.5 mr-1" /> Refresh
          </Button>
        </CardHeader>
        <CardContent className="p-0 overflow-x-auto">
          <table className="w-full text-left text-xs font-tabular">
            <thead className="bg-slate-50 dark:bg-slate-900 text-slate-500 border-b border-slate-200 dark:border-slate-800 font-mono">
              <tr>
                <th className="p-3">Title / Filename</th>
                <th className="p-3">FY</th>
                <th className="p-3">Category</th>
                <th className="p-3">Status</th>
                <th className="p-3 text-right">Pages</th>
                <th className="p-3 text-right">Vectors</th>
                <th className="p-3 text-right">Actions</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-100 dark:divide-slate-800">
              {documents.map((doc) => (
                <tr key={doc.id} className="hover:bg-slate-50/80 dark:hover:bg-slate-850/50">
                  <td className="p-3">
                    <div className="font-semibold text-slate-900 dark:text-slate-100 font-sans">{doc.title}</div>
                    <div className="text-[10px] text-slate-400 font-mono truncate max-w-xs">{doc.filename}</div>
                  </td>
                  <td className="p-3 font-mono text-cyan-500 font-semibold">{doc.financial_year || 'FY24'}</td>
                  <td className="p-3 text-slate-600 dark:text-slate-300 font-sans">{doc.document_type}</td>
                  <td className="p-3">{getStatusBadge(doc.status)}</td>
                  <td className="p-3 text-right text-slate-700 dark:text-slate-300">{doc.total_pages}</td>
                  <td className="p-3 text-right text-emerald-500 font-semibold">{doc.total_chunks}</td>
                  <td className="p-3 text-right space-x-2">
                    <button
                      onClick={() => setPreviewDoc(doc)}
                      className="p-1 text-slate-400 hover:text-cyan-500"
                      title="Preview metadata"
                    >
                      <Eye className="w-4 h-4 inline" />
                    </button>
                    <button
                      onClick={() => handleReprocess(doc.id)}
                      className="p-1 text-slate-400 hover:text-amber-500"
                      title="Reprocess chunks & embeddings"
                    >
                      <RefreshCw className="w-4 h-4 inline" />
                    </button>
                    <button
                      onClick={() => handleDelete(doc.id)}
                      className="p-1 text-slate-400 hover:text-rose-500"
                      title="Delete filing"
                    >
                      <Trash2 className="w-4 h-4 inline" />
                    </button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </CardContent>
      </Card>

      {/* Preview Modal */}
      <Modal
        isOpen={!!previewDoc}
        onClose={() => setPreviewDoc(null)}
        title={previewDoc?.title || 'Filing Details'}
      >
        {previewDoc && (
          <div className="space-y-4 text-xs font-mono">
            <div className="p-3 rounded-lg bg-slate-100 dark:bg-slate-900 space-y-1.5">
              <div><span className="text-slate-400">Document ID:</span> {previewDoc.id}</div>
              <div><span className="text-slate-400">Filename:</span> {previewDoc.filename}</div>
              <div><span className="text-slate-400">Type:</span> {previewDoc.document_type}</div>
              <div><span className="text-slate-400">Financial Year:</span> {previewDoc.financial_year}</div>
              <div><span className="text-slate-400">Status:</span> {previewDoc.status}</div>
              <div><span className="text-slate-400">Pages:</span> {previewDoc.total_pages}</div>
              <div><span className="text-slate-400">Indexed Chunks:</span> {previewDoc.total_chunks}</div>
            </div>
            <p className="text-slate-500 font-sans text-xs">
              This filing is indexed with 384-dimensional dense vector embeddings using SentenceTransformers (BAAI/bge-small-en-v1.5) for semantic query retrieval.
            </p>
          </div>
        )}
      </Modal>
    </div>
  );
};

