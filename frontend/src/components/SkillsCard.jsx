export default function SkillsCard({ skills = {} }) {
  const { found = [], hot_technology = [], in_demand = [] } = skills
  return (
    <div className="card">
      <div className="flex items-center justify-between mb-4">
        <h3 className="section-title">Skills Found</h3>
        <span className="badge badge-blue">{found.length} Total</span>
      </div>
      {hot_technology.length > 0 && (
        <div className="mb-3">
          <p className="text-xs font-semibold text-amber-400 mb-2">🔥 Hot Technologies</p>
          <div className="flex flex-wrap gap-1.5">
            {hot_technology.map(s => <span key={s} className="badge badge-yellow">{s}</span>)}
          </div>
        </div>
      )}
      {in_demand.length > 0 && (
        <div className="mb-3">
          <p className="text-xs font-semibold text-emerald-400 mb-2">⚡ In Demand</p>
          <div className="flex flex-wrap gap-1.5">
            {in_demand.map(s => <span key={s} className="badge badge-green">{s}</span>)}
          </div>
        </div>
      )}
      <div>
        <p className="text-xs font-semibold text-slate-400 mb-2">All Skills</p>
        <div className="flex flex-wrap gap-1.5">
          {found.map(s => <span key={s} className="badge badge-blue">{s}</span>)}
        </div>
      </div>
    </div>
  )
}
