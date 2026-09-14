import React from 'react'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import resaltarCodigo from './resaltado'
// Tema del resaltado. Se empaqueta con el bundle: no sale ninguna peticion
// a un CDN, asi que no hay que tocar la CSP.
import 'highlight.js/styles/github-dark.css'
import MarkdownCodeBlock from './MarkdownCodeBlock'

// Las tablas de markdown no traen scroll propio: al estrechar la columna
// pueden desbordar la tarjeta y hacer que scrollee la pagina entera. Se
// envuelven para que scrollee solo la tabla.
const COMPONENTES = {
  pre: MarkdownCodeBlock,
  table: ({ children, ...props }: React.HTMLAttributes<HTMLTableElement>) => (
    <div className="overflow-x-auto">
      <table {...props}>{children}</table>
    </div>
  ),
}

interface MarkdownProps {
  children: string
  /** Clases del contenedor. Por defecto, la tipografia de las lecciones. */
  className?: string
}

/**
 * Markdown con la misma configuracion en toda la plataforma: GFM (tablas,
 * listas de tareas), resaltado de codigo y boton de copiar en los bloques.
 * react-markdown no interpreta HTML crudo, asi que el contenido no puede
 * inyectar etiquetas.
 */
// El plugin de tipografia pinta el codigo inline entre backticks con
// `code::before/::after`: el alumno veia `nombre` con las comillas de Markdown
// aunque el texto ya estuviera renderizado. Se quitan y se usa un fondo suave.
// Los bloques de codigo van en `not-prose` (MarkdownCodeBlock) y no les afecta.
const CODIGO_INLINE =
  'prose-code:before:content-none prose-code:after:content-none prose-code:rounded prose-code:bg-slate-100 prose-code:px-1 prose-code:py-0.5 prose-code:font-medium'

const Markdown: React.FC<MarkdownProps> = ({ children, className = 'prose prose-slate' }) => (
  <div className={`${className} ${CODIGO_INLINE}`}>
    <ReactMarkdown
      remarkPlugins={[remarkGfm]}
      rehypePlugins={[resaltarCodigo]}
      components={COMPONENTES}
    >
      {children}
    </ReactMarkdown>
  </div>
)

export default Markdown
