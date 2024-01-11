import type { Metadata } from 'next'

import { Inter } from 'next/font/google'
import './globals.css'
import { Toaster } from 'react-hot-toast'

const inter = Inter({ subsets: ['latin'] })

export const metadata: Metadata = {
  title: 'PDF-Summarizer',
  description: 'A app where you can easily summarize PDFs',
}

export default function RootLayout({
  children,
}: {
  children: React.ReactNode
}) {
  return (
    <html lang="en">
      <body className={inter.className}>
      <Toaster position="top-center" />
        {children}</body>
    </html>
  )
}
