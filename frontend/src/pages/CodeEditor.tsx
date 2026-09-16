import React, { useCallback, useEffect, useMemo, useRef, useState } from 'react'
import { Link, useSearchParams } from 'react-router-dom'
import Editor, { useMonaco } from '@monaco-editor/react'
import {
  Play,
  RotateCcw,
  Save,
  Share2,
  Terminal,
  Settings,
  ClipboardCheck,
  CheckCircle2,
  XCircle,
  TestTube2,
  History,
  X,
  ArrowLeft,
  ChevronLeft,
  ChevronRight,
  BookOpen,
  Square,
  Eraser,
  Trophy,
  Maximize2,
  Minimize2,
  ChevronDown,
  ChevronUp,
} from 'lucide-react'
import {
  runPythonCode,
  runHiddenTests,
  getCodeRunner,
  abortExecution,
  isSandboxInterruption,
} from '../services/codeRunner'
import { api } from '../services/api'
import EvaluationHistoryModal from '../components/EvaluationHistoryModal'
import EvaluacionSocratica from '../components/EvaluacionSocratica'
import Markdown from '../components/Markdown'
import type { HiddenTest, RunStatus, RunTestsResult } from '@/sandbox'

// El modo libre arranca vacio: es para el codigo propio del alumno (ejemplos
// suyos o ejercicios de fuera de la plataforma), no para un ejemplo nuestro.
const INITIAL_CODE = ''

const CLAVE_CONTEXTO_PLEGADO = 'pycode:editor:contexto-plegado'

const PLACEHOLDER_PROBLEM =
  'Describe aqui que deberia hacer tu codigo. Mientras mas claro sea el objetivo, mejor sera la evaluacion del tutor.'

// Detecta si el codigo importa un paquete que Pyodide carga lazy desde el
// CDN (numpy, pandas, scipy, scikit-learn, matplotlib). El primer test que
// los use tarda ~3-5s adicionales mientras se descarga; despues queda
// cacheado en el browser. Usamos esto para mostrar un hint al usuario.
const HEAVY_PYODIDE_PACKAGES = /\b(?:import|from)\s+(numpy|pandas|scipy|sklearn|matplotlib)\b/
const usesHeavyImport = (code: string) => HEAVY_PYODIDE_PACKAGES.test(code)

interface EvaluationVerdict {
  raw: string
  logic_score: number | null
  general_score: number | null
}

interface EvaluationResult {
  id: number
  created_at: string
  verdict: EvaluationVerdict
  model_used: string | null
}

// El editor tiene tres modos, y lo que se carga sale solo de la URL:
//   - libre: `/editor`, vacio, para el codigo propio del alumno.
//   - lección: `/editor?lesson=<id>&exercise=<id>`, con el ejercicio activo
//     en la URL para que sea compartible y recargable. En este modo el
//     editor conoce la lección entera y puede navegar entre ejercicios.
//   - reto: `/editor?challenge=<id>`, con el enunciado y el starter del reto.
interface LessonExercise {
  id: number
  lesson_id: number
  title: string
  description: string | null
  instructions: string | null
  starter_code: string | null
  difficulty: string
  points: number
  order: number
  hints: string[]
  completed: boolean
}

interface LessonContext {
  id: number
  title: string
  track: string
  status: string
  progress: number
  exercises: LessonExercise[]
}

const DIFICULTAD_RETO: Record<string, string> = {
  easy: 'Facil',
  medium: 'Medio',
  hard: 'Dificil',
}

interface ChallengeContext {
  id: number
  title: string
  difficulty: string
  topic: string
  prompt: string
  starter_code: string
  level: number | null
  // Los tres niveles del problema (vacio en retos sueltos).
  levels: { id: number; level: number; difficulty: string; completed: boolean }[]
}

interface LessonSummary {
  id: number
  title: string
  track: string
  // Orden curricular explícito (Lesson.order). No asumimos que el orden de
  // la respuesta de la API sea el del temario.
  order: number
}

const EMPTY_SOLUTION = '# Escribe tu solucion aqui\n'

// Tope de caracteres del panel de salida. Un `print` dentro de un bucle
// infinito genera texto sin fin y el navegador no lo aguanta: se conserva el
// final, que es lo que el alumno necesita ver.
const MAX_CHARS_SALIDA = 50_000
const PINTAR_SALIDA_MS = 100

const ES_MAC = typeof navigator !== 'undefined' && /Mac|iPhone|iPad/.test(navigator.platform)
const ATAJO_EJECUTAR = ES_MAC ? '⌘+Enter' : 'Ctrl+Enter'
const MARCA_RECORTE = '[... salida anterior recortada ...]'
const recortarSalida = (texto: string) => {
  if (texto.length <= MAX_CHARS_SALIDA) return texto
  const cola = texto.slice(-MAX_CHARS_SALIDA)
  // Se corta en un salto de linea para no dejar media linea colgando.
  const salto = cola.indexOf('\n')
  return `${MARCA_RECORTE}\n${salto >= 0 ? cola.slice(salto + 1) : cola}`
}

