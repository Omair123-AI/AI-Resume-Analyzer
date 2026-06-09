import { useState } from 'react'
import { motion } from 'framer-motion'
import { Briefcase, Loader2, Sparkles } from 'lucide-react'
import toast from 'react-hot-toast'
import { matchJD, rewriteBullets } from '../services/api'
import MatchScoreChart from '../charts/MatchScoreChart'

export default function JobMatcher() {
  const [jd, setJD]               = useState('')
  const [loading, setLoading]     = useState(false)
  const [result, setResult]       = useState(null)
  const [bullets, setBullets]     = useState('')
  const [rewritten, setRewritten] = useState(null)
  const [rwLoading, setRwLoading] = useState(false)

  const fileId = localStorage.getItem('resumeFileId')

  const handleMatch = async () => {
    if (!fileId) { toast.error('Upload a resume first'); return }
    if (!jd.trim()) { toast.error('Paste a job description'); return }
    setLoading(true)
    try {
      const data = await matchJD(fileId, jd)
      setResult(data)
      toast.success('Analysis complete!')
    } catch (e) { toast.error(e.message) }
    finally { setLoading(false) }
  }

  const handleRewrite = async () => {
    const lines = bullets.split('\n').map(b => b.trim()).filter(Boolean)
    if (!lines.length) { toast.error('Enter bullet points'); return }
    setRwLoading(true)
    try {
      const data = await rewriteBullets(lines)
      setRewritten(data)
      toast.success('Bullets rewritten!')
    } catch (e) { toast.error(e.message) }
    finally { setRwLoading(false) }
  }

  return (
    <main className="max-w-5xl mx-auto px-4 py-12">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-bold text-white mb-2">Job Description Matcher</h1>
        <p className="text-slate-400 mb-8">Paste a job description to see how well your resume matches</p>

        <div className="card mb-6">
          <div className="flex items-center gap-2 mb-3"><Briefcase className="text-indigo-400 w-5 h-5"/><h3 className="section-title mb-0">Paste Job Description</h3></div>
          <textarea value={jd} onChange={e => setJD(e.target.value)} rows={8}
            placeholder="Paste the full job description here..."
            className="input resize-none font-mono text-sm" />
          <button onClick={handleMatch} disabled={loading} className="btn-primary mt-3 w-full justify-center py-4">
            {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Briefcase className="w-4 h-4" />}
            {loading ? 'Analyzing Match...' : 'Analyze Match'}
          </button>
        </div>

        {result && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
            <div className="grid md:grid-cols-2 gap-6">
              <MatchScoreChart score={result.final_match_score || result.match_score} label={result.grade || ''} />
              <div className="card">
                <h3 className="section-title mb-4">Score Breakdown</h3>
                {[
                  { label: 'Overall Match',  value: result.final_match_score || result.match_score },
                  { label: 'TF-IDF Score',   value: result.tfidf_score },
                  { label: 'Semantic Score', value: result.semantic_score || 0 },
                  { label: 'Skill Overlap',  value: result.skill_overlap?.overlap_pct },
                  { label: 'Keyword Match',  value: result.keyword_overlap?.overlap_pct },
                ].map(({ label, value }) => (
                  <div key={label} className="mb-2">
                    <div className="flex justify-between text-xs mb-1">
                      <span className="text-slate-400">{label}</span>
                      <span className="text-white font-medium">{value?.toFixed(1)}%</span>
                    </div>
                    <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                      <div className="h-full bg-indigo-500 rounded-full" style={{ width: `${value || 0}%` }} />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="grid md:grid-cols-2 gap-6">
              <div className="card">
                <h3 className="section-title mb-3 text-emerald-400">✓ Matched Keywords</h3>
                <div className="flex flex-wrap gap-1.5">
                  {(result.matched_keywords || []).map(k => <span key={k} className="badge badge-green">{k}</span>)}
                </div>
              </div>
              <div className="card">
                <h3 className="section-title mb-3 text-red-400">✗ Missing Keywords</h3>
                <div className="flex flex-wrap gap-1.5">
                  {(result.missing_keywords || []).map(k => <span key={k} className="badge badge-red">{k}</span>)}
                </div>
              </div>
            </div>

            {result.suggestions?.length > 0 && (
              <div className="card">
                <h3 className="section-title mb-3">💡 Suggestions</h3>
                <ul className="space-y-2">
                  {result.suggestions.map((s,i) => <li key={i} className="text-slate-300 text-sm flex gap-2"><span className="text-indigo-400">→</span>{s}</li>)}
                </ul>
              </div>
            )}
          </motion.div>
        )}

        {/* AI Rewriter */}
        <div className="card mt-8">
          <div className="flex items-center gap-2 mb-3"><Sparkles className="text-amber-400 w-5 h-5"/><h3 className="section-title mb-0">AI Resume Rewriter</h3></div>
          <p className="text-slate-400 text-sm mb-3">Enter weak bullet points (one per line) and get AI-enhanced versions</p>
          <textarea value={bullets} onChange={e => setBullets(e.target.value)} rows={5}
            placeholder={"Built a web app\nWorked on machine learning models\nHelped with API development"}
            className="input resize-none font-mono text-sm" />
          <button onClick={handleRewrite} disabled={rwLoading} className="btn-primary mt-3">
            {rwLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
            {rwLoading ? 'Rewriting...' : 'Rewrite Bullets'}
          </button>

          {rewritten && (
            <div className="mt-4 space-y-3">
              {rewritten.original.map((orig, i) => (
                <div key={i} className="bg-slate-800 rounded-xl p-4">
                  <p className="text-red-400 text-sm line-through mb-1">{orig}</p>
                  <p className="text-emerald-400 text-sm">✓ {rewritten.improved[i] || orig}</p>
                </div>
              ))}
            </div>
          )}
        </div>
      </motion.div>
    </main>
  )
}
