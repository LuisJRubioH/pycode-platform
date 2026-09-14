import React from 'react'
import type { PropsTipo, SpecMcq } from './tipos'

/**
 * Opción múltiple conceptual. Los distractores son errores reales, así que al
 * fallar el backend devuelve una pista, no la opción correcta.
 */
const Mcq: React.FC<PropsTipo<SpecMcq>> = ({ spec, valor, onChange, deshabilitado }) => {
  const elegida = valor.opcion as number | undefined

  return (
    <div className="mt-3">
      {spec.pseudocodigo && (
        <pre className="text-xs bg-slate-900 text-slate-100 rounded-lg p-3 overflow-x-auto">
          <code>{spec.pseudocodigo}</code>
        </pre>
      )}
      {spec.pregunta && <p className="text-sm text-slate-700 mt-2">{spec.pregunta}</p>}

      <div className="mt-2 space-y-2">
        {(spec.opciones || []).map((opcion, i) => (
          <label
            key={opcion}
            className={`flex items-start gap-2 rounded-lg border px-3 py-2 text-sm cursor-pointer ${
              elegida === i ? 'border-primary-400 bg-primary-50' : 'border-slate-200'
            } ${deshabilitado ? 'cursor-default opacity-70' : ''}`}
          >
            <input
              type="radio"
              className="mt-1"
              checked={elegida === i}
              disabled={deshabilitado}
              onChange={() => onChange({ opcion: i })}
            />
            <span className="text-slate-700">{opcion}</span>
          </label>
        ))}
      </div>
    </div>
  )
}

export default Mcq
