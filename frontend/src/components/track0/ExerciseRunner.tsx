import React, { useState } from 'react'
import { CheckCircle2, XCircle } from 'lucide-react'
import { api } from '../../services/api'
import FlowchartFill from './FlowchartFill'
import FlowchartMatch from './FlowchartMatch'
import Mcq from './Mcq'
import PredictOutput from './PredictOutput'
import TraceTable from './TraceTable'
import type { Detalle, PropsTipo, Respuesta } from './tipos'

/**
 * Contenedor de los ejercicios que no se ejecutan (Track 0).
 *
 * Despacha por `exercise_type` y se ocupa de todo lo que no es pintar: mandar
 * la respuesta a `POST /exercises/{id}/check`, enseñar el feedback y avisar
 * cuando el ejercicio queda hecho. Añadir un tipo es escribir su componente y
 * registrarlo en TIPOS: ni la página de lección ni este archivo cambian de
 * forma (regla 5 de docs/TRACK_0.md).
 *
 * La corrección la hace el backend a propósito: la respuesta correcta no viaja
 * al cliente, así que aquí no hay nada que espiar desde las devtools.
 */
// eslint-disable-next-line @typescript-eslint/no-explicit-any
const TIPOS: Record<string, React.FC<PropsTipo<any>>> = {
  trace_table: TraceTable,
  predict_output: PredictOutput,
  mcq: Mcq,
  flowchart_match: FlowchartMatch,
  flowchart_fill: FlowchartFill,
}

interface Props {
  exerciseId: number
  exerciseType: string
  spec: Record<string, unknown> | null
  completed: boolean
  onCompleted?: () => void
}

const ExerciseRunner: React.FC<Props> = ({
  exerciseId,
  exerciseType,
  spec,
  completed,
  onCompleted,
}) => {
  const [valor, setValor] = useState<Respuesta>({})
  const [enviando, setEnviando] = useState(false)
  const [passed, setPassed] = useState(completed)
  // Resultado del ULTIMO intento: `passed` se queda en true para siempre
  // (el ejercicio ya esta hecho), pero un intento nuevo puede fallar.
  const [ultimoOk, setUltimoOk] = useState<boolean | null>(null)
  const [feedback, setFeedback] = useState<string | null>(null)
  const [detalle, setDetalle] = useState<Detalle | undefined>(undefined)
  const [error, setError] = useState('')

  const Componente = TIPOS[exerciseType]
  if (!Componente || !spec) {
    return (
      <p className="mt-3 text-sm text-slate-500">
        Este tipo de ejercicio ({exerciseType}) todavia no esta disponible en tu version.
      </p>
    )
  }

  const comprobar = async () => {
    setEnviando(true)
    setError('')
    try {
      const r = await api.post(`/exercises/${exerciseId}/check`, { respuesta: valor })
      const datos = await r.json()
      setFeedback(datos.feedback ?? null)
      setUltimoOk(Boolean(datos.passed))
      setDetalle(datos.detalle && Object.keys(datos.detalle).length ? datos.detalle : undefined)
      if (datos.passed) {
        setPassed(true)
        onCompleted?.()
      }
    } catch {
      setError('No se pudo comprobar la respuesta. Reintenta en un momento.')
    } finally {
      setEnviando(false)
    }
  }

  return (
    <div>
      <Componente
        spec={spec}
        valor={valor}
        onChange={(v) => {
          setValor(v)
          // Al tocar algo, el error anterior deja de señalar donde señalaba.
          setDetalle(undefined)
        }}
        detalle={detalle}
        deshabilitado={enviando}
      />

      <div className="mt-3 flex flex-wrap items-center gap-3">
        <button onClick={comprobar} disabled={enviando} className="btn-primary">
          {enviando ? 'Comprobando...' : passed ? 'Comprobar de nuevo' : 'Comprobar'}
        </button>
        {feedback && (
          <span
            className={`inline-flex items-center gap-1 text-sm ${
              ultimoOk ? 'text-emerald-700' : 'text-rose-700'
            }`}
          >
            {ultimoOk ? (
              <CheckCircle2 className="h-4 w-4" />
            ) : (
              <XCircle className="h-4 w-4" />
            )}
            {feedback}
          </span>
        )}
      </div>
      {error && <p className="mt-2 text-sm text-rose-700">{error}</p>}
    </div>
  )
}

export default ExerciseRunner
