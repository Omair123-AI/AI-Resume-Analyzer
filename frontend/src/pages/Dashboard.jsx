import { useState, useEffect } from 'react'
import { motion } from 'framer-motion'
import { BarChart2, Target, BookOpen, Loader2, RefreshCw } from 'lucide-react'
import toast from 'react-hot-toast'
import ATSCard from '../components/ATSCard'
import SkillsCard from '../components/SkillsCard'
import MissingSkills from '../components/MissingSkills'
import ResumeRank from '../components/ResumeRank'
import Suggestions from '../components/Suggestions'
import ATSRadarChart from '../charts/ATSRadarChart'
import SkillPieChart from '../charts/SkillPieChart'
import SectionAnalysisChart from '../charts/SectionAnalysisChart'
import KeywordChart from '../charts/KeywordChart'
import DownloadReport from '../components/DownloadReport'
import { getRoles, getMissingSkills, getCareerAnalysis } from '../services/api'

export default function Dashboard() {
  const [data, setData]             = useState(null)
  const [roles, setRoles]           = useState([])
  const [selectedRole, setRole]     = useState('')
  const [missingData, setMissing]   = useState(null)
  const [careerData, setCareer]     = useState(null)
  const [loading, setLoading]       = useState(false)

  useEffect(() => {
    const saved = localStorage.getItem('resumeData')
    if (saved) setData(JSON.parse(saved))
    getRoles().then(r => setRoles(r.roles || [])).catch(() => {})
  }, [])

  const fileId = data?.file_id
  const parsed = data?.parsed || {}
  const ats    = data?.ats    || {}
  const rank   = data?.rank   || {}

  const handleRoleAnalysis = async () => {
    if (!fileId || !selectedRole) { toast.error('Select a target role'); return }
    setLoading(true)
    try {
      const [ms, ca] = await Promise.all([
        getMissingSkills(fileId, selectedRole),
        getCareerAnalysis(fileId, selectedRole),
      ])
      setMissing(ms)
      setCareer(ca)
      toast.success('Career analysis complete!')
    } catch (e) { toast.error(e.message) }
    finally { setLoading(false) }
  }

  if (!data) return (
    <div className="max-w-4xl mx-auto px-4 py-24 text-center">
      <BarChart2 className="w-16 h-16 text-slate-600 mx-auto mb-4" />
      <h2 className="text-2xl font-bold text-white mb-2">No Resume Analyzed Yet</h2>
      <p className="text-slate-400 mb-6">Upload a resume first to see your dashboard.</p>
      <a href="/upload" className="btn-primary inline-flex">Upload Resume</a>
    </div>
  )

  return (
    <main className="max-w-6xl mx-auto px-4 py-10">
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}>
        <div className="flex flex-wrap items-center justify-between gap-4 mb-8">
          <div>
            <h1 className="text-3xl font-bold text-white">Dashboard</h1>
            <p className="text-slate-400">{parsed.name || 'Your Resume'} — Full Analysis</p>
          </div>
          <DownloadReport fileId={fileId} targetRole={selectedRole} />
        </div>

        {/* KPI Cards */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
          {[
            { label: 'ATS Score',        value: `${ats.total || 0}/100`,         color: 'text-indigo-400' },
            { label: 'Resume Rank',      value: rank.rank || '—',                color: 'text-violet-400' },
            { label: 'Skills Found',     value: parsed.skills?.count || 0,       color: 'text-emerald-400' },
            { label: 'Certifications',   value: parsed.certifications?.count||0, color: 'text-amber-400' },
          ].map(({ label, value, color }) => (
            <div key={label} className="card text-center">
              <p className={`text-2xl font-extrabold ${color}`}>{value}</p>
              <p className="label mt-1">{label}</p>
            </div>
          ))}
        </div>

        {/* Charts Row */}
        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <ATSRadarChart breakdown={ats.breakdown || {}} />
          <SkillPieChart skills={parsed.skills || {}} />
        </div>
        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <SectionAnalysisChart breakdown={ats.breakdown || {}} />
          <KeywordChart keywords={parsed.keywords || []} />
        </div>

        {/* Scores Row */}
        <div className="grid md:grid-cols-2 gap-6 mb-6">
          <ATSCard score={ats.total} label={ats.label} breakdown={ats.breakdown} />
          <ResumeRank data={rank} />
        </div>

        {/* Skills */}
        <SkillsCard skills={parsed.skills || {}} />

        {/* Target Role Analysis */}
        <div className="card mt-6">
          <div className="flex items-center gap-2 mb-4"><Target className="text-indigo-400 w-5 h-5"/><h3 className="section-title mb-0">Target Role Analysis</h3></div>
          <div className="flex gap-3">
            <select value={selectedRole} onChange={e => setRole(e.target.value)} className="input flex-1">
              <option value="">Select target role...</option>
              {roles.map(r => <option key={r} value={r}>{r}</option>)}
            </select>
            <button onClick={handleRoleAnalysis} disabled={loading || !selectedRole} className="btn-primary">
              {loading ? <Loader2 className="w-4 h-4 animate-spin"/> : <RefreshCw className="w-4 h-4"/>}
              Analyze
            </button>
          </div>
        </div>

        {missingData && <div className="mt-4"><MissingSkills data={missingData} /></div>}

        {/* Career Readiness */}
        {careerData?.career_readiness && (
          <div className="card mt-6">
            <div className="flex items-center gap-2 mb-4"><Target className="text-violet-400 w-5 h-5"/><h3 className="section-title mb-0">Career Readiness</h3></div>
            <div className="flex items-center gap-4 mb-4">
              <span className="text-4xl font-extrabold text-violet-400">{careerData.career_readiness.score}</span>
              <div><p className="text-white font-semibold">{careerData.career_readiness.label}</p><p className="text-slate-400 text-sm">Career Readiness Score</p></div>
            </div>
            <div className="grid grid-cols-2 md:grid-cols-5 gap-3">
              {Object.entries(careerData.career_readiness.breakdown || {}).map(([k,v]) => (
                <div key={k} className="bg-slate-800 rounded-xl p-3 text-center">
                  <p className="text-lg font-bold text-violet-400">{v}%</p>
                  <p className="text-slate-400 text-xs capitalize mt-0.5">{k}</p>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Learning Roadmap */}
        {careerData?.learning_roadmap?.steps && (
          <div className="card mt-6">
            <div className="flex items-center gap-2 mb-4"><BookOpen className="text-emerald-400 w-5 h-5"/><h3 className="section-title mb-0">Learning Roadmap</h3></div>
            <p className="text-slate-400 text-sm mb-4">Goal: <span className="text-white font-semibold">{careerData.learning_roadmap.goal}</span> · {careerData.learning_roadmap.estimated_time}</p>
            <div className="space-y-3">
              {careerData.learning_roadmap.steps.map((s) => (
                <div key={s.step} className="flex gap-4 bg-slate-800 rounded-xl p-4">
                  <div className="w-8 h-8 bg-indigo-600 rounded-full flex items-center justify-center text-white font-bold text-sm flex-shrink-0">{s.step}</div>
                  <div>
                    <p className="text-white font-semibold">{s.title}</p>
                    <p className="text-slate-400 text-sm mt-0.5">{s.description}</p>
                    <div className="flex flex-wrap gap-1.5 mt-2">
                      {(s.resources || []).map(r => <span key={r} className="badge badge-blue text-xs">{r}</span>)}
                      <span className="badge badge-yellow text-xs">{s.duration}</span>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        <Suggestions data={data.suggestions || {}} />
      </motion.div>
    </main>
  )
}
