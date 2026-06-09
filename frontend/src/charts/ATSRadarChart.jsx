import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, ResponsiveContainer, Tooltip } from 'recharts'

export default function ATSRadarChart({ breakdown = {} }) {
  const data = Object.entries(breakdown).map(([key, value]) => ({
    subject: key.charAt(0).toUpperCase() + key.slice(1), value
  }))

  return (
    <div className="card">
      <h3 className="section-title mb-4">ATS Breakdown</h3>
      <ResponsiveContainer width="100%" height={280}>
        <RadarChart data={data}>
          <PolarGrid stroke="#334155" />
          <PolarAngleAxis dataKey="subject" tick={{ fill: '#94a3b8', fontSize: 11 }} />
          <PolarRadiusAxis domain={[0, 100]} tick={{ fill: '#64748b', fontSize: 9 }} />
          <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8, color: '#fff' }} />
          <Radar name="Score" dataKey="value" stroke="#4F46E5" fill="#4F46E5" fillOpacity={0.25} strokeWidth={2} />
        </RadarChart>
      </ResponsiveContainer>
    </div>
  )
}
