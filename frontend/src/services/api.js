import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 60000,
})

api.interceptors.response.use(
  res => res.data,
  err => {
    const msg = err.response?.data?.error || err.message || 'Something went wrong'
    return Promise.reject(new Error(msg))
  }
)

// Upload & Analysis
export const uploadResume    = (file) => { const fd = new FormData(); fd.append('resume', file); return api.post('/upload', fd) }
export const getAnalysis     = (fileId) => api.get(`/analyze/${fileId}`)
export const getATSScore     = (fileId) => api.get(`/ats/${fileId}`)

// Roles & Skills
export const getRoles        = () => api.get('/roles')
export const getMissingSkills = (fileId, targetRole) => api.post('/missing-skills', { file_id: fileId, target_role: targetRole })

// JD Match
export const matchJD         = (fileId, jobDescription) => api.post('/jd-match', { file_id: fileId, job_description: jobDescription })

// Career
export const getCareerAnalysis   = (fileId, targetRole) => api.post('/career-analysis', { file_id: fileId, target_role: targetRole })
export const getCareerReadiness  = (fileId) => api.post('/career-readiness', { file_id: fileId })
export const analyzeProjects     = (fileId) => api.post('/analyze-projects', { file_id: fileId })

// AI Rewriter
export const rewriteBullets  = (bullets) => api.post('/rewrite-bullets', { bullets })
export const rewriteBullet   = (text)    => api.post('/rewrite-bullet', { text })

// GitHub / LinkedIn
export const analyzeGitHub   = (github_url) => api.post('/github', { github_url })
export const analyzeLinkedIn = (linkedin_url, profile_data) => api.post('/linkedin', { linkedin_url, profile_data })

// Report
export const generateReport  = (fileId, targetRole, jdText) => api.post('/report/generate', { file_id: fileId, target_role: targetRole, jd_text: jdText })
export const downloadReport  = (reportId) => `/api/report/download/${reportId}`

// Suggestions (separate from upload to avoid rate limiting)
export const getSuggestions = (fileId) => api.post('/suggestions', { file_id: fileId })
