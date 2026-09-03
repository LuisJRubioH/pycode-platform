import React, { useRef, useState } from 'react'
import { Check, Copy } from 'lucide-react'

/**
 * Reemplaza el `<pre>` que genera react-markdown para añadirle un boton de
 * copiar. El texto se lee del DOM con una ref en vez de recorrer el AST:
 * rehype-highlight envuelve cada token en `<span>`, asi que reconstruir el
 * codigo desde `children` obligaria a caminar el arbol. Usamos `textContent`
 * y no `innerText` porque dentro de un `<pre>` dan el mismo resultado y
 * `textContent` no depende del layout (ni falta en jsdom).
 */
const MarkdownCodeBlock: React.FC<React.HTMLAttributes<HTMLPreElement>> = ({
  children,
  ...props
}) => {
  const preRef = useRef<HTMLPreElement>(null)
  const [copied, setCopied] = useState(false)

  const copy = async () => {
    const code = preRef.current?.textContent ?? ''
    try {
      await navigator.clipboard.writeText(code)
      setCopied(true)
      window.setTimeout(() => setCopied(false), 2000)
    } catch (err) {
      console.error('No se pudo copiar el codigo:', err)
    }
  }

  return (
    <div className="group relative not-prose my-6">
      <pre
        ref={preRef}
        {...props}
        className="overflow-x-auto rounded-lg bg-slate-900 p-4 text-sm leading-relaxed text-slate-100"
      >
        {children}
      </pre>
      <button
        onClick={copy}
        aria-label={copied ? 'Codigo copiado' : 'Copiar codigo'}
        title={copied ? 'Copiado' : 'Copiar'}
        className="absolute right-2 top-2 rounded-md border border-slate-600 bg-slate-800/90 p-1.5 text-slate-300 opacity-0 transition hover:bg-slate-700 hover:text-white focus:opacity-100 focus:outline-none focus:ring-2 focus:ring-primary-500 group-hover:opacity-100"
      >
        {copied ? (
          <Check className="h-4 w-4 text-emerald-400" />
        ) : (
          <Copy className="h-4 w-4" />
        )}
      </button>
    </div>
  )
}

export default MarkdownCodeBlock
