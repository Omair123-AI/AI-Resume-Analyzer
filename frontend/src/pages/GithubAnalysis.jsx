import { useState } from 'react'
import { motion } from 'framer-motion'
import { Github, Loader2, Star, GitFork, Users, Code } from 'lucide-react'
import toast from 'react-hot-toast'
import { analyzeGitHub } from '../services/api'
import { CircularProgressbar, buildStyles } from 'react-circular-progressbar'

export default function GithubAnalysis() {
  const [url, setUrl]       = useState('')
  const [loading, setLoad]  = useState(false)
  const [result, setResult] = useState(null)

  const handleAnalyze = async () => {
    if (!url.trim()) { toast.error('Enter a GitHub profile URL'); return }
    setLoad(true)
    try {
      const data = await analyzeGitHub(url.trim())
      setResult(data)
      toast.success('GitHub profile analyzed!')
    } catch (e) { toast.error(e.message) }
    finally { setLoad(false) }
  }

  const color = s => s >= 70 ? '#059669' : s >= 50 ? '#4F46E5' : '#D97706'

  return (
    <main className="max-w-4xl mx-auto px-4 py-12">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <h1 className="text-3xl font-bold text-white mb-2">GitHub Analyzer</h1>
        <p className="text-slate-400 mb-8">Analyze your GitHub profile strength and get improvement tips</p>

        <div className="card mb-8">
          <div className="flex gap-3">
            <input value={url} onChange={e => setUrl(e.target.value)} className="input"
              placeholder="https://github.com/yourusername"
              onKeyDown={e => e.key === 'Enter' && handleAnalyze()} />
            <button onClick={handleAnalyze} disabled={loading} className="btn-primary px-6">
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Github className="w-4 h-4" />}
              {loading ? 'Analyzing...' : 'Analyze'}
            </button>
          </div>
        </div>

        {result && (
          <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="space-y-6">
            {/* Score + Profile */}
            <div className="grid md:grid-cols-2 gap-6">
              <div className="card text-center">
                <div className="w-32 h-32 mx-auto mb-4">
                  <CircularProgressbar value={result.score} text={`${result.score}`}
                    styles={buildStyles({ textColor: color(result.score), pathColor: color(result.score), trailColor: '#1e293b', textSize: '20px' })} />
                </div>
                <p className="text-xl font-bold" style={{ color: color(result.score) }}>{result.score_label}</p>
                <p className="text-slate-400 text-sm">GitHub Strength Score</p>
              </div>

              <div className="card">
                {result.avatar_url && <img src={result.avatar_url} alt="avatar" className="w-14 h-14 rounded-full mb-3" />}
                <p className="text-xl font-bold text-white">{result.name || result.username}</p>
                <p className="text-slate-400 text-sm mb-3">@{result.username}</p>
                {result.bio && <p className="text-slate-300 text-sm mb-3">{result.bio}</p>}
                <div className="grid grid-cols-3 gap-2 text-center">
                  {[
                    { icon: Code,   label: 'Repos',     value: result.public_repos },
                    { icon: Users,  label: 'Followers', value: result.followers },
                    { icon: Star,   label: 'Stars',     value: result.stats?.total_stars },
                  ].map(({ icon: Icon, label, value }) => (
                    <div key={label} className="bg-slate-800 rounded-xl p-2">
                      <p className="text-lg font-bold text-indigo-400">{value || 0}</p>
                      <p className="text-slate-500 text-xs">{label}</p>
                    </div>
                  ))}
                </div>
              </div>
            </div>

            {/* Score breakdown */}
            <div className="card">
              <h3 className="section-title mb-4">Score Breakdown</h3>
              {Object.entries(result.score_breakdown || {}).map(([k, v]) => (
                <div key={k} className="mb-3">
                  <div className="flex justify-between text-xs mb-1">
                    <span className="text-slate-400 capitalize">{k.replace(/_/g, ' ')}</span>
                    <span className="text-white font-medium">{v?.toFixed(1)}</span>
                  </div>
                  <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                    <div className="h-full rounded-full transition-all" style={{ width: `${(v / 25) * 100}%`, background: color(v * 4) }} />
                  </div>
                </div>
              ))}
            </div>

            {/* Languages */}
            {result.top_languages?.length > 0 && (
              <div className="card">
                <h3 className="section-title mb-3">Top Languages</h3>
                <div className="flex flex-wrap gap-2">
                  {result.top_languages.map(({ language }) => (
                    <span key={language} className="badge badge-blue">{language}</span>
                  ))}
                </div>
              </div>
            )}

            {/* Top repos */}
            {result.top_repos?.length > 0 && (
              <div className="card">
                <h3 className="section-title mb-4">Top Repositories</h3>
                <div className="space-y-3">
                  {result.top_repos.map(repo => (
                    <div key={repo.name} className="bg-slate-800 rounded-xl p-4">
                      <div className="flex items-start justify-between">
                        <a href={repo.url} target="_blank" rel="noreferrer"
                          className="text-indigo-400 font-semibold hover:underline">{repo.name}</a>
                        <div className="flex gap-3 text-slate-400 text-xs">
                          <span className="flex items-center gap-1"><Star className="w-3 h-3"/>{repo.stars}</span>
                          <span className="flex items-center gap-1"><GitFork className="w-3 h-3"/>{repo.forks}</span>
                        </div>
                      </div>
                      {repo.description && <p className="text-slate-400 text-sm mt-1">{repo.description}</p>}
                      {repo.language && <span className="badge badge-blue mt-2 text-xs">{repo.language}</span>}
                    </div>
                  ))}
                </div>
              </div>
            )}

            {/* Suggestions */}
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
      </motion.div>
    </main>
  )
}
