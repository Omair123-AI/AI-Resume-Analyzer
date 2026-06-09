import { Lightbulb, Zap, Target } from 'lucide-react'

export default function Suggestions({ data = {} }) {
  const { overall_feedback, quick_wins = [], priority_actions = [], section_tips = {} } = data
  return (
    <div className="card">
      <div className="flex items-center gap-2 mb-4">
        <Lightbulb className="text-yellow-400 w-5 h-5" />
        <h3 className="section-title mb-0">AI Suggestions</h3>
      </div>
      {overall_feedback && <p className="text-slate-300 text-sm mb-4 leading-relaxed">{overall_feedback}</p>}
      {quick_wins.length > 0 && (
        <div className="mb-4">
          <div className="flex items-center gap-1.5 mb-2"><Zap className="w-4 h-4 text-amber-400"/><p className="text-sm font-semibold text-amber-400">Quick Wins</p></div>
          <ul className="space-y-1.5">
            {quick_wins.map((w,i) => <li key={i} className="text-sm text-slate-300 flex gap-2"><span className="text-amber-400 mt-0.5">•</span>{w}</li>)}
          </ul>
        </div>
      )}
      {priority_actions.length > 0 && (
        <div className="mb-4">
          <div className="flex items-center gap-1.5 mb-2"><Target className="w-4 h-4 text-indigo-400"/><p className="text-sm font-semibold text-indigo-400">Priority Actions</p></div>
          <ol className="space-y-1.5">
            {priority_actions.map((a,i) => <li key={i} className="text-sm text-slate-300 flex gap-2"><span className="text-indigo-400 font-bold">{i+1}.</span>{a}</li>)}
          </ol>
        </div>
      )}
      {Object.keys(section_tips).length > 0 && (
        <div>
          <p className="text-sm font-semibold text-slate-400 mb-2">Section Tips</p>
          <div className="space-y-2">
            {Object.entries(section_tips).map(([k,v]) => (
              <div key={k} className="bg-slate-800 rounded-xl px-3 py-2">
                <span className="text-xs font-bold text-indigo-400 capitalize">{k}: </span>
                <span className="text-xs text-slate-300">{v}</span>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  )
}
