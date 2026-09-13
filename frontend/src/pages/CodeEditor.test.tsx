import { describe, it, expect, vi, beforeEach } from 'vitest'
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Link, MemoryRouter, Route, Routes } from 'react-router-dom'
import CodeEditor from './CodeEditor'

// Monaco no corre en jsdom: lo sustituimos por un textarea que expone el
// valor del editor para poder afirmar que el starter code cambia.
vi.mock('@monaco-editor/react', () => ({
  __esModule: true,
  default: ({ value }: { value: string }) => (
    <textarea data-testid="monaco" value={value} readOnly />
  ),
  useMonaco: () => null,
}))

const runPythonCodeMock = vi.fn()
vi.mock('../services/codeRunner', () => ({
  runPythonCode: (...args: unknown[]) => runPythonCodeMock(...args),
  runHiddenTests: vi.fn(),
  abortExecution: vi.fn(),
  isSandboxInterruption: () => false,
  getCodeRunner: () => ({
    status: 'idle' as const,
    onStatusChange: () => () => {},
  }),
}))

const getMock = vi.fn()
const postMock = vi.fn()
vi.mock('../services/api', () => ({
  api: {
    get: (...args: unknown[]) => getMock(...args),
    post: (...args: unknown[]) => postMock(...args),
  },
}))

const lesson = {
  id: 7,
  title: 'Pandas esencial',
  track: 'track-2',
  status: 'in_progress',
  progress: 33,
  exercises: [
    {
      id: 101,
      lesson_id: 7,
      title: 'Series desde diccionario',
      description: 'Crea una Series',
      instructions: 'Construye una Series a partir de un dict.',
      starter_code: '# starter uno\n',
      difficulty: 'easy',
      points: 10,
      order: 1,
      hints: [],
      completed: true,
    },
    {
      id: 102,
      lesson_id: 7,
      title: 'DataFrame desde listas',
      description: 'Crea un DataFrame',
      instructions: 'Construye un DataFrame.',
      starter_code: '# starter dos\n',
      difficulty: 'medium',
      points: 20,
      order: 2,
      hints: [],
      completed: false,
    },
    {
      id: 103,
      lesson_id: 7,
      title: 'Filtrar filas',
      description: 'Filtra un DataFrame',
      instructions: 'Filtra por condicion.',
      starter_code: '# starter tres\n',
      difficulty: 'hard',
      points: 30,
      order: 3,
      hints: [],
      completed: false,
    },
  ],
}

function renderEditor(url: string) {
  return render(
    <MemoryRouter initialEntries={[url]}>
      <Routes>
        <Route path="/editor" element={<CodeEditor />} />
      </Routes>
    </MemoryRouter>
  )
}

