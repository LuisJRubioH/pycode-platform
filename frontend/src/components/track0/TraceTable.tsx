import React from 'react'
import Flowchart from './Flowchart'
import type { PropsTipo, SpecTraceTable } from './tipos'

/**
 * Tabla de traza: el tipo central de Track 0.
 *
 * El alumno sigue el algoritmo a mano y anota cuánto vale cada variable en
 * cada paso. La celda que el backend señala como primera incorrecta se marca
 * en rojo, pero nunca se rellena con el valor correcto: la gracia es volver a
 * trazar, no copiar.
 *
 * Una fila puede traer celdas `fijas` (ya rellenas en el enunciado, como el
 * estado inicial); esas se pintan como texto y no se envían a edición.
 */
const TraceTable: React.FC<PropsTipo<SpecTraceTable>> = ({
  spec,
  valor,
  onChange,
  detalle,
  deshabilitado,
}) => {
  const columnas = spec.columnas || []
  const filas = spec.filas || []

  // La respuesta viaja como matriz de strings, en el orden de `columnas`, y
  // lleva TAMBIEN las celdas que el enunciado ya daba hechas: el backend
  // corrige la tabla entera, asi que si las fijas fueran vacias una respuesta
  // correcta no aprobaria nunca.
  const celdas =
    (valor.celdas as string[][]) ||
    filas.map((fila) => columnas.map((_, c) => fila.fijas?.[c] ?? ''))

  const escribir = (f: number, c: number, texto: string) => {
    const copia = celdas.map((fila) => [...fila])
    copia[f][c] = texto
    onChange({ celdas: copia })
  }

  return (
    <div className="mt-3">
      {spec.pseudocodigo && (
        <pre className="text-xs bg-slate-900 text-slate-100 rounded-lg p-3 overflow-x-auto">
          <code>{spec.pseudocodigo}</code>
        </pre>
      )}
      {spec.nodos && (
        /* Traza de un diagrama (leccion 6): se dibuja encima de la tabla. */
        <Flowchart nodos={spec.nodos} descripcion="Diagrama que hay que trazar" />
      )}
      {spec.ayuda && <p className="text-xs text-slate-500 mt-2">{spec.ayuda}</p>}

      <div className="mt-3 overflow-x-auto">
        <table className="text-sm border-collapse min-w-full">
          <thead>
            <tr>
              <th className="text-left text-xs font-semibold text-slate-500 px-2 py-1 border-b border-slate-200">
                Paso
              </th>
              {columnas.map((columna) => (
                <th
                  key={columna}
                  className="text-left text-xs font-semibold text-slate-500 px-2 py-1 border-b border-slate-200"
                >
                  {columna}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filas.map((fila, f) => (
              <tr key={fila.etiqueta}>
                <td className="px-2 py-1 text-xs text-slate-600 whitespace-nowrap border-b border-slate-100">
                  {fila.etiqueta}
                </td>
                {columnas.map((columna, c) => {
                  const fijada = fila.fijas?.[c]
                  const fallo = detalle?.fila === f && detalle?.columna === c
                  if (fijada != null) {
                    return (
                      <td
                        key={columna}
                        className="px-2 py-1 border-b border-slate-100 text-slate-500 text-xs"
                      >
                        {fijada}
                      </td>
                    )
                  }
                  return (
                    <td key={columna} className="px-2 py-1 border-b border-slate-100">
                      <input
                        type="text"
                        aria-label={`${fila.etiqueta}, ${columna}`}
                        value={celdas[f]?.[c] ?? ''}
                        onChange={(e) => escribir(f, c, e.target.value)}
                        disabled={deshabilitado}
                        className={`w-20 rounded border px-2 py-1 text-sm ${
                          fallo
                            ? 'border-rose-400 bg-rose-50 text-rose-900'
                            : 'border-slate-300'
                        } disabled:bg-slate-100`}
                      />
                    </td>
                  )
                })}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default TraceTable
