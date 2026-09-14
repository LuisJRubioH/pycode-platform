import React from 'react'
import type { PropsTipo, SpecPredictOutput } from './tipos'

/**
 * Qué escribe el algoritmo: el alumno anota la salida, una línea por Escribir.
 *
 * La comparación del backend normaliza espacios y líneas vacías del final, así
 * que aquí no hace falta pelearse con el formato.
 */
const PredictOutput: React.FC<PropsTipo<SpecPredictOutput>> = ({
  spec,
  valor,
  onChange,
  detalle,
  deshabilitado,
}) => {
  const salida = (valor.salida as string) ?? ''

  return (
    <div className="mt-3">
      {spec.pseudocodigo && (
        <pre className="text-xs bg-slate-900 text-slate-100 rounded-lg p-3 overflow-x-auto">
          <code>{spec.pseudocodigo}</code>
        </pre>
      )}
      {spec.ayuda && <p className="text-xs text-slate-500 mt-2">{spec.ayuda}</p>}

      <label className="block mt-3">
        <span className="text-xs font-semibold text-slate-500">
          Lo que aparece en pantalla (una línea por cada Escribir)
        </span>
        <textarea
          aria-label="Salida del algoritmo"
          value={salida}
          onChange={(e) => onChange({ salida: e.target.value })}
          disabled={deshabilitado}
          rows={5}
          className={`mt-1 w-full rounded-lg border px-3 py-2 font-mono text-sm ${
            detalle?.linea != null ? 'border-rose-400 bg-rose-50' : 'border-slate-300'
          } disabled:bg-slate-100`}
        />
      </label>
      {detalle?.linea != null && (
        <p className="text-xs text-rose-700">
          Revisa la línea {detalle.linea + 1} de tu respuesta.
        </p>
      )}
    </div>
  )
}

export default PredictOutput
