import { AlertTriangle } from 'lucide-react'

export default function MissingSkills({ data = {} }) {
  const { role, match_percentage, priority_missing = [], other_missing = [], matched_skills = [] } = data
  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-4">
        <AlertTriangle className="text-amber-400 w-5 h-5" />
        <h3 className="section-title mb-0">Missing Skills</h3>
        {role && <span className="badge badge-blue ml-auto">{role}</span>}
      </div>
      {match_percentage !== undefined && (
        <div className="mb-4 flex items-center gap-3">
          <div className="flex-1 h-2 bg-slate-800 rounded-full overflow-hidden">
            <div className="h-full bg-indigo-500 rounded-full transition-all duration-700"
              style={{ width: `${match_percentage}%` }} />
          </div>
          <span className="text-sm font-bold text-indigo-400">{match_percentage}% Match</span>
        </div>
      )}
      {priority_missing.length > 0 && (
        <div className="mb-3">
          <p className="text-xs font-semibold text-red-400 mb-2">🚨 Priority (High Demand)</p>
          <div className="flex flex-wrap gap-1.5">
            {priority_missing.map(s => <span key={s} className="badge badge-red">{s}</span>)}
          </div>
        </div>
      )}
      {other_missing.length > 0 && (
        <div className="mb-3">
          <p className="text-xs font-semibold text-slate-400 mb-2">Other Missing</p>
          <div className="flex flex-wrap gap-1.5">
            {other_missing.map(s => <span key={s} className="badge">{s}</span>)}
          </div>
        </div>
      )}
      {matched_skills.length > 0 && (
        <div>
          <p className="text-xs font-semibold text-emerald-400 mb-2">✓ You Have</p>
          <div className="flex flex-wrap gap-1.5">
            {matched_skills.map(s => <span key={s} className="badge badge-green">{s}</span>)}
          </div>
        </div>
      )}
    </div>
  )
}
