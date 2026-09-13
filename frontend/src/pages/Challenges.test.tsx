import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, within } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'
import Challenges from './Challenges'

const getMock = vi.fn()
const postMock = vi.fn()
vi.mock('../services/api', () => ({
  api: {
    get: (...args: unknown[]) => getMock(...args),
    post: (...args: unknown[]) => postMock(...args),
    delete: vi.fn(),
  },
}))

const navigateMock = vi.fn()
vi.mock('react-router-dom', async (importOriginal) => {
  const actual = await importOriginal<typeof import('react-router-dom')>()
  return { ...actual, useNavigate: () => navigateMock }
})

const niveles = [
  { id: 11, level: 1, difficulty: 'easy', completed: true },
  { id: 12, level: 2, difficulty: 'medium', completed: false },
  { id: 13, level: 3, difficulty: 'hard', completed: false },
]

const detalle = (id: number, prompt: string) => ({
  id,
  title: 'Two Sum',
  slug: `two-sum-${id}`,
  source: 'pycode-curated-open',
  source_path: 'x',
  difficulty: niveles.find((n) => n.id === id)!.difficulty,
  topic: 'arrays',
  prompt,
  starter_code: 'def f():\n    pass\n',
  order_index: 1000,
  level: niveles.find((n) => n.id === id)!.level,
  levels: niveles,
})

describe('Retos — progresion por niveles', () => {
  beforeEach(() => {
    getMock.mockReset()
    postMock.mockReset()
    navigateMock.mockReset()
    getMock.mockImplementation((path: string) => {
      if (path.startsWith('/challenges/recommended')) {
        return Promise.resolve({
          ok: true,
          json: async () => ({
            recommended_difficulty: 'medium',
            items: [
              {
                id: 12,
                title: 'Two Sum',
                slug: 'two-sum-12',
                source: 'pycode-curated-open',
                difficulty: 'medium',
                topic: 'arrays',
                prompt_preview: 'en O(n)',
                order_index: 1000,
                completed: false,
                level: 2,
              },
            ],
          }),
        })
      }
      if (path === '/challenges/12') {
        return Promise.resolve({ ok: true, json: async () => detalle(12, 'Nivel medio: en O(n).') })
      }
      if (path === '/challenges/11') {
        return Promise.resolve({ ok: true, json: async () => detalle(11, 'Nivel facil: dos bucles.') })
      }
      return Promise.resolve({ ok: false, json: async () => ({}) })
    })
  })

  it('pide como mucho 50 recomendados (el endpoint devuelve 422 por encima)', async () => {
    render(
      <MemoryRouter>
        <Challenges />
      </MemoryRouter>
    )
    await screen.findByText('Nivel medio: en O(n).')
    const pedido = getMock.mock.calls.map(([p]) => p).find((p: string) => p.includes('recommended'))
    expect(pedido).toBe('/challenges/recommended?limit=50')
  })

  it('la tarjeta dice el nivel y el detalle muestra los tres, con el actual y los hechos', async () => {
    const user = userEvent.setup()
    render(
      <MemoryRouter>
        <Challenges />
      </MemoryRouter>
    )

    await screen.findByText('Nivel medio: en O(n).')
    expect(screen.getByText(/Nivel 2 de 3/)).toBeInTheDocument()

    const progresion = screen.getByRole('list')
    const botones = within(progresion).getAllByRole('button')
    expect(botones.map((b) => b.textContent)).toEqual([
      'Nivel 1 · Facil',
      'Nivel 2 · Medio',
      'Nivel 3 · Dificil',
    ])
    // El nivel en el que estas no es un enlace a si mismo.
    expect(botones[1]).toHaveAttribute('aria-current', 'step')
    expect(botones[1]).toBeDisabled()
    expect(within(botones[0]).getByLabelText('hecho')).toBeInTheDocument()

    await user.click(botones[0])
    await screen.findByText('Nivel facil: dos bucles.')
  })

  it('no hay boton para marcar a mano: se resuelve pasando los tests', async () => {
    render(
      <MemoryRouter>
        <Challenges />
      </MemoryRouter>
    )
    await screen.findByText('Nivel medio: en O(n).')
    expect(screen.queryByRole('button', { name: /Marcar como hecho/ })).not.toBeInTheDocument()
    expect(screen.queryByRole('button', { name: /Desmarcar/ })).not.toBeInTheDocument()
    expect(screen.getByText(/Ejecutar tests/)).toBeInTheDocument()
    // El nivel 2 no esta resuelto; el 1 si, pero no es el seleccionado.
    expect(screen.queryByText('Resuelto')).not.toBeInTheDocument()
  })

  it('"Resolver en el editor" lleva el reto en la URL', async () => {
    const user = userEvent.setup()
    render(
      <MemoryRouter>
        <Challenges />
      </MemoryRouter>
    )
    await screen.findByText('Nivel medio: en O(n).')
    await user.click(screen.getByRole('button', { name: /Resolver en el editor/ }))
    expect(navigateMock).toHaveBeenCalledWith('/editor?challenge=12')
  })
})