describe('CodeEditor — navegación por lección', () => {
  beforeEach(() => {
    getMock.mockReset()
    postMock.mockReset()
    runPythonCodeMock.mockReset()
    localStorage.clear()
    getMock.mockImplementation((path: string) => {
      if (path === '/lessons/7') {
        return Promise.resolve({ ok: true, json: async () => lesson })
      }
      return Promise.resolve({ ok: true, json: async () => [] })
    })
  })

  it('muestra la cabecera con el ejercicio activo, su lección y sus badges', async () => {
    renderEditor('/editor?lesson=7&exercise=101')

    await screen.findByText('Ejercicio 1 de 3 — Series desde diccionario')
    expect(screen.getByText('Pandas esencial')).toBeInTheDocument()
    expect(screen.getByText('easy · 10 pts')).toBeInTheDocument()
    expect(screen.getByText('33% de la lección')).toBeInTheDocument()
    // El ejercicio ya aprobado se marca como hecho.
    expect(screen.getByText('Hecho')).toBeInTheDocument()
  })

  it('"Anterior" se deshabilita en el primer ejercicio', async () => {
    renderEditor('/editor?lesson=7&exercise=101')
    await screen.findByText('Ejercicio 1 de 3 — Series desde diccionario')

    expect(screen.getByRole('button', { name: /Anterior/ })).toBeDisabled()
    expect(screen.getByRole('button', { name: /Siguiente/ })).toBeEnabled()
  })

  it('"Siguiente" se deshabilita en el último ejercicio', async () => {
    renderEditor('/editor?lesson=7&exercise=103')
    await screen.findByText('Ejercicio 3 de 3 — Filtrar filas')

    expect(screen.getByRole('button', { name: /Siguiente/ })).toBeDisabled()
    expect(screen.getByRole('button', { name: /Anterior/ })).toBeEnabled()
  })

  it('"Siguiente" carga el starter code del siguiente ejercicio y limpia la salida', async () => {
    const user = userEvent.setup()
    renderEditor('/editor?lesson=7&exercise=101')

    await screen.findByText('Ejercicio 1 de 3 — Series desde diccionario')
    expect(screen.getByTestId('monaco')).toHaveValue('# starter uno\n')

    await user.click(screen.getByRole('button', { name: /Siguiente/ }))

    await screen.findByText('Ejercicio 2 de 3 — DataFrame desde listas')
    // No se arrastra el código del ejercicio anterior.
    await waitFor(() =>
      expect(screen.getByTestId('monaco')).toHaveValue('# starter dos\n')
    )
    expect(screen.getByText('medium · 20 pts')).toBeInTheDocument()
    expect(screen.queryByText('Hecho')).not.toBeInTheDocument()
  })

  it('sin parámetros de lección el editor sigue en modo libre', async () => {
    renderEditor('/editor')
    await waitFor(() => expect(screen.getByTestId('monaco')).toBeInTheDocument())
    // Vacio: el modo libre es para el codigo propio del alumno.
    expect(screen.getByTestId('monaco')).toHaveValue('')
    expect(screen.queryByText(/Ejercicio 1 de/)).not.toBeInTheDocument()
    expect(getMock).not.toHaveBeenCalled()
  })

  it('el modo libre no carga el ultimo ejercicio que la leccion dejo en localStorage', async () => {
    // Lo que guarda LessonDetail al pulsar "Practicar".
    localStorage.setItem(
      'pycode_tutor_context',
      JSON.stringify({
        problem_description: 'Bucles for y while\n\nEjercicio: Tabla del 7',
        student_code: '# starter de la leccion\n',
        exercise_id: 101,
      })
    )
    renderEditor('/editor')

    await waitFor(() => expect(screen.getByTestId('monaco')).toBeInTheDocument())
    expect(screen.getByTestId('monaco')).not.toHaveValue('# starter de la leccion\n')
    expect(screen.queryByDisplayValue(/Tabla del 7/)).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /Ejecutar tests/ })).not.toBeInTheDocument()
  })

  it('ir de una leccion a "Editor" deja el editor limpio', async () => {
    const user = userEvent.setup()
    render(
      <MemoryRouter initialEntries={['/editor?lesson=7&exercise=101']}>
        <Link to="/editor">Editor</Link>
        <Routes>
          <Route path="/editor" element={<CodeEditor />} />
        </Routes>
      </MemoryRouter>
    )
    await screen.findByText('Ejercicio 1 de 3 — Series desde diccionario')
    expect(screen.getByTestId('monaco')).toHaveValue('# starter uno\n')

    await user.click(screen.getByRole('link', { name: 'Editor' }))

    await waitFor(() =>
      expect(screen.queryByText(/Ejercicio 1 de 3/)).not.toBeInTheDocument()
    )
    expect(screen.getByTestId('monaco')).toHaveValue('')
    expect(screen.queryByDisplayValue(/Series desde diccionario/)).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /Ejecutar tests/ })).not.toBeInTheDocument()
  })
})

describe('CodeEditor — salida separada de stdout y stderr', () => {
  beforeEach(() => {
    getMock.mockReset()
    postMock.mockReset()
    runPythonCodeMock.mockReset()
    localStorage.clear()
  })

  it('stdout y stderr se muestran en bloques distintos, no concatenados', async () => {
    const user = userEvent.setup()
    runPythonCodeMock.mockResolvedValue({
      ok: true,
      stdout: 'total: 42',
      stderr: 'FutureWarning: algo va a cambiar',
      images: [],
      durationMs: 12,
      timedOut: false,
    })

    renderEditor('/editor')
    await user.click(screen.getByRole('button', { name: /Ejecutar/ }))

    await screen.findByText('total: 42')
    // Cada flujo con su etiqueta: un warning ya no parece un error del alumno.
    expect(screen.getByText('stdout')).toBeInTheDocument()
    expect(screen.getByText('stderr / warnings')).toBeInTheDocument()
    // Y siguen siendo dos nodos separados.
    expect(screen.getByText('total: 42')).not.toBe(
      screen.getByText('FutureWarning: algo va a cambiar')
    )
  })

  it('sin salida ni error muestra la nota, sin bloque de stderr', async () => {
    const user = userEvent.setup()
    runPythonCodeMock.mockResolvedValue({
      ok: true,
      stdout: '',
      stderr: '',
      images: [],
      durationMs: 3,
      timedOut: false,
    })

    renderEditor('/editor')
    await user.click(screen.getByRole('button', { name: /Ejecutar/ }))

    await screen.findByText('(sin salida)')
    expect(screen.queryByText('stderr / warnings')).not.toBeInTheDocument()
  })

  it('"Limpiar salida" vacia el panel sin tocar el codigo', async () => {
    const user = userEvent.setup()
    runPythonCodeMock.mockResolvedValue({
      ok: true,
      stdout: 'total: 42',
      stderr: 'FutureWarning: algo va a cambiar',
      images: [],
      durationMs: 12,
      timedOut: false,
    })

    renderEditor('/editor')
    const limpiar = screen.getByRole('button', { name: /Limpiar salida/ })
    // Sin nada que limpiar, el boton no hace como que hace algo.
    expect(limpiar).toBeDisabled()

    const codigo = (screen.getByTestId('monaco') as HTMLTextAreaElement).value
    await user.click(screen.getByRole('button', { name: /^Ejecutar$/ }))
    await screen.findByText('total: 42')

    await user.click(limpiar)

    expect(screen.queryByText('total: 42')).not.toBeInTheDocument()
    expect(screen.queryByText('FutureWarning: algo va a cambiar')).not.toBeInTheDocument()
    expect(screen.getByText(/La salida aparecera aqui/)).toBeInTheDocument()
    expect(screen.getByTestId('monaco')).toHaveValue(codigo)
    expect(limpiar).toBeDisabled()
  })
})

