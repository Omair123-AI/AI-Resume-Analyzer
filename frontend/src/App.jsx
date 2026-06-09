import { Routes, Route } from 'react-router-dom'
import Navbar from './components/Navbar'
import Home from './pages/Home'
import ResumeUpload from './pages/ResumeUpload'
import Dashboard from './pages/Dashboard'
import JobMatcher from './pages/JobMatcher'
import GithubAnalysis from './pages/GithubAnalysis'
import LinkedinAnalysis from './pages/LinkedinAnalysis'
import Report from './pages/Report'

export default function App() {
  return (
    <div className="min-h-screen bg-slate-950">
      <Navbar />
      <Routes>
        <Route path="/"         element={<Home />} />
        <Route path="/upload"   element={<ResumeUpload />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/job-match" element={<JobMatcher />} />
        <Route path="/github"   element={<GithubAnalysis />} />
        <Route path="/linkedin" element={<LinkedinAnalysis />} />
        <Route path="/report"   element={<Report />} />
      </Routes>
    </div>
  )
}
