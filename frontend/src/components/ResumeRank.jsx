import { Trophy, TrendingUp, AlertCircle } from 'lucide-react'

const RANK_CONFIG = {
  Excellent: { color: 'text-emerald-400', bg: 'bg-emerald-500/10 border-emerald-500/30', icon: '🏆' },
  Good:      { color: 'text-indigo-400',  bg: 'bg-indigo-500/10 border-indigo-500/30',  icon: '👍' },
  Average:   { color: 'text-amber-400',   bg: 'bg-amber-500/10 border-amber-500/30',    icon: '📈' },
  Poor:      { color: 'text-red-400',     bg: 'bg-red-500/10 border-red-500/30',        icon: '⚠️' },
}

export default function ResumeRank({ data = {} }) {
  const { rank, percentile, strengths = [], weaknesses = [], next_steps = [] } = data
  const cfg = RANK_CONFIG[rank] || RANK_CONFIG.Average

  return (
    <div className="card">
      <h3 className="section-title mb-4">Resume Rank</h3>
      <div className={`rounded-xl border px-4 py-3 mb-4 flex items-center gap-3 ${cfg.bg}`}>
        <span className="text-2xl">{cfg.icon}</span>
        <div>
          <p className={`text-xl font-bold ${cfg.color}`}>{rank}</p>
          <p className="text-slate-400 text-sm">Top {100 - percentile}% of resumes</p>
        </div>
      </div>
      {strengths.length > 0 && (
        <div className="mb-3">
          <p className="text-xs font-semibold text-emerald-400 mb-1.5 flex items-center gap-1"><TrendingUp className="w-3.5 h-3.5"/>Strengths</p>
          <ul className="space-y-1">{strengths.map((s,i) => <li key={i} className="text-xs text-slate-300 flex gap-1.5"><span className="text-emerald-400">✓</span>{s}</li>)}</ul>
        </div>
      )}
      {weaknesses.length > 0 && (
        <div className="mb-3">
          <p className="text-xs font-semibold text-amber-400 mb-1.5 flex items-center gap-1"><AlertCircle className="w-3.5 h-3.5"/>Improve</p>
          <ul className="space-y-1">{weaknesses.map((w,i) => <li key={i} className="text-xs text-slate-300 flex gap-1.5"><span className="text-amber-400">!</span>{w}</li>)}</ul>
        </div>
      )}
      {next_steps.length > 0 && (
        <div>
          <p className="text-xs font-semibold text-indigo-400 mb-1.5">Next Steps</p>
          <ol className="space-y-1">{next_steps.map((s,i) => <li key={i} className="text-xs text-slate-300 flex gap-1.5"><span className="text-indigo-400 font-bold">{i+1}.</span>{s}</li>)}</ol>
        </div>
      )}
    </div>
  )
}
