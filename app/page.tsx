import FileUpload from '@/components/FileUpload'
import Image from 'next/image'

export default function Home() {
  return (
    <main className='flex flex-col justify-center items-center gap-5 bg-slate-800 text-white w-full min-h-screen'>
      <h1>PDF - summarizer</h1>
      <p>
        A app where you can easily summarize PDFs
      </p>
      <FileUpload/>
    </main>
  )
}
