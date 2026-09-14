import React from 'react'
import { AlertTriangle, ListChecks, Target } from 'lucide-react'
import Markdown from './Markdown'
import { type Seccion, type TipoSeccion, useSeccionVisible } from './lessonSecciones'

const ESTILO: Record<TipoSeccion, { caja: string; icono: React.ReactNode }> = {
  objetivo: {
    caja: 'rounded-xl border-l-4 border-primary-500 bg-primary-50/70 px-5 py-1',
    icono: <Target className="h-5 w-5 text-primary-600" aria-hidden />,
  },
  errores: {
    caja: 'rounded-xl border-l-4 border-rose-400 bg-rose-50/70 px-5 py-1',
    icono: <AlertTriangle className="h-5 w-5 text-rose-600" aria-hidden />,
  },
  resumen: {
    caja: 'rounded-xl border-l-4 border-emerald-500 bg-emerald-50/70 px-5 py-1',
    icono: <ListChecks className="h-5 w-5 text-emerald-600" aria-hidden />,
  },
  normal: { caja: '', icono: null },
}

/** El contenido de la leccion, una `<section>` con ancla por cada `##`. */
export const LessonSections: React.FC<{ intro: string; secciones: Seccion[] }> = ({
  intro,
  secciones,
}) => (
  <div className="mx-auto max-w-prose space-y-10">
    {intro && <Markdown>{intro}</Markdown>}
    {secciones.map((s) => (
      <section
        key={s.id}
        id={s.id}
        data-tipo={s.tipo}
        aria-labelledby={`${s.id}-titulo`}
        className={`scroll-mt-6 ${ESTILO[s.tipo].caja}`}
      >
        <h2
          id={`${s.id}-titulo`}
          className="mt-5 mb-3 flex items-center gap-2 text-2xl font-bold text-slate-900"
        >
          {ESTILO[s.tipo].icono}
          {s.titulo}
        </h2>
        <Markdown className="prose prose-slate">{s.cuerpo}</Markdown>
      </section>
    ))}
  </div>
)

interface EntradaIndice {
  id: string
  titulo: string
}

/** Indice con anclas: lateral y fijo en pantallas anchas, desplegable en moviles. */
export const LessonIndex: React.FC<{ entradas: EntradaIndice[] }> = ({ entradas }) => {
  const actual = useSeccionVisible(entradas.map((e) => e.id))

  const lista = (
    <ol className="space-y-1 text-sm">
      {entradas.map((e) => (
        <li key={e.id}>
          <a
            href={`#${e.id}`}
            aria-current={actual === e.id ? 'location' : undefined}
            className={`block rounded-md border-l-2 px-3 py-1.5 transition-colors ${
              actual === e.id
                ? 'border-primary-600 bg-primary-50 font-medium text-primary-800'
                : 'border-transparent text-slate-600 hover:border-slate-300 hover:text-slate-900'
            }`}
          >
            {e.titulo}
          </a>
        </li>
      ))}
    </ol>
  )

  return (
    <nav aria-label="Indice de la leccion">
      <details className="card p-4 lg:hidden">
        <summary className="cursor-pointer text-sm font-semibold text-slate-800">
          En esta leccion ({entradas.length} secciones)
        </summary>
        <div className="mt-3">{lista}</div>
      </details>
      <div className="hidden lg:block sticky top-6">
        <p className="mb-2 px-3 text-xs font-semibold uppercase tracking-wide text-slate-500">
          En esta leccion
        </p>
        {lista}
      </div>
    </nav>
  )
}
