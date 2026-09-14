import React from 'react'
import Flowchart, { NodoDiagrama } from './Flowchart'
import type { PropsTipo } from './tipos'

export interface SpecFlowchartMatch {
  /** Cada fragmento de pseudocodigo que hay que emparejar. */
  fragmentos: { etiqueta: string; codigo: string }[]
  /** Los diagramas, que se muestran etiquetados A, B, C... */
  diagramas: { nodos: NodoDiagrama[]; descripcion?: string }[]
  ayuda?: string
}

const LETRAS = 'ABCDEFGH'.split('')

/**
 * Emparejar cada fragmento de pseudocodigo con el diagrama que dice lo mismo.
 *
 * El ejercicio que hace explicita la equivalencia entre las dos notaciones,
 * que es justo lo que enseña la leccion: el mismo algoritmo escrito de dos
 * formas.
 */
const FlowchartMatch: React.FC<PropsTipo<SpecFlowchartMatch>> = ({
  spec,
  valor,
  onChange,
  detalle,
  deshabilitado,
}) => {
  const fragmentos = spec.fragmentos || []
  const diagramas = spec.diagramas || []
  const asignaciones = (valor.asignaciones as (number | null)[]) || fragmentos.map(() => null)

  const elegir = (fragmento: number, opcion: string) => {
    const copia = [...asignaciones]
    copia[fragmento] = opcion === '' ? null : Number(opcion)
    onChange({ asignaciones: copia })
  }

  return (
    <div className="mt-3">
      {spec.ayuda && <p className="text-xs text-slate-500">{spec.ayuda}</p>}

      <div className="mt-3 flex flex-wrap gap-6">
        {diagramas.map((diagrama, i) => (
          <div key={i} className="min-w-[16rem]">
            <p className="text-xs font-semibold text-slate-500 uppercase tracking-wide">
              Diagrama {LETRAS[i]}
            </p>
            <Flowchart
              nodos={diagrama.nodos}
              descripcion={diagrama.descripcion || `Diagrama ${LETRAS[i]}`}
            />
          </div>
        ))}
      </div>

      <div className="mt-4 space-y-3">
        {fragmentos.map((fragmento, i) => (
          <div
            key={fragmento.etiqueta}
            className={`rounded-lg border p-3 ${
              detalle?.posicion === i ? 'border-rose-400 bg-rose-50' : 'border-slate-200'
            }`}
          >
            <pre className="text-xs bg-slate-900 text-slate-100 rounded p-2 overflow-x-auto">
              <code>{fragmento.codigo}</code>
            </pre>
            <label className="mt-2 flex items-center gap-2 text-sm">
              <span className="text-slate-600">{fragmento.etiqueta} se corresponde con el</span>
              <select
                aria-label={fragmento.etiqueta}
                value={asignaciones[i] ?? ''}
                disabled={deshabilitado}
                onChange={(e) => elegir(i, e.target.value)}
                className="rounded border border-slate-300 px-2 py-1 text-sm disabled:bg-slate-100"
              >
                <option value="">elige...</option>
                {diagramas.map((_, k) => (
                  <option key={k} value={k}>
                    Diagrama {LETRAS[k]}
                  </option>
                ))}
              </select>
            </label>
          </div>
        ))}
      </div>
    </div>
  )
}

export default FlowchartMatch
