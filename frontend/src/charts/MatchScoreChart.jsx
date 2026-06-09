import { CircularProgressbar, buildStyles } from 'react-circular-progressbar'
import 'react-circular-progressbar/dist/styles.css'

export default function MatchScoreChart({ score = 0, label = '' }) {
  const color = score >= 80 ? '#059669' : score >= 60 ? '#4F46E5' : score >= 40 ? '#D97706' : '#DC2626'

  return (
    <div className="card text-center">
      <h3 className="section-title mb-6">JD Match Score</h3>
      <div className="w-40 h-40 mx-auto mb-4">
        <CircularProgressbar
          value={score}
          text={`${score}%`}
          styles={buildStyles({
            textColor: color,
            pathColor: color,
            trailColor: '#1e293b',
            textSize: '18px',
            strokeLinecap: 'round',
          })}
        />
      </div>
      <p className="text-lg font-bold mt-2" style={{ color }}>{label}</p>
    </div>
  )
}