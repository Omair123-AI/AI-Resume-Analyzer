import { Link } from 'react-router-dom'
import { motion } from 'framer-motion'
import { UploadCloud, BarChart2, Zap, Github, Linkedin, FileText, Star, ChevronRight } from 'lucide-react'

const FEATURES = [
  { icon: UploadCloud, title: 'Smart Resume Parsing',    desc: 'Extracts skills, experience, education, projects & certifications from PDF/DOCX.', color: 'text-indigo-400' },
  { icon: BarChart2,   title: 'ATS Score (0-100)',        desc: 'Multi-factor ATS scoring across skills, keywords, formatting & experience.', color: 'text-violet-400' },
  { icon: Zap,         title: 'AI Resume Rewriter',       desc: 'Transform weak bullets into impactful achievement statements using Gemini AI.', color: 'text-amber-400' },
  { icon: Github,      title: 'GitHub Analyzer',          desc: 'Score your GitHub profile on repos, languages, stars & project quality.', color: 'text-slate-300' },
  { icon: Linkedin,    title: 'LinkedIn Analyzer',        desc: 'Audit your LinkedIn completeness and get personalized improvement tips.', color: 'text-blue-400' },
  { icon: FileText,    title: 'PDF Career Report',        desc: 'Download a full career assessment report with charts, scores & roadmap.', color: 'text-emerald-400' },
]

const STATS = [
  { value: '50,000+', label: 'Skills in Database' },
  { value: '200+',    label: 'Job Roles Mapped' },
  { value: '100',     label: 'ATS Score Scale' },
  { value: '5+',      label: 'AI Integrations' },
]

export default function Home() {
  return (
    <main className="max-w-6xl mx-auto px-4 py-16">
      {/* Hero */}
      <motion.div initial={{ opacity: 0, y: 30 }} animate={{ opacity: 1, y: 0 }} transition={{ duration: 0.6 }} className="text-center mb-20">
        <div className="inline-flex items-center gap-2 bg-indigo-500/10 border border-indigo-500/30 text-indigo-300 text-sm font-medium px-4 py-1.5 rounded-full mb-6">
          <Star className="w-4 h-4" /> AI-Powered Career Intelligence Platform
        </div>
        <h1 className="text-5xl md:text-6xl font-extrabold text-white leading-tight mb-6">
          Analyze. Improve.<br />
          <span className="gradient-text">Get Hired.</span>
        </h1>
        <p className="text-slate-400 text-lg max-w-2xl mx-auto mb-10 leading-relaxed">
          Upload your resume and get instant ATS scoring, skill gap analysis, AI-powered suggestions,
          job matching, and a personalized learning roadmap — all in one platform.
        </p>
        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <Link to="/upload" className="btn-primary text-base px-8 py-4 justify-center">
            <UploadCloud className="w-5 h-5" /> Analyze My Resume <ChevronRight className="w-4 h-4" />
          </Link>
          <Link to="/dashboard" className="btn-secondary text-base px-8 py-4 justify-center">
            <BarChart2 className="w-5 h-5" /> View Dashboard
          </Link>
        </div>
      </motion.div>

      {/* Stats */}
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.3 }}
        className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-20">
        {STATS.map(({ value, label }) => (
          <div key={label} className="card text-center">
            <p className="text-3xl font-extrabold gradient-text">{value}</p>
            <p className="text-slate-400 text-sm mt-1">{label}</p>
          </div>
        ))}
      </motion.div>

      {/* Features */}
      <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.5 }}>
        <h2 className="text-3xl font-bold text-white text-center mb-3">Everything You Need</h2>
        <p className="text-slate-400 text-center mb-10">Not just an ATS checker — a complete career intelligence platform</p>
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {FEATURES.map(({ icon: Icon, title, desc, color }) => (
            <div key={title} className="card-hover group">
              <Icon className={`w-8 h-8 ${color} mb-3 group-hover:scale-110 transition-transform`} />
              <h3 className="font-bold text-white mb-2">{title}</h3>
              <p className="text-slate-400 text-sm leading-relaxed">{desc}</p>
            </div>
          ))}
        </div>
      </motion.div>

      {/* CTA */}
      <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} transition={{ delay: 0.7 }}
        className="mt-20 text-center bg-gradient-to-r from-indigo-600/20 to-violet-600/20 border border-indigo-500/30 rounded-3xl p-12">
        <h2 className="text-3xl font-bold text-white mb-4">Ready to land your dream job?</h2>
        <p className="text-slate-400 mb-8">Upload your resume and get a full analysis in under 30 seconds.</p>
        <Link to="/upload" className="btn-primary inline-flex text-base px-10 py-4">
          <UploadCloud className="w-5 h-5" /> Start Free Analysis
        </Link>
      </motion.div>
    </main>
  )
}
