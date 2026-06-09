import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Cell } from 'recharts'

const COLOR = v => v >= 70 ? '#059669' : v >= 50 ? '#4F46E5' : v >= 30 ? '#D97706' : '#DC2626'

export default function SectionAnalysisChart({ breakdown = {} }) {
  const data = Object.entries(breakdown).map(([k, v]) => ({
    name: k.charAt(0).toUpperCase() + k.slice(1), score: v
  }))

  return (
    <div className="card">
      <h3 className="section-title mb-4">Section Analysis</h3>
      <ResponsiveContainer width="100%" height={240}>
        <BarChart data={data} layout="vertical">
          <CartesianGrid strokeDasharray="3 3" stroke="#1e293b" />
          <XAxis type="number" domain={[0, 100]} tick={{ fill: '#64748b', fontSize: 10 }} />
          <YAxis type="category" dataKey="name" tick={{ fill: '#94a3b8', fontSize: 11 }} width={80} />
          <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8, color: '#fff' }}
            formatter={(v) => [`${v}%`, 'Score']} />
          <Bar dataKey="score" radius={[0, 6, 6, 0]}>
            {data.map((entry, i) => <Cell key={i} fill={COLOR(entry.score)} />)}
          </Bar>
        </BarChart>
      </ResponsiveContainer>
    </div>
  )
}
