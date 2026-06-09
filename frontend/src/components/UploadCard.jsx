import { useDropzone } from 'react-dropzone'
import { UploadCloud, FileText, CheckCircle } from 'lucide-react'
import { motion } from 'framer-motion'

export default function UploadCard({ onFile, file }) {
  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop: files => files[0] && onFile(files[0]),
    accept: { 'application/pdf': ['.pdf'], 'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx'] },
    maxFiles: 1,
  })

  return (
    <motion.div initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }}
      {...getRootProps()}
      className={`card cursor-pointer border-2 border-dashed transition-all duration-300 text-center py-12
        ${isDragActive ? 'border-indigo-500 bg-indigo-500/10' : file ? 'border-emerald-500 bg-emerald-500/5' : 'border-slate-700 hover:border-indigo-500/60'}`}>
      <input {...getInputProps()} />
      {file ? (
        <>
          <CheckCircle className="w-12 h-12 text-emerald-400 mx-auto mb-3" />
          <p className="text-emerald-400 font-semibold text-lg">{file.name}</p>
          <p className="text-slate-400 text-sm mt-1">Click or drop to replace</p>
        </>
      ) : (
        <>
          <UploadCloud className={`w-12 h-12 mx-auto mb-3 ${isDragActive ? 'text-indigo-400' : 'text-slate-500'}`} />
          <p className="text-white font-semibold text-lg">{isDragActive ? 'Drop it here!' : 'Upload Your Resume'}</p>
          <p className="text-slate-400 text-sm mt-1">PDF or DOCX · Max 16MB</p>
        </>
      )}
    </motion.div>
  )
}
