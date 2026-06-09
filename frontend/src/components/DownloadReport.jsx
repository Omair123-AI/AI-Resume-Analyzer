import { useState } from 'react'
import { FileDown, Loader2 } from 'lucide-react'
import toast from 'react-hot-toast'
import { generateReport, downloadReport } from '../services/api'

export default function DownloadReport({ fileId, targetRole = '', jdText = '' }) {
  const [loading, setLoading] = useState(false)

  const handleGenerate = async () => {
    if (!fileId) { toast.error('Upload a resume first'); return }
    setLoading(true)
    try {
      const res = await generateReport(fileId, targetRole, jdText)
      window.open(downloadReport(res.report_id), '_blank')
      toast.success('Report downloaded!')
    } catch (e) {
      toast.error(e.message)
    } finally {
      setLoading(false)
    }
  }

  return (
    <button onClick={handleGenerate} disabled={loading} className="btn-primary">
      {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <FileDown className="w-4 h-4" />}
      {loading ? 'Generating...' : 'Download PDF Report'}
    </button>
  )
}
