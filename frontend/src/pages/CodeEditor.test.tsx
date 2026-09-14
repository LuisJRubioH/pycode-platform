import { describe, it, expect, vi, beforeEach } from 'vitest'
import { act, fireEvent, render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { Link, MemoryRouter, Route, Routes, useLocation } from 'react-router-dom'
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
const runHiddenTestsMock = vi.fn()
vi.mock('../services/codeRunner', () => ({
  runPythonCode: (...args: unknown[]) => runPythonCodeMock(...args),
  runHiddenTests: (...args: unknown[]) => runHiddenTestsMock(...args),
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

// Expone la URL actual para comprobar navegaciones con setSearchParams.
function UbicacionActual() {
  const location = useLocation()
  return <span data-testid="ubicacion">{location.search}</span>
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
    // El starter se aplica en un efecto, un render despues de la cabecera.
    await waitFor(() => expect(screen.getByTestId('monaco')).toHaveValue('# starter uno\n'))

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
    // El starter se aplica en un efecto, un render despues de la cabecera.
    await waitFor(() => expect(screen.getByTestId('monaco')).toHaveValue('# starter uno\n'))

    await user.click(screen.getByRole('link', { name: 'Editor' }))

    await waitFor(() =>
      expect(screen.queryByText(/Ejercicio 1 de 3/)).not.toBeInTheDocument()
    )
    expect(screen.getByTestId('monaco')).toHaveValue('')
    expect(screen.queryByText(/Construye una Series/)).not.toBeInTheDocument()
    // Vuelve el enunciado editable del modo libre, vacio.
    expect(screen.getByLabelText(/Enunciado del ejercicio/)).toHaveValue('')
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

describe('CodeEditor — modo reto', () => {
  beforeEach(() => {
    runHiddenTestsMock.mockReset()
  })

  const reto = {
    id: 42,
    title: 'Contar vocales',
    slug: 'contar-vocales',
    source: 'Retos_Python',
    source_path: 'x',
    difficulty: 'easy',
    topic: 'strings',
    prompt: 'Escribe `contar_vocales(texto)` que cuente las **vocales** de un texto.',
    starter_code: 'def contar_vocales(texto):\n    ...\n',
    order_index: 1,
    level: 1,
    levels: [
      { id: 42, level: 1, difficulty: 'easy', completed: false },
      { id: 43, level: 2, difficulty: 'medium', completed: false },
      { id: 44, level: 3, difficulty: 'hard', completed: false },
    ],
  }

  beforeEach(() => {
    getMock.mockReset()
    postMock.mockReset()
    runPythonCodeMock.mockReset()
    localStorage.clear()
    getMock.mockImplementation((path: string) => {
      if (path === '/challenges/42') {
        return Promise.resolve({ ok: true, json: async () => reto })
      }
      return Promise.resolve({ ok: false, json: async () => ({}) })
    })
  })

  it('carga el enunciado y el starter del reto, con "Ejecutar tests"', async () => {
    renderEditor('/editor?challenge=42')

    await screen.findByText('Contar vocales')
    expect(screen.getByText(/Reto · strings\s*· Nivel 1 de 3/)).toBeInTheDocument()
    expect(screen.getByText('Facil')).toBeInTheDocument()
    await waitFor(() =>
      expect(screen.getByTestId('monaco')).toHaveValue('def contar_vocales(texto):\n    ...\n')
    )
    // El enunciado se renderiza como Markdown y no es editable.
    expect(screen.getByText('contar_vocales(texto)').tagName).toBe('CODE')
    expect(screen.getByText('vocales').tagName).toBe('STRONG')
    expect(screen.queryByLabelText(/Enunciado del ejercicio/)).not.toBeInTheDocument()
    expect(screen.getByRole('link', { name: /Volver a retos/ })).toHaveAttribute('href', '/challenges')
    expect(screen.getByRole('button', { name: /Ejecutar tests/ })).toBeInTheDocument()
  })

  it('pasar todos los tests registra el reto y ofrece el siguiente nivel', async () => {
    const user = userEvent.setup()
    const tests = [
      { name: 'uno', code: 'assert True' },
      { name: 'dos', code: 'assert True' },
    ]
    getMock.mockImplementation((path: string) => {
      if (path === '/challenges/42') return Promise.resolve({ ok: true, json: async () => reto })
      if (path === '/challenges/42/hidden-tests') {
        return Promise.resolve({ ok: true, json: async () => ({ challenge_id: 42, tests }) })
      }
      return Promise.resolve({ ok: false, json: async () => ({}) })
    })
    postMock.mockResolvedValue({ ok: true, json: async () => ({}) })
    runHiddenTestsMock.mockResolvedValue({
      total: 2,
      passed: 2,
      durationMs: 5,
      verdicts: tests.map((t) => ({ name: t.name, passed: true })),
    })

    render(
      <MemoryRouter initialEntries={['/editor?challenge=42']}>
        <Routes>
          <Route path="/editor" element={<CodeEditor />} />
        </Routes>
        <UbicacionActual />
      </MemoryRouter>
    )
    await screen.findByText('Contar vocales')
    await user.click(screen.getByRole('button', { name: /Ejecutar tests/ }))

    await screen.findByText(/Reto resuelto/)
    expect(postMock).toHaveBeenCalledWith('/challenges/42/complete', {
      passed_tests: 2,
      total_tests: 2,
    })
    await user.click(screen.getByRole('button', { name: /Ir al Nivel 2/ }))
    expect(screen.getByTestId('ubicacion')).toHaveTextContent('?challenge=43')
  })

  it('con tests fallidos no registra el reto', async () => {
    const user = userEvent.setup()
    getMock.mockImplementation((path: string) => {
      if (path === '/challenges/42') return Promise.resolve({ ok: true, json: async () => reto })
      if (path === '/challenges/42/hidden-tests') {
        return Promise.resolve({
          ok: true,
          json: async () => ({ challenge_id: 42, tests: [{ name: 'uno', code: 'x' }] }),
        })
      }
      return Promise.resolve({ ok: false, json: async () => ({}) })
    })
    runHiddenTestsMock.mockResolvedValue({
      total: 1,
      passed: 0,
      durationMs: 5,
      verdicts: [{ name: 'uno', passed: false, errorMessage: 'AssertionError' }],
    })

    renderEditor('/editor?challenge=42')
    await screen.findByText('Contar vocales')
    await user.click(screen.getByRole('button', { name: /Ejecutar tests/ }))

    await screen.findByText(/Tests: 0 \/ 1 pasaron/)
    expect(postMock).not.toHaveBeenCalled()
    expect(screen.queryByText(/Reto resuelto/)).not.toBeInTheDocument()
  })

  it('ir del reto a "Editor" deja el editor limpio', async () => {
    const user = userEvent.setup()
    render(
      <MemoryRouter initialEntries={['/editor?challenge=42']}>
        <Link to="/editor">Editor</Link>
        <Routes>
          <Route path="/editor" element={<CodeEditor />} />
        </Routes>
      </MemoryRouter>
    )
    await screen.findByText('Contar vocales')
    await waitFor(() =>
      expect(screen.getByTestId('monaco')).toHaveValue('def contar_vocales(texto):\n    ...\n')
    )

    await user.click(screen.getByRole('link', { name: 'Editor' }))

    await waitFor(() => expect(screen.queryByText('Contar vocales')).not.toBeInTheDocument())
    expect(screen.getByTestId('monaco')).toHaveValue('')
    expect(screen.queryByText('contar_vocales(texto)')).not.toBeInTheDocument()
    expect(screen.getByLabelText(/Enunciado del ejercicio/)).toHaveValue('')
  })

  // ---- navegacion entre retos, sin volver al listado ----------------------

  const listaRetos = {
    items: [
      { id: 41, title: 'Invertir cadena', difficulty: 'easy', topic: 'strings' },
      { id: 42, title: 'Contar vocales', difficulty: 'easy', topic: 'strings' },
      { id: 45, title: 'Palindromo', difficulty: 'easy', topic: 'strings' },
    ],
  }

  const conLista = (path: string) => {
    if (path === '/challenges/42') return Promise.resolve({ ok: true, json: async () => reto })
    if (path === '/challenges/45')
      return Promise.resolve({
        ok: true,
        json: async () => ({ ...reto, id: 45, title: 'Palindromo', level: null, levels: [] }),
      })
    if (path.startsWith('/challenges?difficulty=easy'))
      return Promise.resolve({ ok: true, json: async () => listaRetos })
    if (path.startsWith('/challenges/recommended'))
      return Promise.resolve({ ok: true, json: async () => listaRetos })
    return Promise.resolve({ ok: false, json: async () => ({}) })
  }

  it('dice en que reto de la lista estas y deja ir al anterior y al siguiente', async () => {
    getMock.mockImplementation(conLista)
    renderEditor('/editor?challenge=42&dificultad=easy')

    await screen.findByText(/Reto 2 de 3 — Contar vocales/)
    expect(screen.getByRole('button', { name: /Anterior/ })).toBeEnabled()
    expect(screen.getByRole('button', { name: /^Siguiente/ })).toBeEnabled()
    // La lista se pide con el filtro con el que se entro, no otra.
    expect(getMock.mock.calls.map(([p]) => p)).toContain('/challenges?difficulty=easy&limit=60')
  })

  it('"Siguiente" carga el siguiente reto sin pasar por el listado', async () => {
    const user = userEvent.setup()
    getMock.mockImplementation(conLista)
    renderEditor('/editor?challenge=42&dificultad=easy')

    await screen.findByText(/Reto 2 de 3 — Contar vocales/)
    await user.click(screen.getByRole('button', { name: /^Siguiente/ }))

    await screen.findByText(/Reto 3 de 3 — Palindromo/)
    // Pidio el detalle del siguiente reto...
    expect(getMock.mock.calls.map(([p]) => p)).toContain('/challenges/45')
    // ...y la lista sigue siendo la del mismo filtro: no se pidio otra, asi
    // que "siguiente" seguira significando lo mismo en el proximo salto.
    const listas = getMock.mock.calls
      .map(([p]) => p as string)
      .filter((p) => p.startsWith('/challenges?') || p.startsWith('/challenges/recommended'))
    expect(new Set(listas)).toEqual(new Set(['/challenges?difficulty=easy&limit=60']))
  })

  it('en los extremos de la lista los botones se deshabilitan', async () => {
    getMock.mockImplementation(conLista)
    renderEditor('/editor?challenge=45&dificultad=easy')

    await screen.findByText(/Reto 3 de 3 — Palindromo/)
    expect(screen.getByRole('button', { name: /Anterior/ })).toBeEnabled()
    expect(screen.getByRole('button', { name: /^Siguiente/ })).toBeDisabled()
  })

  it('si la lista no carga, el reto se resuelve igual y no hay navegacion', async () => {
    getMock.mockImplementation((path: string) => {
      if (path === '/challenges/42') return Promise.resolve({ ok: true, json: async () => reto })
      return Promise.resolve({ ok: false, json: async () => ({}) })
    })
    renderEditor('/editor?challenge=42&dificultad=easy')

    await screen.findByText('Contar vocales')
    expect(screen.queryByText(/Reto 2 de 3/)).not.toBeInTheDocument()
    expect(screen.getByRole('button', { name: /Anterior/ })).toBeDisabled()
    expect(screen.getByRole('button', { name: /^Siguiente/ })).toBeDisabled()
    expect(screen.getByRole('button', { name: /Ejecutar tests/ })).toBeInTheDocument()
  })

  it('si el reto no existe lo dice, en vez de dejar el editor en blanco sin mas', async () => {
    renderEditor('/editor?challenge=999')
    await screen.findByText('No pudimos cargar este reto.')
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
