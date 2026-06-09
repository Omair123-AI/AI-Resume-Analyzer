import { Link, useLocation } from 'react-router-dom'
import { BrainCircuit, UploadCloud, LayoutDashboard, Briefcase, Github, Linkedin, FileText, Menu, X } from 'lucide-react'
import { useState } from 'react'

const NAV = [
  { to: '/',          label: 'Home',      icon: BrainCircuit },
  { to: '/upload',    label: 'Upload',    icon: UploadCloud },
  { to: '/dashboard', label: 'Dashboard', icon: LayoutDashboard },
  { to: '/job-match', label: 'Job Match', icon: Briefcase },
  { to: '/github',    label: 'GitHub',    icon: Github },
  { to: '/linkedin',  label: 'LinkedIn',  icon: Linkedin },
  { to: '/report',    label: 'Report',    icon: FileText },
]

export default function Navbar() {
  const { pathname } = useLocation()
  const [open, setOpen] = useState(false)

  return (
    <nav className="sticky top-0 z-50 bg-slate-950/90 backdrop-blur border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-4 flex items-center justify-between h-16">
        <Link to="/" className="flex items-center gap-2">
          <div className="w-8 h-8 bg-gradient-to-br from-indigo-500 to-violet-600 rounded-lg flex items-center justify-center">
            <BrainCircuit className="w-5 h-5 text-white" />
          </div>
          <span className="font-bold text-white hidden sm:block">ResumeAI</span>
        </Link>

        {/* Desktop */}
        <div className="hidden md:flex items-center gap-1">
          {NAV.map(({ to, label, icon: Icon }) => (
            <Link key={to} to={to}
              className={`flex items-center gap-1.5 px-3 py-2 rounded-lg text-sm font-medium transition-all
                ${pathname === to
                  ? 'bg-indigo-600 text-white'
                  : 'text-slate-400 hover:text-white hover:bg-slate-800'}`}>
              <Icon className="w-4 h-4" />{label}
            </Link>
          ))}
        </div>

        {/* Mobile toggle */}
        <button onClick={() => setOpen(!open)} className="md:hidden text-slate-400 hover:text-white">
          {open ? <X /> : <Menu />}
        </button>
      </div>

      {/* Mobile menu */}
      {open && (
        <div className="md:hidden bg-slate-900 border-t border-slate-800 px-4 py-3 flex flex-col gap-1">
          {NAV.map(({ to, label, icon: Icon }) => (
            <Link key={to} to={to} onClick={() => setOpen(false)}
              className={`flex items-center gap-2 px-3 py-2.5 rounded-xl text-sm font-medium transition-all
                ${pathname === to ? 'bg-indigo-600 text-white' : 'text-slate-400 hover:text-white hover:bg-slate-800'}`}>
              <Icon className="w-4 h-4" />{label}
            </Link>
          ))}
        </div>
      )}
    </nav>
  )
}
