import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { motion } from 'framer-motion'
import { Loader2, CheckCircle, User, Mail, Phone, Sparkles } from 'lucide-react'
import toast from 'react-hot-toast'
import UploadCard from '../components/UploadCard'
import ATSCard from '../components/ATSCard'
import ResumeRank from '../components/ResumeRank'
import SkillsCard from '../components/SkillsCard'
import Suggestions from '../components/Suggestions'
import { uploadResume } from '../services/api'
import axios from 'axios'

export default function ResumeUpload() {
  const [file, setFile]           = useState(null)
  const [loading, setLoading]     = useState(false)
  const [aiLoading, setAiLoading] = useState(false)
  const [result, setResult]       = useState(null)
  const [suggestions, setSuggestions] = useState(null)
  const navigate = useNavigate()

  const handleUpload = async () => {
    if (!file) { toast.error('Please select a file first'); return }
    setLoading(true)
    setSuggestions(null)
    try {
      // Step 1: Upload + parse (fast, no Gemini)
      const data = await uploadResume(file)
      setResult(data)
      localStorage.setItem('resumeFileId', data.file_id)
      localStorage.setItem('resumeData', JSON.stringify(data))
      toast.success('Resume analyzed!')

      // Step 2: Fetch AI suggestions separately (with delay)
      fetchSuggestions(data.file_id)

    } catch (e) {
      toast.error(e.message)
    } finally {
      setLoading(false)
    }
  }

  const fetchSuggestions = async (fileId) => {
    setAiLoading(true)
    try {
      // Small delay to avoid rate limit collision with any other calls
      await new Promise(r => setTimeout(r, 2000))
      const res = await axios.post('/api/suggestions', { file_id: fileId })
      setSuggestions(res.data)
      // Update localStorage with suggestions
      const saved = JSON.parse(localStorage.getItem('resumeData') || '{}')
      saved.suggestions = res.data
      localStorage.setItem('resumeData', JSON.stringify(saved))
      toast.success('AI suggestions ready!')
    } catch (e) {
      console.error('Suggestions error:', e)
    } finally {
      setAiLoading(false)
    }
  }

  const parsed = result?.parsed || {}

  return (
    <main className="max-w-5xl mx-auto px-4 py-12">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-bold text-white mb-2">Upload Resume</h1>
        <p className="text-slate-400 mb-8">Get instant ATS score, skill analysis & AI suggestions</p>

        <UploadCard onFile={setFile} file={file} />

        <div className="flex gap-3 mt-4">
          <button onClick={handleUpload} disabled={!file || loading} className="btn-primary flex-1 justify-center py-4">
            {loading
              ? <><Loader2 className="w-4 h-4 animate-spin" />Analyzing...</>
              : '🚀 Analyze Resume'}
          </button>
          {result && (
            <button onClick={() => navigate('/dashboard')} className="btn-secondary px-6">
              View Full Dashboard →
            </button>
          )}
        </div>

        {result && (
          <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} className="mt-10 space-y-6">

            {/* Contact info */}
            <div className="card">
              <div className="flex items-center gap-2 mb-4">
                <CheckCircle className="w-5 h-5 text-emerald-400"/>
                <h3 className="section-title mb-0">Extracted Info</h3>
              </div>
              <div className="grid sm:grid-cols-3 gap-4">
                {[
                  { icon: User,  label: 'Name',  value: parsed.name },
                  { icon: Mail,  label: 'Email', value: parsed.email },
                  { icon: Phone, label: 'Phone', value: parsed.phone },
                ].map(({ icon: Icon, label, value }) => (
                  <div key={label} className="bg-slate-800 rounded-xl px-4 py-3 flex items-center gap-3">
                    <Icon className="w-4 h-4 text-indigo-400 flex-shrink-0" />
                    <div>
                      <p className="label text-xs">{label}</p>
                      <p className="value text-sm">{value || '—'}</p>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <ATSCard score={result.ats?.total} label={result.ats?.label} breakdown={result.ats?.breakdown} />
              <ResumeRank data={result.rank} />
            </div>

            <SkillsCard skills={parsed.skills} />

            {/* AI Suggestions — loads after upload */}
            {aiLoading && (
              <div className="card flex items-center gap-3">
                <Loader2 className="w-5 h-5 text-indigo-400 animate-spin flex-shrink-0" />
                <div>
                  <p className="text-white font-semibold">Generating AI Suggestions...</p>
                  <p className="text-slate-400 text-sm">Gemini is analyzing your resume. This takes a few seconds.</p>
                </div>
              </div>
            )}

            {suggestions && <Suggestions data={suggestions} />}
          </motion.div>
        )}
      </motion.div>
    </main>
  )
}
