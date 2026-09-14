import React from 'react'
import Flowchart, { NodoDiagrama } from './Flowchart'
import type { PropsTipo } from './tipos'

export interface SpecFlowchartFill {
  pseudocodigo?: string
  /** Los nodos del diagrama; los que tienen `texto: null` son los huecos. */
  nodos: NodoDiagrama[]
  /** Nombre de cada hueco, en orden, para el enunciado y el feedback. */
  huecos: { etiqueta: string }[]
  /** Opciones entre las que elegir, compartidas por todos los huecos. */
  banco: string[]
  ayuda?: string
}

/**
 * Completar los nodos vacios de un diagrama desde un banco de opciones.
 *
 * Lo que hace que este ejercicio enseñe algo es que el diagrama **se redibuja**
 * con lo que el alumno elige: se ve al momento si lo que ha puesto en el rombo
 * es una condicion o un calculo. Por eso el diagrama son datos y no una imagen.
 */
const FlowchartFill: React.FC<PropsTipo<SpecFlowchartFill>> = ({
  spec,
  valor,
  onChange,
  detalle,
  deshabilitado,
}) => {
  const huecos = spec.huecos || []
  const banco = spec.banco || []
  const elegidas = (valor.huecos as (number | null)[]) || huecos.map(() => null)

  // El diagrama se pinta con las elecciones ya puestas: los huecos sin
  // contestar siguen vacios.
  let visto = -1
  const nodos = (spec.nodos || []).map((nodo) => {
    if (nodo.texto !== null) return nodo
    visto += 1
    const elegida = elegidas[visto]
    return { ...nodo, texto: elegida == null ? null : banco[elegida] ?? null }
  })

  const elegir = (hueco: number, opcion: string) => {
    const copia = [...elegidas]
    copia[hueco] = opcion === '' ? null : Number(opcion)
    onChange({ huecos: copia })
  }

  return (
    <div className="mt-3">
      {spec.pseudocodigo && (
        <pre className="text-xs bg-slate-900 text-slate-100 rounded-lg p-3 overflow-x-auto">
          <code>{spec.pseudocodigo}</code>
        </pre>
      )}
      {spec.ayuda && <p className="text-xs text-slate-500 mt-2">{spec.ayuda}</p>}

      <Flowchart
        nodos={nodos}
        resaltado={detalle?.posicion}
        descripcion="Diagrama de flujo con nodos por completar"
      />

      <div className="mt-3 space-y-2">
        {huecos.map((hueco, i) => (
          <label key={hueco.etiqueta} className="flex items-center gap-2 text-sm flex-wrap">
            <span
              className={`min-w-[9rem] ${
                detalle?.posicion === i ? 'text-rose-700 font-semibold' : 'text-slate-600'
              }`}
            >
              {hueco.etiqueta}
            </span>
            <select
              aria-label={hueco.etiqueta}
              value={elegidas[i] ?? ''}
              disabled={deshabilitado}
              onChange={(e) => elegir(i, e.target.value)}
              className={`rounded border px-2 py-1 text-sm font-mono disabled:bg-slate-100 ${
                detalle?.posicion === i ? 'border-rose-400 bg-rose-50' : 'border-slate-300'
              }`}
            >
              <option value="">elige...</option>
              {banco.map((opcion, k) => (
                <option key={opcion} value={k}>
                  {opcion}
                </option>
              ))}
            </select>
          </label>
        ))}
      </div>
    </div>
  )
}

export default FlowchartFill