describe('CodeEditor — atajo Ctrl+Enter', () => {
  beforeEach(() => {
    getMock.mockReset()
    postMock.mockReset()
    runPythonCodeMock.mockReset()
    localStorage.clear()
  })

  it('Ctrl+Enter y Cmd+Enter ejecutan el codigo; con algo corriendo no lanzan otro', async () => {
    let terminar!: () => void
    runPythonCodeMock.mockImplementation(
      () =>
        new Promise((resolve) => {
          terminar = () =>
            resolve({ ok: true, stdout: 'hola', stderr: '', images: [], durationMs: 1, timedOut: false })
        })
    )
    renderEditor('/editor')
    await waitFor(() => expect(screen.getByTestId('monaco')).toBeInTheDocument())

    const evento = fireEvent.keyDown(window, { key: 'Enter', ctrlKey: true })
    expect(runPythonCodeMock).toHaveBeenCalledTimes(1)
    // preventDefault: dentro de Monaco no debe insertar ademas una linea.
    expect(evento).toBe(false)

    // Mientras corre, repetir el atajo no lanza una segunda ejecucion.
    await screen.findByRole('button', { name: /Ejecutando/ })
    fireEvent.keyDown(window, { key: 'Enter', ctrlKey: true })
    expect(runPythonCodeMock).toHaveBeenCalledTimes(1)

    act(() => terminar())
    await screen.findByText('hola')

    fireEvent.keyDown(window, { key: 'Enter', metaKey: true })
    expect(runPythonCodeMock).toHaveBeenCalledTimes(2)
  })

  it('Enter solo o Shift+Ctrl+Enter no ejecutan', async () => {
    renderEditor('/editor')
    await waitFor(() => expect(screen.getByTestId('monaco')).toBeInTheDocument())

    fireEvent.keyDown(window, { key: 'Enter' })
    fireEvent.keyDown(window, { key: 'Enter', ctrlKey: true, shiftKey: true })
    expect(runPythonCodeMock).not.toHaveBeenCalled()
  })
})

describe('CodeEditor — salida en vivo (issue #32)', () => {
  beforeEach(() => {
    getMock.mockReset()
    postMock.mockReset()
    runPythonCodeMock.mockReset()
    localStorage.clear()
  })

  it('muestra lo impreso mientras corre y lo conserva si la ejecucion se corta', async () => {
    const user = userEvent.setup()
    let emitir!: (lineas: string[]) => void
    let cortar!: (e: Error) => void
    runPythonCodeMock.mockImplementation(
      (_code: string, _timeout: number | undefined, onSalida: (l: string[]) => void) => {
        emitir = onSalida
        return new Promise((_, reject) => {
          cortar = reject
        })
      }
    )

    renderEditor('/editor')
    await user.click(screen.getByRole('button', { name: /Ejecutar/ }))

    // Un bucle con print: la salida aparece antes de que termine nada.
    // (se pinta agrupado cada 100 ms, de ahi el findByText).
    act(() => emitir(['retirando...', 'retirando...']))
    expect(await screen.findByText(/retirando\.\.\.\s+retirando\.\.\./)).toBeInTheDocument()
    act(() => emitir(['retirando...']))
    expect(await screen.findByText(/(retirando\.\.\.\s+){2}retirando\.\.\./)).toBeInTheDocument()

    // El alumno pulsa Detener justo tras una tanda que aun no se habia
    // pintado: se muestra igual, y lo anterior sigue a la vista.
    act(() => emitir(['ultima']))
    act(() => cortar(new Error('Ejecucion detenida.')))
    await screen.findByText(/Ejecucion detenida\./)
    expect(screen.getByText(/(retirando\.\.\.\s+){2}retirando\.\.\.\s+ultima/)).toBeInTheDocument()

    // Una tanda rezagada que llega tras el corte no se pega a la salida.
    act(() => emitir(['rezagada']))
    await new Promise((r) => setTimeout(r, 150))
    expect(screen.queryByText(/rezagada/)).not.toBeInTheDocument()
  })
})
