import React, { useState, useEffect, useRef } from 'react';
import { motion, AnimatePresence } from 'motion/react';
import {
  Upload, FileText, Trash2, RefreshCw, CheckCircle2,
  XCircle, Loader2, CloudUpload, Building2, AlertCircle,
} from 'lucide-react';
import { ANButton } from '../components/shared/ANButton';
import { api } from '../services/api';
import type { Company, DocumentItem } from '../types';

const DOC_TYPES = [
  'Annual Report', 'Quarterly Result', 'Investor Presentation',
  'Earnings Call Transcript', 'Corporate Announcement', 'Financial Statement',
  'Research Report', 'Other',
];

const FY_OPTIONS = ['FY25', 'FY24', 'FY23', 'FY22', 'FY21', 'FY20'];

const StatusBadge: React.FC<{ status: DocumentItem['status'] }> = ({ status }) => {
  const map: Record<DocumentItem['status'], { label: string; color: string; icon: React.ReactNode }> = {
    UPLOADED:   { label: 'Uploaded',   color: 'badge-muted',  icon: <FileText className="w-3 h-3" /> },
    QUEUED:     { label: 'Queued',     color: 'badge-brand',  icon: <Loader2  className="w-3 h-3 animate-spin" /> },
    PROCESSING: { label: 'Processing', color: 'badge-brand',  icon: <Loader2  className="w-3 h-3 animate-spin" /> },
    PROCESSED:  { label: 'Indexed',    color: 'badge-lime',   icon: <CheckCircle2 className="w-3 h-3" /> },
    FAILED:     { label: 'Failed',     color: 'badge-neg',    icon: <XCircle  className="w-3 h-3" /> },
  };
  const { label, color, icon } = map[status] ?? map.UPLOADED;
  return <span className={`badge ${color} gap-1`}>{icon}{label}</span>;
};

