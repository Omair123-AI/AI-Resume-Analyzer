import { useState } from 'react'
import { motion } from 'framer-motion'
import { FileText, Download, Loader2, CheckCircle, AlertCircle } from 'lucide-react'
import toast from 'react-hot-toast'
import { generateReport, downloadReport, getRoles } from '../services/api'
import { useEffect } from 'react'

export default function Report() {
  const [loading, setLoading]     = useState(false)
  const [reportId, setReportId]   = useState(null)
  const [roles, setRoles]         = useState([])
  const [targetRole, setRole]     = useState('')
  const [jdText, setJdText]       = useState('')
  const [includeJD, setIncludeJD] = useState(false)

  const fileId = localStorage.getItem('resumeFileId')

  useEffect(() => {
    getRoles().then(r => setRoles(r.roles || [])).catch(() => {})
  }, [])

  const handleGenerate = async () => {
    if (!fileId) { toast.error('Upload a resume first to generate a report'); return }
    setLoading(true)
    try {
      const res = await generateReport(fileId, targetRole, includeJD ? jdText : '')
      setReportId(res.report_id)
      toast.success('Report generated successfully!')
    } catch (e) {
      toast.error(e.message)
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = () => {
    if (!reportId) return
    window.open(downloadReport(reportId), '_blank')
  }

  const REPORT_SECTIONS = [
    'Resume Information (Name, Contact, Links)',
    'ATS Score with Breakdown (0-100)',
    'Extracted Skills & Hot Technologies',
    'Missing Skills for Target Role',
    'Job Description Match Score',
    'Career Readiness Score',
    'AI Improvement Suggestions',
    'Personalized Learning Roadmap',
    'Charts & Visual Analytics',
  ]

  return (
    <main className="max-w-4xl mx-auto px-4 py-12">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-bold text-white mb-2">PDF Career Report</h1>
        <p className="text-slate-400 mb-8">Generate a comprehensive career assessment report with charts and roadmap</p>

        {/* Status */}
        <div className={`card mb-6 border ${fileId ? 'border-emerald-500/30 bg-emerald-500/5' : 'border-amber-500/30 bg-amber-500/5'}`}>
          <div className="flex items-center gap-3">
            {fileId
              ? <CheckCircle className="text-emerald-400 w-5 h-5 flex-shrink-0" />
              : <AlertCircle className="text-amber-400 w-5 h-5 flex-shrink-0" />}
            <div>
              <p className={`font-semibold ${fileId ? 'text-emerald-400' : 'text-amber-400'}`}>
                {fileId ? 'Resume Ready' : 'No Resume Found'}
              </p>
              <p className="text-slate-400 text-sm">
                {fileId
                  ? `File ID: ${fileId.slice(0, 16)}...`
                  : 'Please upload a resume first from the Upload page'}
              </p>
            </div>
            {!fileId && (
              <a href="/upload" className="btn-primary ml-auto text-sm py-2 px-4">Upload Now</a>
            )}
          </div>
        </div>

        {/* Report Options */}
        <div className="card mb-6">
          <h3 className="section-title mb-4">Report Options</h3>

          <div className="mb-4">
            <label className="label text-sm mb-2 block">Target Role (Optional)</label>
            <select value={targetRole} onChange={e => setRole(e.target.value)} className="input">
              <option value="">No specific role</option>
              {roles.map(r => <option key={r} value={r}>{r}</option>)}
            </select>
            <p className="text-slate-500 text-xs mt-1">Adds missing skills & learning roadmap tailored to this role</p>
          </div>

          <div className="mb-4">
            <label className="flex items-center gap-2 cursor-pointer">
              <input type="checkbox" checked={includeJD} onChange={e => setIncludeJD(e.target.checked)}
                className="w-4 h-4 accent-indigo-500" />
              <span className="text-slate-300 text-sm font-medium">Include Job Description Match</span>
            </label>
          </div>

          {includeJD && (
            <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }}>
              <label className="label text-sm mb-2 block">Paste Job Description</label>
              <textarea value={jdText} onChange={e => setJdText(e.target.value)}
                className="input resize-none font-mono text-sm" rows={5}
                placeholder="Paste the job description to include match analysis in report..." />
            </motion.div>
          )}
        </div>

        {/* What's included */}
        <div className="card mb-6">
          <h3 className="section-title mb-4">What's Included in the Report</h3>
          <div className="grid md:grid-cols-2 gap-2">
            {REPORT_SECTIONS.map((section, i) => (
              <div key={i} className="flex items-center gap-2 text-sm text-slate-300">
                <CheckCircle className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                {section}
              </div>
            ))}
          </div>
        </div>

        {/* Generate / Download buttons */}
        <div className="flex gap-3">
          <button onClick={handleGenerate} disabled={loading || !fileId} className="btn-primary flex-1 justify-center py-4">
            {loading
              ? <><Loader2 className="w-4 h-4 animate-spin" />Generating Report...</>
              : <><FileText className="w-4 h-4" />Generate PDF Report</>}
          </button>

          {reportId && (
            <motion.button initial={{ opacity: 0, scale: 0.9 }} animate={{ opacity: 1, scale: 1 }}
              onClick={handleDownload} className="btn-secondary px-6">
              <Download className="w-4 h-4" /> Download
            </motion.button>
          )}
        </div>

        {reportId && (
          <motion.div initial={{ opacity: 0, y: 10 }} animate={{ opacity: 1, y: 0 }}
            className="mt-6 card border-emerald-500/30 bg-emerald-500/5">
            <div className="flex items-center gap-3">
              <CheckCircle className="text-emerald-400 w-6 h-6 flex-shrink-0" />
              <div>
                <p className="text-emerald-400 font-semibold">Report Generated Successfully!</p>
                <p className="text-slate-400 text-sm mt-0.5">Your PDF report is ready to download.</p>
              </div>
              <button onClick={handleDownload} className="btn-primary ml-auto">
                <Download className="w-4 h-4" /> Download PDF
              </button>
            </div>
          </motion.div>
        )}
      </motion.div>
    </main>
  )
}
