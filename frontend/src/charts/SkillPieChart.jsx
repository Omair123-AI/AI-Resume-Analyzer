import { PieChart, Pie, Cell, Tooltip, Legend, ResponsiveContainer } from 'recharts'

const COLORS = ['#4F46E5','#7C3AED','#059669','#D97706','#DC2626','#0891B2']

export default function SkillPieChart({ skills = {} }) {
  const { found = [], hot_technology = [], in_demand = [] } = skills
  const other = found.filter(s => !hot_technology.includes(s) && !in_demand.includes(s))

  const data = [
    { name: 'Hot Tech',   value: hot_technology.length },
    { name: 'In Demand',  value: in_demand.length },
    { name: 'Other',      value: other.length },
  ].filter(d => d.value > 0)

  return (
    <div className="card">
      <h3 className="section-title mb-4">Skill Distribution</h3>
      <ResponsiveContainer width="100%" height={240}>
        <PieChart>
          <Pie data={data} cx="50%" cy="50%" innerRadius={60} outerRadius={90}
            dataKey="value" label={({ name, percent }) => `${name} ${(percent*100).toFixed(0)}%`}
            labelLine={{ stroke: '#64748b' }}>
            {data.map((_, i) => <Cell key={i} fill={COLORS[i % COLORS.length]} />)}
          </Pie>
          <Tooltip contentStyle={{ background: '#1e293b', border: '1px solid #334155', borderRadius: 8 }} />
        </PieChart>
      </ResponsiveContainer>
    </div>
  )
}