export const DocumentIntelligencePage: React.FC = () => {
  const [documents,  setDocuments]  = useState<DocumentItem[]>([]);
  const [companies,  setCompanies]  = useState<Company[]>([]);
  const [loading,    setLoading]    = useState(true);
  const [uploading,  setUploading]  = useState(false);
  const [dragOver,   setDragOver]   = useState(false);
  const [companyId,  setCompanyId]  = useState('');
  const [docType,    setDocType]    = useState(DOC_TYPES[0]);
  const [fy,         setFy]         = useState(FY_OPTIONS[0]);
  const [title,      setTitle]      = useState('');
  const [uploadMsg,  setUploadMsg]  = useState('');
  const fileRef = useRef<HTMLInputElement>(null);

  const load = async () => {
    setLoading(true);
    try {
      const [docs, comps] = await Promise.all([api.getDocuments(), api.getCompanies()]);
      setDocuments(docs);
      setCompanies(comps);
      if (!companyId && comps.length) setCompanyId(comps[0].id);
    } finally { setLoading(false); }
  };

  useEffect(() => { load(); }, []);

  const handleFile = async (file: File) => {
    if (!companyId || !title.trim()) {
      setUploadMsg('Please select a company and enter a document title.');
      return;
    }
    setUploading(true); setUploadMsg('');
    const formData = new FormData();
    formData.append('company_id', companyId);
    formData.append('title',       title);
    formData.append('financial_year', fy);
    formData.append('document_type',  docType);
    formData.append('file', file);
    formData.append('auto_process', 'true');
    try {
      const res = await api.uploadDocument(formData);
      setUploadMsg(`✓ ${res.message}`);
      setTitle('');
      load();
    } catch (e: any) {
      setUploadMsg(`Error: ${e?.response?.data?.detail || e.message}`);
    } finally { setUploading(false); }
  };

  const handleDrop = (e: React.DragEvent) => {
    e.preventDefault(); setDragOver(false);
    const f = e.dataTransfer.files[0];
    if (f) handleFile(f);
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Delete this document and all its indexed chunks?')) return;
    await api.deleteDocument(id);
    setDocuments((prev) => prev.filter((d) => d.id !== id));
  };

  const handleReprocess = async (id: string) => {
    await api.processDocument(id);
    load();
  };

  return (
    <div className="page-container py-8 space-y-7">
      <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-black tracking-tight" style={{ color: 'var(--text-1)', letterSpacing: '-0.02em' }}>
          Document <span style={{ color: 'var(--brand)' }}>Intelligence</span>
        </h1>
        <p className="text-sm mt-1" style={{ color: 'var(--text-3)' }}>
          Upload financial filings. AlphaNexus extracts, chunks, embeds and indexes them for instant AI research.
        </p>
      </motion.div>

      <div className="grid lg:grid-cols-3 gap-6">
        {/* Upload Panel */}
        <div className="card p-5 space-y-4">
          <h3 className="font-bold text-sm" style={{ color: 'var(--text-1)' }}>Upload Document</h3>

          <div className="space-y-3">
            <div>
              <label className="text-xs font-semibold uppercase tracking-wider" style={{ color: 'var(--text-3)' }}>Company</label>
              <select value={companyId} onChange={(e) => setCompanyId(e.target.value)} className="input w-full px-3 py-2 text-sm mt-1">
                <option value="">Select company…</option>
                {companies.map((c) => <option key={c.id} value={c.id}>{c.symbol} — {c.name}</option>)}
              </select>
            </div>
            <div>
              <label className="text-xs font-semibold uppercase tracking-wider" style={{ color: 'var(--text-3)' }}>Title</label>
              <input value={title} onChange={(e) => setTitle(e.target.value)} placeholder="Document title…"
                className="input w-full px-3 py-2 text-sm mt-1" />
            </div>
            <div className="grid grid-cols-2 gap-2">
              <div>
                <label className="text-xs font-semibold uppercase tracking-wider" style={{ color: 'var(--text-3)' }}>Type</label>
                <select value={docType} onChange={(e) => setDocType(e.target.value)} className="input w-full px-2 py-1.5 text-xs mt-1">
                  {DOC_TYPES.map((t) => <option key={t} value={t}>{t}</option>)}
                </select>
              </div>
              <div>
                <label className="text-xs font-semibold uppercase tracking-wider" style={{ color: 'var(--text-3)' }}>FY</label>
                <select value={fy} onChange={(e) => setFy(e.target.value)} className="input w-full px-2 py-1.5 text-xs mt-1">
                  {FY_OPTIONS.map((f) => <option key={f} value={f}>{f}</option>)}
                </select>
              </div>
            </div>
          </div>

          {/* Drop Zone */}
          <div
            onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
            onDragLeave={() => setDragOver(false)}
            onDrop={handleDrop}
            onClick={() => fileRef.current?.click()}
            className="rounded-xl flex flex-col items-center justify-center gap-3 p-6 cursor-pointer transition-all"
            style={{
              border: `2px dashed ${dragOver ? 'var(--brand)' : 'var(--border-strong)'}`,
              background: dragOver ? 'var(--brand-muted)' : 'var(--surface-2)',
            }}
          >
            <CloudUpload className="w-7 h-7" style={{ color: dragOver ? 'var(--brand)' : 'var(--text-4)' }} />
            <div className="text-xs text-center" style={{ color: 'var(--text-3)' }}>
              <span className="font-semibold" style={{ color: 'var(--brand)' }}>Click or drag</span> to upload<br />
              PDF · DOCX · XLSX · CSV · Max 50 MB
            </div>
            <input
              ref={fileRef}
              type="file"
              accept=".pdf,.docx,.doc,.xlsx,.xls,.csv"
              className="hidden"
              onChange={(e) => { const f = e.target.files?.[0]; if (f) handleFile(f); }}
            />
          </div>

          {uploading && (
            <div className="flex items-center gap-2 text-xs" style={{ color: 'var(--brand)' }}>
              <Loader2 className="w-3.5 h-3.5 animate-spin" />
              Uploading and processing…
            </div>
          )}
          {uploadMsg && (
            <div
              className="text-xs rounded-lg p-3"
              style={{
                background: uploadMsg.startsWith('✓') ? 'var(--lime-muted)' : 'rgba(255,100,110,.08)',
                color: uploadMsg.startsWith('✓') ? 'var(--positive-text)' : 'var(--negative-text)',
                border: `1px solid ${uploadMsg.startsWith('✓') ? 'rgba(212,255,36,.2)' : 'rgba(255,100,110,.2)'}`,
              }}
            >
              {uploadMsg}
            </div>
          )}
        </div>

        {/* Document List */}
        <div className="lg:col-span-2 card overflow-hidden">
          <div className="flex items-center justify-between p-4" style={{ borderBottom: '1px solid var(--border)' }}>
            <h3 className="font-bold text-sm" style={{ color: 'var(--text-1)' }}>
              Indexed Documents <span style={{ color: 'var(--text-4)' }}>({documents.length})</span>
            </h3>
            <ANButton variant="ghost" size="xs" icon={<RefreshCw className="w-3.5 h-3.5" />} onClick={load}>
              Refresh
            </ANButton>
          </div>

          <div className="overflow-x-auto">
            {loading ? (
              <div className="p-6 space-y-3">
                {Array.from({ length: 3 }).map((_, i) => (
                  <div key={i} className="skeleton h-10 rounded-lg w-full" />
                ))}
              </div>
            ) : documents.length === 0 ? (
              <div className="py-16 text-center" style={{ color: 'var(--text-4)' }}>
                <FileText className="w-8 h-8 mx-auto mb-2 opacity-30" />
                <div className="text-sm font-medium">No documents uploaded yet.</div>
              </div>
            ) : (
              <table className="w-full text-left text-xs">
                <thead style={{ background: 'var(--surface-2)' }}>
                  <tr className="text-[10px] font-bold uppercase tracking-wider" style={{ color: 'var(--text-4)' }}>
                    {['Document', 'Type', 'FY', 'Pages', 'Chunks', 'Status', ''].map((h) => (
                      <th key={h} className="px-4 py-2.5 font-bold">{h}</th>
                    ))}
                  </tr>
                </thead>
                <tbody>
                  {documents.map((doc) => (
                    <tr key={doc.id} style={{ borderTop: '1px solid var(--border)' }}
                      className="transition-colors hover:bg-[var(--surface-2)]">
                      <td className="px-4 py-3 max-w-[160px]">
                        <div className="font-semibold truncate" style={{ color: 'var(--text-1)' }}>{doc.title}</div>
                        <div className="text-[10px] truncate" style={{ color: 'var(--text-4)' }}>{doc.filename}</div>
                      </td>
                      <td className="px-4 py-3 text-xs" style={{ color: 'var(--text-3)' }}>{doc.document_type}</td>
                      <td className="px-4 py-3 font-mono text-xs" style={{ color: 'var(--text-3)' }}>{doc.financial_year || '—'}</td>
                      <td className="px-4 py-3 font-tabular" style={{ color: 'var(--text-3)' }}>{doc.total_pages}</td>
                      <td className="px-4 py-3 font-tabular" style={{ color: 'var(--lime)' }}>{doc.total_chunks}</td>
                      <td className="px-4 py-3"><StatusBadge status={doc.status} /></td>
                      <td className="px-4 py-3">
                        <div className="flex items-center gap-1.5">
                          <button onClick={() => handleReprocess(doc.id)} title="Reprocess"
                            className="p-1 rounded hover:opacity-80" style={{ color: 'var(--brand)' }}>
                            <RefreshCw className="w-3.5 h-3.5" />
                          </button>
                          <button onClick={() => handleDelete(doc.id)} title="Delete"
                            className="p-1 rounded hover:opacity-80" style={{ color: 'var(--negative-text)' }}>
                            <Trash2 className="w-3.5 h-3.5" />
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
