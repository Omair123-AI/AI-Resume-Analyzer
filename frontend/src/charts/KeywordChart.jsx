export default function KeywordChart({ keywords = [] }) {
  return (
    <div className="card">
      <h3 className="section-title mb-4">Top Keywords</h3>
      <div className="flex flex-wrap gap-2">
        {keywords.slice(0, 30).map((kw, i) => {
          const size = i < 5 ? 'text-base font-bold' : i < 15 ? 'text-sm font-semibold' : 'text-xs'
          const opacity = Math.max(0.4, 1 - i * 0.025)
          return (
            <span key={kw} className={`${size} text-indigo-400 px-2 py-1 bg-indigo-500/10 rounded-lg`}
              style={{ opacity }}>{kw}</span>
          )
        })}
      </div>
    </div>
  )
}
