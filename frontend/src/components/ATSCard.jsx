import { CircularProgressbar, buildStyles } from 'react-circular-progressbar'
import 'react-circular-progressbar/dist/styles.css'

const COLOR = s => s >= 80 ? '#059669' : s >= 60 ? '#4F46E5' : s >= 40 ? '#D97706' : '#DC2626'

export default function ATSCard({ score = 0, label = '', breakdown = {} }) {
  const color = COLOR(score)
  return (
    <div className="card">
      <h3 className="section-title mb-4">ATS Score</h3>
      <div className="flex items-center gap-6">
        <div className="w-28 h-28 flex-shrink-0">
          <CircularProgressbar value={score} text={`${score}`}
            styles={buildStyles({ textColor: color, pathColor: color, trailColor: '#1e293b', textSize: '22px' })} />
        </div>
        <div>
          <p className="text-2xl font-bold" style={{ color }}>{label}</p>
          <p className="text-slate-400 text-sm mt-1">{score}/100 ATS Score</p>
        </div>
      </div>
      {Object.keys(breakdown).length > 0 && (
        <div className="mt-4 space-y-2">
          {Object.entries(breakdown).map(([k, v]) => (
            <div key={k}>
              <div className="flex justify-between text-xs mb-1">
                <span className="text-slate-400 capitalize">{k}</span>
                <span className="text-white font-medium">{v}%</span>
              </div>
              <div className="h-1.5 bg-slate-800 rounded-full overflow-hidden">
                <div className="h-full rounded-full transition-all duration-700"
                  style={{ width: `${v}%`, background: COLOR(v) }} />
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
