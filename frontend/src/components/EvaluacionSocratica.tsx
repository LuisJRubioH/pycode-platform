import React from 'react'
import { CheckCircle2, AlertTriangle, Lightbulb, ClipboardCheck } from 'lucide-react'
import Markdown from './Markdown'
import {
  partirVeredicto,
  tonoDeNota,
  ETIQUETA_TONO,
  type BloqueVeredicto,
  type TipoBloque,
  type Tono,
} from './evaluacionSecciones'

interface Props {
  raw: string
  logicScore: number | null
  generalScore: number | null
  /** Historial: las notas ya salen en la cabecera plegable, no se repiten. */
  compacto?: boolean
}

// Tailwind no ve las clases construidas por concatenacion, asi que cada tono
// lleva sus clases completas escritas.
const COLOR_TONO: Record<Tono, { texto: string; barra: string; fondo: string; borde: string }> = {
  excelente: {
    texto: 'text-emerald-700',
    barra: 'bg-emerald-500',
    fondo: 'bg-emerald-50',
    borde: 'border-emerald-200',
  },
  bien: {
    texto: 'text-sky-700',
    barra: 'bg-sky-500',
    fondo: 'bg-sky-50',
    borde: 'border-sky-200',
  },
  regular: {
    texto: 'text-amber-700',
    barra: 'bg-amber-500',
    fondo: 'bg-amber-50',
    borde: 'border-amber-200',
  },
  flojo: {
    texto: 'text-rose-700',
    barra: 'bg-rose-500',
    fondo: 'bg-rose-50',
    borde: 'border-rose-200',
  },
  'sin-nota': {
    texto: 'text-slate-500',
    barra: 'bg-slate-300',
    fondo: 'bg-slate-50',
    borde: 'border-slate-200',
  },
}

const TarjetaNota: React.FC<{ etiqueta: string; nota: number | null }> = ({
  etiqueta,
  nota,
}) => {
  const tono = tonoDeNota(nota)
  const color = COLOR_TONO[tono]
  return (
    <div className={`rounded-lg border p-3 ${color.fondo} ${color.borde}`}>
      <div className="flex items-baseline justify-between gap-2">
        <p className="text-xs uppercase tracking-wide text-slate-500">{etiqueta}</p>
        <span className={`text-[11px] font-semibold ${color.texto}`}>
          {ETIQUETA_TONO[tono]}
        </span>
      </div>
      <p className={`text-3xl font-bold leading-tight ${color.texto}`}>
        {nota ?? '—'}
        <span className="text-sm font-normal text-slate-500"> /100</span>
      </p>
      {/* La barra repite la nota de forma no numerica: de un vistazo se ve
          cuanto falta sin leer la cifra. */}
      <div
        className="mt-2 h-1.5 w-full overflow-hidden rounded-full bg-white/70"
        role="img"
        aria-label={nota === null ? 'Sin nota' : `${nota} de 100`}
      >
        <div
          className={`h-full rounded-full ${color.barra}`}
          style={{ width: `${nota ?? 0}%` }}
        />
      </div>
    </div>
  )
}

const ESTILO_BLOQUE: Record<
  Exclude<TipoBloque, 'normal' | 'analisis' | 'calificacion'>,
  { icono: typeof CheckCircle2; titulo: string; texto: string; fondo: string; borde: string }
> = {
  fuertes: {
    icono: CheckCircle2,
    titulo: 'Lo que ya hiciste bien',
    texto: 'text-emerald-800',
    fondo: 'bg-emerald-50',
    borde: 'border-emerald-200',
  },
  mejora: {
    icono: AlertTriangle,
    titulo: 'Qué mejorar',
    texto: 'text-amber-800',
    fondo: 'bg-amber-50',
    borde: 'border-amber-200',
  },
  recomendaciones: {
    icono: Lightbulb,
    titulo: 'Para pensar',
    texto: 'text-indigo-800',
    fondo: 'bg-indigo-50',
    borde: 'border-indigo-200',
  },
}

// Tailwind Typography no tiene `prose-xs`: el escalon mas pequeno es
// `prose-sm`, y es el que usa el resto de la plataforma.
const PROSA =
  'prose prose-sm prose-slate max-w-none prose-p:my-1.5 prose-li:my-0.5 prose-ul:my-1.5 prose-ol:my-1.5'

const Bloque: React.FC<{ bloque: BloqueVeredicto }> = ({ bloque }) => {
  const prosa = PROSA

  if (bloque.tipo === 'normal' || bloque.tipo === 'analisis') {
    return <Markdown className={prosa}>{bloque.cuerpo}</Markdown>
  }

  if (bloque.tipo === 'calificacion') {
    // Solo se llega aqui cuando alguna nota no se pudo extraer: el desglose en
    // texto es entonces la unica forma de verla, asi que no se descarta.
    return (
      <div className="rounded-lg border border-slate-200 bg-slate-50 p-3">
        <div className="mb-1 flex items-center gap-2 text-slate-700">
          <ClipboardCheck className="h-4 w-4 flex-shrink-0" />
          <h3 className="text-xs font-semibold uppercase tracking-wide">Calificación</h3>
        </div>
        <Markdown className={prosa}>{bloque.cuerpo}</Markdown>
      </div>
    )
  }

  const estilo = ESTILO_BLOQUE[bloque.tipo]
  const Icono = estilo.icono
  return (
    <section className={`rounded-lg border ${estilo.borde} ${estilo.fondo} p-3`}>
      <div className={`mb-1.5 flex items-center gap-2 ${estilo.texto}`}>
        <Icono className="h-4 w-4 flex-shrink-0" />
        <h3 className="text-xs font-semibold uppercase tracking-wide">{estilo.titulo}</h3>
      </div>
      <Markdown className={prosa}>{bloque.cuerpo}</Markdown>
    </section>
  )
}

/**
 * Retroalimentacion del tutor con forma: las dos notas como fichas de color y
 * cada bloque del veredicto en su tarjeta.
 *
 * Antes esto era un `<pre>` con el Markdown en crudo: el alumno leia los
 * asteriscos y las almohadillas, y lo que mas importa (que esta bien, que hay
 * que arreglar) tenia exactamente el mismo peso visual que el resto.
 */
const EvaluacionSocratica: React.FC<Props> = ({
  raw,
  logicScore,
  generalScore,
  compacto = false,
}) => {
  const bloques = React.useMemo(() => partirVeredicto(raw), [raw])
  const notasCompletas = logicScore !== null && generalScore !== null

  // El desglose en texto de la calificacion solo se muestra si alguna nota no
  // se pudo extraer: con las dos fichas delante es repetir lo mismo.
  const visibles = bloques.filter(
    (b) => !(b.tipo === 'calificacion' && notasCompletas)
  )

  return (
    <div className="space-y-3">
      {/* En el historial las notas ya van en la cabecera de cada intento. */}
      {!compacto && (
        <div className="grid gap-3 sm:grid-cols-2">
          <TarjetaNota etiqueta="Lógica" nota={logicScore} />
          <TarjetaNota etiqueta="Solución general" nota={generalScore} />
        </div>
      )}

      {visibles.map((bloque, i) => (
        <Bloque key={`${bloque.tipo}-${i}`} bloque={bloque} />
      ))}
    </div>
  )
}

export default EvaluacionSocratica
