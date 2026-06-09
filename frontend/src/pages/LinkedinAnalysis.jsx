import { useState } from 'react'
import { motion } from 'framer-motion'
import { Linkedin, Loader2, Plus, Minus } from 'lucide-react'
import toast from 'react-hot-toast'
import { analyzeLinkedIn } from '../services/api'
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar'

export default function LinkedinAnalysis() {
  const [url, setUrl]           = useState('')
  const [loading, setLoad]      = useState(false)
  const [result, setResult]     = useState(null)
  const [advanced, setAdvanced] = useState(false)
  const [profile, setProfile]   = useState({
    headline: '', summary: '', skills: '', experience_count: '',
    recommendations: '', certifications: '', projects: '', education: ''
  })

  const handleAnalyze = async () => {
    if (!url.trim()) { toast.error('Enter a LinkedIn profile URL'); return }
    setLoad(true)
    try {
      const profileData = advanced ? {
        ...profile,
        skills: profile.skills ? profile.skills.split(',').map(s => s.trim()).filter(Boolean) : [],
        experience_count: parseInt(profile.experience_count) || 0,
        recommendations:  parseInt(profile.recommendations)  || 0,
        certifications:   parseInt(profile.certifications)   || 0,
        projects:         parseInt(profile.projects)         || 0,
      } : null
      const data = await analyzeLinkedIn(url.trim(), profileData)
      setResult(data)
      toast.success('LinkedIn profile analyzed!')
    } catch (e) { toast.error(e.message) }
    finally { setLoad(false) }
  }

  const color = s => s >= 70 ? '#059669' : s >= 50 ? '#4F46E5' : '#D97706'

  return (
    <main className="max-w-4xl mx-auto px-4 py-12">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-bold text-white mb-2">LinkedIn Analyzer</h1>
        <p className="text-slate-400 mb-8">Audit your LinkedIn profile and get optimization tips</p>

        <div className="card mb-6">
          <div className="flex gap-3 mb-4">
            <input value={url} onChange={e => setUrl(e.target.value)} className="input"
              placeholder="https://linkedin.com/in/yourprofile"
              onKeyDown={e => e.key === 'Enter' && handleAnalyze()} />
            <button onClick={handleAnalyze} disabled={loading} className="btn-primary px-6">
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Linkedin className="w-4 h-4" />}
              {loading ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>

          <button onClick={() => setAdvanced(!advanced)} className="flex items-center gap-2 text-indigo-400 text-sm font-medium hover:text-indigo-300 transition-colors">
            {advanced ? <Minus className="w-4 h-4" /> : <Plus className="w-4 h-4" />}
            {advanced ? 'Hide' : 'Add'} Profile Details (for deeper analysis)
          </button>

          {advanced && (
            <motion.div initial={{ opacity: 0, height: 0 }} animate={{ opacity: 1, height: 'auto' }}
              className="mt-4 grid grid-cols-1 md:grid-cols-2 gap-3">
              <div>
                <label className="label text-xs mb-1 block">Headline</label>
                <input value={profile.headline} onChange={e => setProfile({...profile, headline: e.target.value})}
                  className="input text-sm" placeholder="Senior Software Engineer | React & Node.js" />
              </div>
              <div>
                <label className="label text-xs mb-1 block">Skills (comma-separated)</label>
                <input value={profile.skills} onChange={e => setProfile({...profile, skills: e.target.value})}
                  className="input text-sm" placeholder="Python, React, AWS, SQL..." />
              </div>
              <div className="md:col-span-2">
                <label className="label text-xs mb-1 block">Summary (paste your about section)</label>
                <textarea value={profile.summary} onChange={e => setProfile({...profile, summary: e.target.value})}
                  className="input resize-none text-sm" rows={3} placeholder="Your LinkedIn about section..." />
              </div>
              {[
                { key: 'experience_count', label: 'Number of Experience Entries', placeholder: '3' },
                { key: 'recommendations',  label: 'Recommendations Received',     placeholder: '5' },
                { key: 'certifications',   label: 'Certifications Listed',        placeholder: '2' },
                { key: 'projects',         label: 'Projects Listed',              placeholder: '2' },
              ].map(({ key, label, placeholder }) => (
                <div key={key}>
                  <label className="label text-xs mb-1 block">{label}</label>
                  <input type="number" min="0" value={profile[key]}
                    onChange={e => setProfile({...profile, [key]: e.target.value})}
                    className="input text-sm" placeholder={placeholder} />
                </div>
              ))}
            </motion.div>
          )}
        </div>

        {result && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">

            {/* Score card */}
            {result.score !== undefined && (
              <div className="grid md:grid-cols-2 gap-6">
                <div className="card text-center">
                  <div className="w-32 h-32 mx-auto mb-4">
                    <CircularProgressbar value={result.score} text={`${result.score}`}
                      styles={buildStyles({ textColor: color(result.score), pathColor: color(result.score), trailColor: '#1e293b', textSize: '20px' })} />
                  </div>
                  <p className="text-xl font-bold" style={{ color: color(result.score) }}>{result.label}</p>
                  <p className="text-slate-400 text-sm">LinkedIn Profile Score</p>
                </div>

                <div className="card">
                  <h3 className="section-title mb-4">Score Breakdown</h3>
                  {Object.entries(result.breakdown || {}).map(([k, v]) => (
                    <div key={k} className="mb-2">
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-slate-400 capitalize">{k}</span>
                        <span className="text-white font-medium">{v?.toFixed(1)}</span>
                      </div>
                      <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                        <div className="h-full rounded-full transition-all duration-700"
                          style={{ width: `${(v / 20) * 100}%`, background: color(v * 5) }} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Analysis details */}
            {result.analysis && (
              <div className="card">
                <h3 className="section-title mb-4">Profile Analysis</h3>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                  {[
                    { label: 'Skills',          value: result.analysis.skills_count },
                    { label: 'Experience',       value: result.analysis.experience_count },
                    { label: 'Recommendations',  value: result.analysis.recommendations },
                    { label: 'Certifications',   value: result.analysis.certifications },
                  ].map(({ label, value }) => (
                    <div key={label} className="bg-slate-800 rounded-xl p-3 text-center">
                      <p className="text-2xl font-bold text-indigo-400">{value ?? '—'}</p>
                      <p className="text-slate-400 text-xs mt-1">{label}</p>
                    </div>
                  ))}
                </div>
                {result.analysis.headline && (
                  <div className="mt-4 bg-slate-800 rounded-xl p-3">
                    <p className="text-slate-400 text-xs mb-1">Headline</p>
                    <p className="text-white text-sm">{result.analysis.headline}</p>
                  </div>
                )}
                <div className="flex gap-3 mt-3">
                  <span className={`badge ${result.analysis.summary ? 'badge-green' : 'badge-red'}`}>
                    {result.analysis.summary ? '✓ Has Summary' : '✗ No Summary'}
                  </span>
                  <span className={`badge ${result.analysis.has_education ? 'badge-green' : 'badge-red'}`}>
                    {result.analysis.has_education ? '✓ Education Listed' : '✗ No Education'}
                  </span>
                </div>
              </div>
            )}

            {/* Manual checklist (URL-only mode) */}
            {result.manual_checklist && (
              <div className="card">
                <h3 className="section-title mb-4">📋 Profile Checklist</h3>
                <p className="text-slate-400 text-sm mb-4">{result.message}</p>
                <ul className="space-y-2">
                  {result.manual_checklist.map((item, i) => (
                    <li key={i} className="flex items-start gap-3 text-sm text-slate-300 bg-slate-800 rounded-xl px-4 py-3">
                      <span className="text-indigo-400 font-bold mt-0.5">{i + 1}.</span>{item}
                    </li>
                  ))}
                </ul>
              </div>
            )}

            {/* Suggestions */}
            {result.suggestions?.length > 0 && (
              <div className="card">
                <h3 className="section-title mb-3">💡 Optimization Tips</h3>
                <ul className="space-y-2">
                  {result.suggestions.map((s, i) => (
                    <li key={i} className="text-slate-300 text-sm flex gap-2">
                      <span className="text-indigo-400 mt-0.5">→</span>{s}
                    </li>
                  ))}
                </ul>
              </div>
            )}
          </motion.div>
        )}
      </motion.div>
    </main>
  )
}