const CodeEditor: React.FC = () => {
  const [code, setCode] = useState(INITIAL_CODE)
  const [output, setOutput] = useState('')
  // stderr y warnings van aparte del stdout: mezclarlos hacia que un
  // DeprecationWarning pareciera un error del alumno.
  const [errorOutput, setErrorOutput] = useState('')
  const [outputNote, setOutputNote] = useState('')
  const [outputImages, setOutputImages] = useState<string[]>([])
  const [problemDescription, setProblemDescription] = useState('')
  const [expectedOutput, setExpectedOutput] = useState('')
  const [isRunning, setIsRunning] = useState(false)
  const [sandboxStatus, setSandboxStatus] = useState<RunStatus>('idle')
  const [theme, setTheme] = useState('vs-dark')
  const [fontSize, setFontSize] = useState(14)
  const [minimap, setMinimap] = useState(false)
  const [showSettings, setShowSettings] = useState(false)
  // Pantalla completa: el editor se sale del contenedor de `Layout`, que le
  // come navbar + 4rem de padding vertical, y ocupa toda la ventana. Sin esto,
  // en un portatil el area de codigo se quedaba en un par de lineas visibles y
  // no habia ninguna forma de agrandarla.
  const [pantallaCompleta, setPantallaCompleta] = useState(false)
  // El enunciado y la salida esperada ocupan una banda fija que solo hace falta
  // mientras se lee; plegarla devuelve ese espacio al codigo. Se recuerda entre
  // sesiones porque es una preferencia de como trabaja el alumno, no del
  // ejercicio concreto.
  const [contextoPlegado, setContextoPlegado] = useState(() => {
    try {
      return localStorage.getItem(CLAVE_CONTEXTO_PLEGADO) === '1'
    } catch {
      return false
    }
  })
  const [isEvaluating, setIsEvaluating] = useState(false)
  const [evaluation, setEvaluation] = useState<EvaluationResult | null>(null)
  const [evaluationError, setEvaluationError] = useState('')
  const [exerciseId, setExerciseId] = useState<number | null>(null)
  const [isRunningTests, setIsRunningTests] = useState(false)
  const [testsResult, setTestsResult] = useState<RunTestsResult | null>(null)
  const [testsError, setTestsError] = useState('')
  const [showHistory, setShowHistory] = useState(false)
  const [lesson, setLesson] = useState<LessonContext | null>(null)
  const [lessonError, setLessonError] = useState('')
  const [nextLesson, setNextLesson] = useState<LessonSummary | null>(null)

  const [challenge, setChallenge] = useState<ChallengeContext | null>(null)
  const [challengeError, setChallengeError] = useState('')
  // La lista de retos en la que esta el actual, para navegar entre ellos.
  const [retosLista, setRetosLista] = useState<{ id: number; title: string }[]>([])
  // True cuando el reto quedo registrado como resuelto en esta sesion.
  const [retoResuelto, setRetoResuelto] = useState(false)

  const [searchParams, setSearchParams] = useSearchParams()
  const lessonParam = searchParams.get('lesson')
  const exerciseParam = searchParams.get('exercise')
  // Si la URL trae las dos cosas, manda la lección.
  const challengeParam = lessonParam ? null : searchParams.get('challenge')
  // Con que lista se llego al reto (el filtro de la pagina de Retos). Sirve
  // para saber cual es el siguiente sin volver al listado.
  const dificultadParam = searchParams.get('dificultad')

  const monaco = useMonaco()

  // Qué hay cargado en el editor: `leccion:ejercicio`, `reto:<id>` o null en
  // modo libre.
  const loadedExerciseRef = useRef<string | null>(null)

  // El modo libre ya no lee el contexto del tutor de localStorage: la lección
  // lo guarda al pulsar "Practicar", y al entrar despues por "Editor" en el
  // menu aparecia el ultimo ejercicio (enunciado, starter y "Ejecutar tests")
  // sin haber venido de ninguna leccion. El ejercicio llega solo por la URL.

  const fetchLesson = useCallback(async (id: string) => {
    const res = await api.get(`/lessons/${id}`)
    if (!res.ok) throw new Error(`status ${res.status}`)
    return (await res.json()) as LessonContext
  }, [])

  // Pasar de una lección o un reto a "Editor" en el menu no desmonta la pagina
  // (es la misma ruta): sin esto el modo libre heredaba el ejercicio entero.
  useEffect(() => {
    if (lessonParam || challengeParam || loadedExerciseRef.current === null) return
    loadedExerciseRef.current = null
    setCode(INITIAL_CODE)
    setProblemDescription('')
    setExpectedOutput('')
    setExerciseId(null)
    setOutput('')
    setErrorOutput('')
    setOutputNote('')
    setOutputImages([])
    setTestsResult(null)
    setTestsError('')
    setEvaluation(null)
    setEvaluationError('')
  }, [lessonParam, challengeParam])

  // Modo reto (`/editor?challenge=<id>`): enunciado y starter del reto. Se
  // resuelve con "Ejecutar tests": si pasan todos, el reto queda hecho.
  useEffect(() => {
    if (!challengeParam) {
      setChallenge(null)
      setChallengeError('')
      return
    }
    let cancelled = false
    setChallengeError('')
    api
      .get(`/challenges/${challengeParam}`)
      .then(async (res) => {
        if (!res.ok) throw new Error(`status ${res.status}`)
        const data = (await res.json()) as ChallengeContext
        if (cancelled) return
        setChallenge(data)
        const key = `reto:${data.id}`
        if (loadedExerciseRef.current === key) return
        loadedExerciseRef.current = key
        setRetoResuelto(false)
        setCode(data.starter_code || EMPTY_SOLUTION)
        setProblemDescription(`${data.title}\n\n${data.prompt}`.trim())
        setExpectedOutput('')
        setExerciseId(null)
        setOutput('')
        setErrorOutput('')
        setOutputNote('')
        setOutputImages([])
        setTestsResult(null)
        setTestsError('')
        setEvaluation(null)
        setEvaluationError('')
      })
      .catch((err) => {
        console.error('No se pudo cargar el reto:', err)
        if (!cancelled) {
          setChallenge(null)
          setChallengeError('No pudimos cargar este reto.')
        }
      })
    return () => {
      cancelled = true
    }
  }, [challengeParam])

  // La lista de retos del mismo filtro con el que se entro. Se pide una vez
  // por filtro, no por reto: moverse entre retos no vuelve a pedirla.
  useEffect(() => {
    if (!challengeParam) {
      setRetosLista([])
      return
    }
    let cancelled = false
    const url = dificultadParam
      ? `/challenges?difficulty=${dificultadParam}&limit=60`
      : '/challenges/recommended?limit=50'
    api
      .get(url)
      .then(async (res) => {
        if (!res.ok) throw new Error(`status ${res.status}`)
        const data = await res.json()
        if (!cancelled) setRetosLista(data.items || [])
      })
      .catch((err) => {
        // Sin lista no hay Anterior/Siguiente, pero el reto se resuelve igual.
        console.error('No se pudo cargar la lista de retos:', err)
        if (!cancelled) setRetosLista([])
      })
    return () => {
      cancelled = true
    }
  }, [challengeParam, dificultadParam])

  // Carga la lección cuando la URL la referencia.
  useEffect(() => {
    if (!lessonParam) {
      setLesson(null)
      setLessonError('')
      return
    }
    let cancelled = false
    setLessonError('')
    fetchLesson(lessonParam)
      .then((data) => {
        if (!cancelled) setLesson(data)
      })
      .catch((err) => {
        console.error('No se pudo cargar la leccion:', err)
        if (!cancelled) {
          setLesson(null)
          setLessonError('No pudimos cargar la leccion de este ejercicio.')
        }
      })
    return () => {
      cancelled = true
    }
  }, [lessonParam, fetchLesson])

  const exercises = useMemo(() => lesson?.exercises ?? [], [lesson])

  // Índice del ejercicio activo: el de la URL si existe en la lección,
  // si no el primero (así `/editor?lesson=3` abre el ejercicio 1).
  const activeIndex = useMemo(() => {
    if (exercises.length === 0) return -1
    const fromUrl = exercises.findIndex((ex) => String(ex.id) === exerciseParam)
    return fromUrl >= 0 ? fromUrl : 0
  }, [exercises, exerciseParam])

  const activeExercise = activeIndex >= 0 ? exercises[activeIndex] : null

  // Solo reseteamos editor/salida/tests cuando cambia de verdad el ejercicio
  // activo. Refrescar la lección (p.ej. tras aprobar los tests) no debe
  // borrarle el código al alumno.
  useEffect(() => {
    if (!lesson || !activeExercise) return
    const key = `${lesson.id}:${activeExercise.id}`
    if (loadedExerciseRef.current === key) return
    loadedExerciseRef.current = key

    setCode(activeExercise.starter_code || EMPTY_SOLUTION)
    setProblemDescription(
      `${lesson.title}\n\nEjercicio: ${activeExercise.title}\n${
        activeExercise.instructions || activeExercise.description || ''
      }`.trim()
    )
    setExpectedOutput('')
    setExerciseId(activeExercise.id)
    setOutput('')
    setErrorOutput('')
    setOutputNote('')
    setOutputImages([])
    setTestsResult(null)
    setTestsError('')
    setEvaluation(null)
    setEvaluationError('')
  }, [lesson, activeExercise])

  // Donde cae el reto actual dentro de la lista con la que se entro.
  const retoIndex = challenge ? retosLista.findIndex((r) => r.id === challenge.id) : -1
  const retoAnterior = retoIndex > 0 ? retosLista[retoIndex - 1] : null
  const retoSiguiente =
    retoIndex >= 0 && retoIndex < retosLista.length - 1 ? retosLista[retoIndex + 1] : null

  const irAReto = (id: number) => {
    const params: Record<string, string> = { challenge: String(id) }
    if (dificultadParam) params.dificultad = dificultadParam
    setSearchParams(params)
  }

  // Siguiente nivel del mismo problema, para ofrecerlo al resolver el reto.
  const siguienteNivel =
    challenge?.level ? challenge.levels.find((l) => l.level === challenge.level! + 1) ?? null : null

  // Enunciado que viene de la plataforma (lección o reto); null en modo libre.
  const enunciadoFijo = activeExercise
    ? activeExercise.instructions || activeExercise.description || ''
    : challenge
    ? challenge.prompt
    : null

  const isLastExercise = activeIndex >= 0 && activeIndex === exercises.length - 1
  const lessonCompleted = lesson?.status === 'completed'

  // La siguiente lección solo hace falta cuando el alumno terminó la actual
  // y está en el último ejercicio: la pedimos ahí y no en cada carga.
  useEffect(() => {
    if (!lesson || !lessonCompleted || !isLastExercise || nextLesson) return
    let cancelled = false
    api
      .get('/lessons')
      .then(async (res) => {
        if (!res.ok) return
        const all = (await res.json()) as LessonSummary[]
        const sameTrack = all.filter((item) => item.track === lesson.track)
        const pool = [...(sameTrack.length > 0 ? sameTrack : all)].sort(
          (a, b) => (a.order ?? 0) - (b.order ?? 0)
        )
        const idx = pool.findIndex((item) => item.id === lesson.id)
        const candidate = idx >= 0 ? pool[idx + 1] : undefined
        if (!cancelled && candidate) setNextLesson(candidate)
      })
      .catch((err) => console.error('No se pudo buscar la siguiente leccion:', err))
    return () => {
      cancelled = true
    }
  }, [lesson, lessonCompleted, isLastExercise, nextLesson])

  const goToExercise = (index: number) => {
    if (!lesson || index < 0 || index >= exercises.length) return
    setSearchParams({
      lesson: String(lesson.id),
      exercise: String(exercises[index].id),
    })
  }

  const goToLesson = (lessonId: number) => {
    setNextLesson(null)
    setSearchParams({ lesson: String(lessonId) })
  }

  useEffect(() => {
    if (monaco) {
      document.fonts.ready.then(() => {
        monaco.editor.remeasureFonts()
      })
    }
  }, [monaco])

  useEffect(() => {
    const runner = getCodeRunner()
    setSandboxStatus(runner.status)
    return runner.onStatusChange(setSandboxStatus)
  }, [])

  // El panel sigue al final como una terminal: mientras llega salida en vivo y
  // tambien al cortar, que es cuando el aviso de "detenida" queda debajo de
  // todo lo impreso y el alumno no lo veria sin bajar.
  const salidaRef = useRef<HTMLDivElement>(null)
  useEffect(() => {
    if (!salidaRef.current) return
    salidaRef.current.scrollTop = salidaRef.current.scrollHeight
  }, [output, errorOutput])

  const runCode = async () => {
    setOutput('')
    setErrorOutput('')
    setOutputNote('')
    setOutputImages([])
    setIsRunning(true)
    // Salida en vivo: si el codigo no termina, el alumno ve el print repetirse
    // y sabe que tiene que pulsar Detener. Si lo detiene, lo impreso se queda.
    // Las tandas se acumulan y se pintan como mucho cada PINTAR_SALIDA_MS:
    // repintar en cada tanda un `print` dentro de un bucle infinito dejaba el
    // hilo principal segundos sin responder, y con el el boton Detener.
    let pendientes: string[] = []
    let pintado: ReturnType<typeof setTimeout> | undefined
    const pintar = () => {
      pintado = undefined
      const nuevas = pendientes.join('\n')
      pendientes = []
      setOutput((prev) => recortarSalida(prev ? `${prev}\n${nuevas}` : nuevas))
    }
    // La salida en vivo viaja por un canal distinto al del resultado, asi que
    // una tanda rezagada podria llegar despues y duplicarse sobre el stdout
    // final: al terminar se cierra el grifo.
    let enVivo = true
    const onSalida = (lineas: string[]) => {
      if (!enVivo) return
      pendientes.push(...lineas)
      if (pintado === undefined) pintado = setTimeout(pintar, PINTAR_SALIDA_MS)
    }
    try {
      const result = await runPythonCode(code, undefined, onSalida).finally(() => {
        enVivo = false
        // Si se corta, lo que quedaba por pintar tambien se muestra.
        if (pintado !== undefined) {
          clearTimeout(pintado)
          pintar()
        }
      })
      const hasImages = (result.images || []).length > 0
      setOutput(recortarSalida(result.stdout || ''))
      setErrorOutput(result.stderr || (result.ok ? '' : 'Error de ejecución'))
      setOutputImages(result.images || [])
      if (!result.stdout && !result.stderr && result.ok) {
        setOutputNote(hasImages ? '(plot generado)' : '(sin salida)')
      }
    } catch (err) {
      // Un corte del sandbox (bucle infinito o "Detener") trae un mensaje ya
      // pensado para el alumno: no lo disfrazamos de error de Python.
      if (isSandboxInterruption(err)) {
        setErrorOutput(err.message)
      } else {
        const msg = err instanceof Error ? err.message : String(err)
        setErrorOutput(`Error: ${msg}`)
      }
    } finally {
      setIsRunning(false)
    }
  }

  // Ctrl+Enter (⌘+Enter en Mac) ejecuta, como en Jupyter, Colab o VS Code.
  // Se escucha en fase de captura: Monaco usa Ctrl+Enter para "insertar linea
  // debajo" y, si le llegara antes, se tragaria el atajo cuando el foco esta
  // en el editor. El ref evita registrar el listener en cada render sin que
  // se quede con un `code` viejo.
  const atajoRef = useRef({ runCode, isRunning })
  atajoRef.current = { runCode, isRunning }
  useEffect(() => {
    const alPulsar = (e: KeyboardEvent) => {
      if (e.key !== 'Enter' || !(e.ctrlKey || e.metaKey) || e.shiftKey || e.altKey) return
      e.preventDefault()
      e.stopPropagation()
      if (atajoRef.current.isRunning) return
      void atajoRef.current.runCode()
    }
    window.addEventListener('keydown', alPulsar, true)
    return () => window.removeEventListener('keydown', alPulsar, true)
  }, [])

  // Escape sale de pantalla completa. En pantalla completa la navbar queda
  // tapada, asi que sin esto la unica salida seria el boton: si el foco esta
  // dentro de Monaco no es evidente que siga ahi.
  useEffect(() => {
    if (!pantallaCompleta) return
    const alPulsar = (e: KeyboardEvent) => {
      if (e.key === 'Escape') setPantallaCompleta(false)
    }
    window.addEventListener('keydown', alPulsar)
    return () => window.removeEventListener('keydown', alPulsar)
  }, [pantallaCompleta])

  useEffect(() => {
    try {
      localStorage.setItem(CLAVE_CONTEXTO_PLEGADO, contextoPlegado ? '1' : '0')
    } catch {
      // Modo privado o almacenamiento lleno: la preferencia no sobrevive a la
      // recarga, pero la sesion actual funciona igual.
    }
  }, [contextoPlegado])

  const haySalida = Boolean(output || errorOutput || outputNote || outputImages.length > 0)

  // Vacia el panel de salida sin tocar el codigo. Tambien sirve mientras corre:
  // lo que siga imprimiendo se pinta sobre el panel ya vacio.
  const clearOutput = () => {
    setOutput('')
    setErrorOutput('')
    setOutputNote('')
    setOutputImages([])
  }

  const resetCode = () => {
    // En modo lección "reiniciar" vuelve al starter code del ejercicio, no
    // al snippet genérico: el enunciado sigue siendo el mismo.
    if (activeExercise) {
      setCode(activeExercise.starter_code || EMPTY_SOLUTION)
    } else {
      setCode(INITIAL_CODE)
      setProblemDescription('')
      setExpectedOutput('')
    }
    setOutput('')
    setErrorOutput('')
    setOutputNote('')
    setOutputImages([])
    setEvaluation(null)
    setEvaluationError('')
    setTestsResult(null)
    setTestsError('')
  }

  const saveCode = () => {
    const blob = new Blob([code], { type: 'text/x-python' })
    const url = URL.createObjectURL(blob)
    const anchor = document.createElement('a')
    anchor.href = url
    anchor.download = 'script.py'
    document.body.appendChild(anchor)
    anchor.click()
    document.body.removeChild(anchor)
    URL.revokeObjectURL(url)
  }

  const shareCode = async () => {
    try {
      if (navigator.clipboard) {
        await navigator.clipboard.writeText(code)
        alert('Codigo copiado al portapapeles')
      } else {
        alert('Tu navegador no soporta esta accion')
      }
    } catch (error) {
      alert('Error al copiar el codigo')
      console.error(error)
    }
  }

  // Los tests ocultos existen para ejercicios de leccion y para retos: mismo
  // runner, distinto endpoint y distinta forma de registrar el resultado.
  const testsUrl =
    exerciseId !== null
      ? `/exercises/${exerciseId}/hidden-tests`
      : challenge
      ? `/challenges/${challenge.id}/hidden-tests`
      : null

  const registrarReto = async (reto: ChallengeContext, passed: number, total: number) => {
    const res = await api.post(`/challenges/${reto.id}/complete`, {
      passed_tests: passed,
      total_tests: total,
    })
    if (!res.ok) {
      const data = await res.json().catch(() => ({}))
      setTestsError(
        typeof data.detail === 'string' ? data.detail : 'No se pudo registrar el reto como resuelto.'
      )
      return
    }
    setRetoResuelto(true)
    // Refresca la progresion de niveles para ofrecer el siguiente.
    const detalle = await api.get(`/challenges/${reto.id}`)
    if (detalle.ok) setChallenge((await detalle.json()) as ChallengeContext)
  }

  const runTests = async () => {
    if (testsUrl === null) return
    setTestsError('')
    setTestsResult(null)
    setIsRunningTests(true)
    try {
      const res = await api.get(testsUrl)
      if (!res.ok) {
        setTestsError('No se pudieron obtener los tests del ejercicio.')
        return
      }
      const body = (await res.json()) as { tests: HiddenTest[] }
      if (body.tests.length === 0) {
        setTestsError('Este ejercicio aún no tiene tests configurados.')
        return
      }
      const result = await runHiddenTests(code, body.tests)
      setTestsResult(result)
      // Si todos los tests pasan, registra la submission: el backend marca
      // el ejercicio como completado (result=success) y suma los puntos.
      if (result.total > 0 && result.passed === result.total && exerciseId === null && challenge) {
        await registrarReto(challenge, result.passed, result.total)
      } else if (result.total > 0 && result.passed === result.total) {
        try {
          await api.post(`/exercises/${exerciseId}/submit`, {
            exercise_id: exerciseId,
            code,
            success: true,
            passed_tests: result.passed,
            total_tests: result.total,
          })
          // Refresca la lección para que el estado (ejercicio hecho, % de la
          // lección) se vea sin recargar la página.
          if (lessonParam) {
            const refreshed = await fetchLesson(lessonParam)
            setLesson(refreshed)
          }
        } catch (submitErr) {
          console.error('No se pudo registrar la completitud:', submitErr)
        }
      }
    } catch (err) {
      if (isSandboxInterruption(err)) {
        setTestsError(err.message)
      } else {
        console.error('Error al ejecutar tests:', err)
        setTestsError('Error al ejecutar los tests en el sandbox.')
      }
    } finally {
      setIsRunningTests(false)
    }
  }

  const evaluateCode = async () => {
    const trimmedDesc = problemDescription.trim()
    if (trimmedDesc.length < 10 || trimmedDesc === PLACEHOLDER_PROBLEM.trim()) {
      setEvaluationError(
        'Escribe primero qué intenta hacer tu código (mínimo 10 caracteres). El evaluador necesita el enunciado.'
      )
      return
    }
    setEvaluationError('')
    setIsEvaluating(true)
    setEvaluation(null)
    try {
      const res = await api.post('/tutor/evaluate', {
        problem_description: trimmedDesc,
        code,
        expected_output: expectedOutput.trim() || undefined,
        actual_output:
          [output, errorOutput].filter(Boolean).join('\n').trim() ||
          undefined,
      })
      if (!res.ok) {
        const data = await res.json().catch(() => ({}))
        const detail = typeof data.detail === 'string' ? data.detail : 'No se pudo evaluar el código.'
        setEvaluationError(detail)
        return
      }
      const data = (await res.json()) as EvaluationResult
      setEvaluation(data)
    } catch (err) {
      console.error('Error al evaluar:', err)
      setEvaluationError('Error de red al contactar al evaluador.')
    } finally {
      setIsEvaluating(false)
    }
  }

  return (
    <div
      className={
        pantallaCompleta
          ? 'fixed inset-0 z-40 flex flex-col overflow-y-auto bg-white'
          : // Solo a partir de lg se ata el alto a la ventana. Por debajo no
            // caben las dos columnas ni con calzador: se apilan y la pagina
            // scrollea, en vez de repartir una pantalla de movil entre barra,
            // enunciado, editor y salida y dejarlos todos inservibles.
            'flex flex-col lg:h-[calc(100vh-8rem)] lg:min-h-[38rem]'
      }
    >
      <div className="bg-white border-b border-slate-200 p-3 sm:p-4 flex flex-wrap items-center justify-between gap-3">
        <div className="flex min-w-0 items-center gap-3">
          <h1 className="text-xl font-semibold text-slate-900">Editor de Codigo</h1>
          <div
            className={`w-2 h-2 rounded-full ${
              sandboxStatus === 'ready' || sandboxStatus === 'running'
                ? 'bg-green-500'
                : sandboxStatus === 'error'
                ? 'bg-red-500'
                : sandboxStatus === 'loading'
                ? 'bg-yellow-500 animate-pulse'
                : 'bg-slate-400'
            }`}
          />
          <span className="text-sm text-slate-500">
            {sandboxStatus === 'idle' && 'Sandbox sin iniciar'}
            {sandboxStatus === 'loading' && 'Cargando Pyodide...'}
            {sandboxStatus === 'ready' && 'Listo (Pyodide)'}
            {sandboxStatus === 'running' && 'Ejecutando...'}
            {sandboxStatus === 'error' && 'Error en ejecución previa'}
          </span>
        </div>

        <div className="flex flex-wrap items-center justify-end gap-2">
          <button
            onClick={runCode}
            disabled={isRunning}
            className="btn-primary disabled:opacity-50"
            title={`Ejecutar (${ATAJO_EJECUTAR})`}
            aria-keyshortcuts="Control+Enter Meta+Enter"
          >
            <Play className="h-4 w-4 mr-2" />
            {isRunning ? 'Ejecutando...' : 'Ejecutar'}
            {!isRunning && (
              <kbd aria-hidden="true" className="ml-2 hidden sm:inline rounded bg-white/20 px-1.5 py-0.5 font-sans text-[10px] font-medium">
                {ATAJO_EJECUTAR}
              </kbd>
            )}
          </button>

          {/* Solo con codigo del alumno corriendo: durante la carga de Pyodide
              no hay nada que detener y matar el worker dejaria la carga colgada. */}
          {sandboxStatus === 'running' && (
            <button
              onClick={abortExecution}
              className="btn-secondary text-red-700"
              title="Detener la ejecucion y reiniciar el sandbox"
            >
              <Square className="h-4 w-4 mr-2" />
              Detener
            </button>
          )}

          <button onClick={resetCode} className="btn-secondary" title="Reiniciar codigo">
            <RotateCcw className="h-4 w-4" />
          </button>

          <button onClick={saveCode} className="btn-secondary" title="Descargar script Python">
            <Save className="h-4 w-4" />
          </button>

          <button onClick={shareCode} className="btn-secondary" title="Copiar codigo al portapapeles">
            <Share2 className="h-4 w-4" />
          </button>

          {testsUrl !== null && (
            <div className="flex items-center gap-2">
              <button
                onClick={runTests}
                disabled={isRunningTests}
                className="btn-secondary disabled:opacity-50"
                title="Correr los tests ocultos del ejercicio en Pyodide"
              >
                <TestTube2 className="h-4 w-4 mr-2" />
                {isRunningTests ? 'Ejecutando tests...' : 'Ejecutar tests'}
              </button>
              {isRunningTests && usesHeavyImport(code) && (
                <span className="text-xs text-amber-700 italic">
                  Primera vez: ~5s mientras Pyodide carga numpy/pandas del CDN
                </span>
              )}
            </div>
          )}

          {exerciseId !== null && (
            <button
              onClick={() => setShowHistory(true)}
              className="btn-secondary"
              title="Ver evaluaciones previas de este ejercicio"
            >
              <History className="h-4 w-4 mr-2" />
              Historial
            </button>
          )}

          <button
            onClick={evaluateCode}
            disabled={isEvaluating}
            className="btn-secondary disabled:opacity-50"
            title="Pedir al evaluador una calificación socrática de tu intento"
          >
            <ClipboardCheck className="h-4 w-4 mr-2" />
            {isEvaluating ? 'Evaluando...' : 'Evaluar mi código'}
          </button>

          <button
            onClick={() => setPantallaCompleta((v) => !v)}
            className="btn-secondary"
            aria-pressed={pantallaCompleta}
            title={
              pantallaCompleta
                ? 'Salir de pantalla completa (Esc)'
                : 'Editor a pantalla completa'
            }
          >
            {pantallaCompleta ? (
              <Minimize2 className="h-4 w-4" />
            ) : (
              <Maximize2 className="h-4 w-4" />
            )}
          </button>

          <div className="relative">
            <button
              onClick={() => setShowSettings(!showSettings)}
              className={`btn-secondary ${showSettings ? 'ring-2 ring-primary-500' : ''}`}
              title="Configuracion"
            >
              <Settings className="h-4 w-4" />
            </button>

            {showSettings && (
              <div className="absolute right-0 mt-2 w-64 bg-white border border-slate-200 rounded-lg shadow-lg z-10 p-4">
                <h3 className="text-sm font-semibold text-slate-800 mb-3 border-b border-slate-100 pb-2">
                  Configurar editor
                </h3>

                <div className="space-y-4">
                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">Tema</label>
                    <select
                      value={theme}
                      onChange={(e) => setTheme(e.target.value)}
                      className="w-full text-sm border-slate-300 rounded focus:ring-primary-500 focus:border-primary-500 p-1.5 border"
                    >
                      <option value="vs-dark">Oscuro (vs-dark)</option>
                      <option value="light">Claro (light)</option>
                      <option value="hc-black">Alto contraste</option>
                    </select>
                  </div>

                  <div>
                    <label className="block text-xs font-medium text-slate-600 mb-1">
                      Tamaño de fuente: {fontSize}px
                    </label>
                    <input
                      type="range"
                      min="10"
                      max="24"
                      value={fontSize}
                      onChange={(e) => setFontSize(Number(e.target.value))}
                      className="w-full accent-primary-600"
                    />
                  </div>

                  <div className="flex items-center">
                    <input
                      id="minimap-toggle"
                      type="checkbox"
                      checked={minimap}
                      onChange={(e) => setMinimap(e.target.checked)}
                      className="h-4 w-4 text-primary-600 focus:ring-primary-500 border-slate-300 rounded"
                    />
                    <label htmlFor="minimap-toggle" className="ml-2 block text-xs text-slate-600 cursor-pointer">
                      Mostrar minimapa
                    </label>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>
      </div>

      {lessonError && (
        <div className="bg-rose-50 border-b border-rose-200 px-4 py-2 text-sm text-rose-700">
          {lessonError}
        </div>
      )}

      {challengeError && (
        <div className="bg-rose-50 border-b border-rose-200 px-4 py-2 text-sm text-rose-700">
          {challengeError}
        </div>
      )}

      {challenge && (
        <div className="bg-white border-b border-slate-200 px-4 py-3 flex flex-wrap items-center justify-between gap-3">
          <div className="min-w-0">
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <Trophy className="h-3.5 w-3.5 text-amber-600 flex-shrink-0" />
              <span>
                Reto · {challenge.topic}
                {challenge.level ? <> · Nivel {challenge.level} de 3</> : null}
              </span>
            </div>
            <div className="mt-1 flex items-center gap-2 flex-wrap">
              <h2 className="text-base font-semibold text-slate-900">
                {retoIndex >= 0 ? `Reto ${retoIndex + 1} de ${retosLista.length} — ` : ''}
                {challenge.title}
              </h2>
              <span className="text-xs px-2 py-1 rounded-full bg-amber-100 text-amber-700">
                {DIFICULTAD_RETO[challenge.difficulty] || challenge.difficulty}
              </span>
            </div>
          </div>

          <div className="flex items-center gap-2 flex-wrap">
            <Link to="/challenges" className="btn-secondary">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Volver a retos
            </Link>
            {/* Anterior/Siguiente entre retos, igual que entre los ejercicios
                de una lección: se sigue desde aquí sin volver al listado. */}
            <button
              onClick={() => retoAnterior && irAReto(retoAnterior.id)}
              disabled={!retoAnterior}
              className="btn-secondary disabled:opacity-50"
              title={retoAnterior ? retoAnterior.title : 'Es el primer reto de la lista'}
            >
              <ChevronLeft className="h-4 w-4 mr-1" />
              Anterior
            </button>
            <button
              onClick={() => retoSiguiente && irAReto(retoSiguiente.id)}
              disabled={!retoSiguiente}
              className="btn-secondary disabled:opacity-50"
              title={retoSiguiente ? retoSiguiente.title : 'Es el último reto de la lista'}
            >
              Siguiente
              <ChevronRight className="h-4 w-4 ml-1" />
            </button>
          </div>
        </div>
      )}

      {lesson && activeExercise && (
        <div className="bg-white border-b border-slate-200 px-4 py-3 flex flex-wrap items-center justify-between gap-3">
          <div className="min-w-0">
            <div className="flex items-center gap-2 text-xs text-slate-500">
              <BookOpen className="h-3.5 w-3.5 text-primary-600 flex-shrink-0" />
              <Link
                to={`/lessons/${lesson.id}`}
                className="truncate hover:text-primary-700 hover:underline"
              >
                {lesson.title}
              </Link>
              <span>·</span>
              <span>{lesson.progress}% de la lección</span>
            </div>
            <div className="mt-1 flex items-center gap-2 flex-wrap">
              <h2 className="text-base font-semibold text-slate-900">
                Ejercicio {activeIndex + 1} de {exercises.length} — {activeExercise.title}
              </h2>
              <span className="text-xs px-2 py-1 rounded-full bg-primary-100 text-primary-700">
                {activeExercise.difficulty} · {activeExercise.points} pts
              </span>
              {activeExercise.completed && (
                <span className="text-[10px] uppercase tracking-wide text-emerald-700 bg-emerald-100 rounded px-1.5 py-0.5 font-semibold inline-flex items-center gap-1">
                  <CheckCircle2 className="h-3 w-3" />
                  Hecho
                </span>
              )}
            </div>
          </div>

          <div className="flex items-center gap-2 flex-wrap">
            <Link to={`/lessons/${lesson.id}`} className="btn-secondary">
              <ArrowLeft className="h-4 w-4 mr-2" />
              Volver a la lección
            </Link>
            <button
              onClick={() => goToExercise(activeIndex - 1)}
              disabled={activeIndex <= 0}
              className="btn-secondary disabled:opacity-50"
            >
              <ChevronLeft className="h-4 w-4 mr-1" />
              Anterior
            </button>
            <button
              onClick={() => goToExercise(activeIndex + 1)}
              disabled={isLastExercise}
              className="btn-secondary disabled:opacity-50"
              title={
                isLastExercise
                  ? 'Es el último ejercicio de la lección'
                  : 'Cargar el siguiente ejercicio'
              }
            >
              Siguiente
              <ChevronRight className="h-4 w-4 ml-1" />
            </button>
            {isLastExercise && lessonCompleted && nextLesson && (
              <button onClick={() => goToLesson(nextLesson.id)} className="btn-primary">
                Ir a la siguiente lección
                <ChevronRight className="h-4 w-4 ml-1" />
              </button>
            )}
          </div>
        </div>
      )}

      <div className="border-b border-slate-200 bg-slate-50">
        {/* El enunciado ocupa una banda fija que solo hace falta mientras se
            lee. Plegarla es la forma barata de devolverle ese alto al codigo
            sin irse a pantalla completa. */}
        <button
          onClick={() => setContextoPlegado((v) => !v)}
          aria-expanded={!contextoPlegado}
          className="flex w-full items-center gap-2 px-4 py-2 text-xs font-semibold uppercase tracking-wide text-slate-600 hover:bg-slate-100"
        >
          {contextoPlegado ? (
            <ChevronDown className="h-4 w-4" />
          ) : (
            <ChevronUp className="h-4 w-4" />
          )}
          {contextoPlegado ? 'Mostrar enunciado' : 'Ocultar enunciado'}
        </button>

        <div
          className={`grid lg:grid-cols-[1.4fr,1fr] gap-0 border-t border-slate-200 ${
            contextoPlegado ? 'hidden' : ''
          }`}
        >
        <div className="p-4 lg:border-r border-slate-200">
          {enunciadoFijo !== null ? (
            <>
              {/* Lección o reto: el enunciado es del ejercicio, no del alumno.
                  Se muestra como Markdown y no se puede editar, que antes era
                  un textarea que el alumno podia reescribir antes de pedir la
                  evaluacion. */}
              <p className="block text-xs font-semibold text-slate-700 uppercase tracking-wide mb-2">
                Enunciado del ejercicio
              </p>
              <Markdown className="prose prose-sm prose-slate max-w-none max-h-40 overflow-auto rounded-lg border border-slate-300 bg-white px-3 py-2">
                {enunciadoFijo}
              </Markdown>
            </>
          ) : (
            <>
              <label
                htmlFor="enunciado-libre"
                className="block text-xs font-semibold text-slate-700 uppercase tracking-wide mb-2"
              >
                Enunciado del ejercicio (requerido para evaluar)
              </label>
              <textarea
                id="enunciado-libre"
                value={problemDescription}
                onChange={(e) => setProblemDescription(e.target.value)}
                placeholder={PLACEHOLDER_PROBLEM}
                className="w-full p-3 border border-slate-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white"
                rows={4}
              />
            </>
          )}
        </div>

        <div className="p-4">
          <label className="block text-xs font-semibold text-slate-700 uppercase tracking-wide mb-2">
            Salida esperada o criterio correcto (opcional)
          </label>
          <textarea
            value={expectedOutput}
            onChange={(e) => setExpectedOutput(e.target.value)}
            placeholder="Ejemplo: debe imprimir la suma total, o devolver una lista ordenada..."
            className="w-full p-3 border border-slate-300 rounded-lg resize-none focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent bg-white"
            rows={4}
          />
        </div>
        </div>
      </div>

      {evaluationError && (
        <div className="bg-red-50 border-y border-red-200 px-4 py-2 text-sm text-red-700">
          {evaluationError}
        </div>
      )}

      {testsError && (
        <div className="bg-amber-50 border-y border-amber-200 px-4 py-2 text-sm text-amber-800">
          {testsError}
        </div>
      )}

      {testsResult && (
        <div
          className={`border-y px-4 py-3 ${
            testsResult.passed === testsResult.total
              ? 'bg-emerald-50 border-emerald-200'
              : 'bg-rose-50 border-rose-200'
          }`}
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center gap-2">
              <TestTube2
                className={`h-4 w-4 ${
                  testsResult.passed === testsResult.total
                    ? 'text-emerald-600'
                    : 'text-rose-600'
                }`}
              />
              <span className="text-sm font-semibold text-slate-800">
                Tests: {testsResult.passed} / {testsResult.total} pasaron
                <span className="text-slate-500 font-normal ml-2">
                  ({testsResult.durationMs.toFixed(0)} ms)
                </span>
              </span>
            </div>
            <button
              onClick={() => setTestsResult(null)}
              className="text-slate-400 hover:text-slate-600"
              aria-label="Cerrar"
            >
              <X className="h-4 w-4" />
            </button>
          </div>
          <ul className="mt-2 space-y-1 text-sm">
            {testsResult.verdicts.map((v, i) => (
              <li key={i} className="flex items-start gap-2">
                {v.passed ? (
                  <CheckCircle2 className="h-4 w-4 text-emerald-600 mt-0.5 flex-shrink-0" />
                ) : (
                  <XCircle className="h-4 w-4 text-rose-600 mt-0.5 flex-shrink-0" />
                )}
                <div className="flex-1">
                  <span className="text-slate-800">{v.name || `Test ${i + 1}`}</span>
                  {!v.passed && v.errorMessage && (
                    <pre className="mt-1 text-xs font-mono whitespace-pre-wrap text-rose-700 bg-white/60 rounded px-2 py-1">
                      {v.errorMessage}
                    </pre>
                  )}
                </div>
              </li>
            ))}
          </ul>
          {retoResuelto && challenge && (
            <div className="mt-3 flex flex-wrap items-center gap-3 border-t border-emerald-200 pt-3">
              <span className="inline-flex items-center gap-1.5 text-sm font-semibold text-emerald-800">
                <Trophy className="h-4 w-4" />
                Reto resuelto: queda marcado como hecho y suma a tu ELO de retos.
              </span>
              {siguienteNivel && (
                <button onClick={() => irAReto(siguienteNivel.id)} className="btn-primary">
                  Ir al Nivel {siguienteNivel.level}
                  <ChevronRight className="h-4 w-4 ml-1" />
                </button>
              )}
              {retoSiguiente && (
                <button
                  onClick={() => irAReto(retoSiguiente.id)}
                  className={siguienteNivel ? 'btn-secondary' : 'btn-primary'}
                >
                  Siguiente reto
                  <ChevronRight className="h-4 w-4 ml-1" />
                </button>
              )}
            </div>
          )}
        </div>
      )}

      {/* min-h-0: sin el, un hijo flex no baja de la altura de su contenido y
          una salida larga estiraba la pagina en vez de hacer scroll en el panel. */}
      <div className="flex-1 flex flex-col lg:flex-row min-h-0">
        {/* Apilados por debajo de lg: ahi la salida se llevaba 24rem de ancho
            y dejaba el codigo en una columna donde no cabe ni una linea. */}
        <div className="h-72 min-w-0 flex-1 lg:h-auto lg:min-h-0">
          <Editor
            height="100%"
            defaultLanguage="python"
            value={code}
            onChange={(value) => setCode(value || '')}
            theme={theme}
            options={{
              minimap: { enabled: minimap },
              fontSize,
              fontFamily: 'JetBrains Mono, monospace',
              lineNumbers: 'on',
              roundedSelection: false,
              scrollBeyondLastLine: false,
              automaticLayout: true,
              padding: { top: 16 },
            }}
          />
        </div>

        <div className="flex h-64 w-full min-w-0 flex-col bg-slate-900 text-white lg:h-auto lg:w-96 lg:shrink-0">
          <div className="p-3 bg-slate-800 border-b border-slate-700 flex items-center gap-2">
            <Terminal className="h-4 w-4" />
            <span className="text-sm font-medium">Salida</span>
            {/* Resalta en ambar cuando hay algo que limpiar; apagado si no. */}
            <button
              onClick={clearOutput}
              disabled={!haySalida}
              className={`ml-auto inline-flex items-center gap-1 rounded-md px-2.5 py-1 text-xs font-semibold transition-colors ${
                haySalida
                  ? 'bg-amber-400 text-slate-900 shadow hover:bg-amber-300'
                  : 'text-slate-500 cursor-not-allowed'
              }`}
              title="Borrar la salida del panel (el codigo no se toca)"
            >
              <Eraser className="h-3.5 w-3.5" />
              Limpiar salida
            </button>
          </div>

          <div className="p-3 bg-slate-800 border-b border-slate-700">
            <p className="text-xs text-slate-300">
              Pulsa <strong>Evaluar mi código</strong> cuando quieras una calificación socrática.
              El tutor de Q&A vive en una página aparte para preguntas conceptuales.
            </p>
          </div>

          <div ref={salidaRef} className="flex-1 min-h-0 p-4 overflow-auto">
            {output || errorOutput || outputNote || outputImages.length > 0 ? (
              <div className="space-y-3">
                {output && (
                  <div>
                    <p className="text-[10px] uppercase tracking-wide text-slate-400 mb-1">
                      stdout
                    </p>
                    <pre className="text-sm font-mono whitespace-pre-wrap">{output}</pre>
                  </div>
                )}
                {errorOutput && (
                  <div>
                    <p className="text-[10px] uppercase tracking-wide text-amber-400 mb-1">
                      stderr / warnings
                    </p>
                    <pre className="text-sm font-mono whitespace-pre-wrap text-amber-300 bg-amber-950/40 border-l-2 border-amber-500 rounded-r px-2 py-1">
                      {errorOutput}
                    </pre>
                  </div>
                )}
                {outputNote && (
                  <p className="text-sm font-mono text-slate-400">{outputNote}</p>
                )}
                {outputImages.map((b64, i) => (
                  <img
                    key={i}
                    src={`data:image/png;base64,${b64}`}
                    alt={`Plot ${i + 1}`}
                    className="max-w-full bg-white rounded shadow"
                  />
                ))}
              </div>
            ) : (
              <p className="text-slate-400 text-sm">
                {isRunning
                  ? 'Ejecutando... lo que imprima tu codigo aparecera aqui en cuanto lo imprima.'
                  : `La salida aparecera aqui despues de ejecutar el codigo (boton Ejecutar o ${ATAJO_EJECUTAR}).`}
              </p>
            )}
          </div>

          <div className="p-3 bg-slate-800 border-t border-slate-700">
            <div className="flex items-center justify-between text-xs text-slate-400">
              <span>Estado: {isRunning ? 'Ejecutando...' : 'Listo'}</span>
              <span>Python 3.11</span>
            </div>
          </div>
        </div>
      </div>

      {showHistory && exerciseId !== null && (
        <EvaluationHistoryModal
          exerciseId={exerciseId}
          onClose={() => setShowHistory(false)}
        />
      )}

      {evaluation && (
        <div
          className="fixed inset-0 bg-black/50 flex items-center justify-center z-50 p-4"
          onClick={() => setEvaluation(null)}
        >
          <div
            className="bg-white rounded-lg shadow-xl max-w-3xl w-full max-h-[85vh] flex flex-col"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="flex items-center justify-between border-b border-slate-200 p-4">
              <div>
                <h2 className="text-lg font-semibold text-slate-900">
                  Evaluación socrática
                </h2>
                <p className="text-xs text-slate-500 mt-1">
                  Evaluación #{evaluation.id} · {new Date(evaluation.created_at).toLocaleString()}
                  {evaluation.model_used ? ` · ${evaluation.model_used}` : ''}
                </p>
              </div>
              <button
                onClick={() => setEvaluation(null)}
                className="text-slate-400 hover:text-slate-600"
                aria-label="Cerrar"
              >
                <X className="h-5 w-5" />
              </button>
            </div>

            <div className="p-4 overflow-auto flex-1">
              <EvaluacionSocratica
                raw={evaluation.verdict.raw}
                logicScore={evaluation.verdict.logic_score}
                generalScore={evaluation.verdict.general_score}
              />
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default CodeEditor
