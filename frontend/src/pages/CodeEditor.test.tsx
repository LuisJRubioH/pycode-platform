import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter, Route, Routes } from 'react-router-dom'
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

vi.mock('../services/codeRunner', () => ({
  runPythonCode: vi.fn(),
  runHiddenTests: vi.fn(),
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
    expect(screen.queryByText(/Ejercicio 1 de/)).not.toBeInTheDocument()
    expect(getMock).not.toHaveBeenCalled()
  })
})
