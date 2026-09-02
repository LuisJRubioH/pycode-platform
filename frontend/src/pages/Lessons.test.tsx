import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import { MemoryRouter } from 'react-router-dom'
import Lessons from './Lessons'

// Mock del servicio de API: Lessons.tsx llama api.get('/lessons').
const getMock = vi.fn()
vi.mock('../services/api', () => ({
  api: {
    get: (...args: unknown[]) => getMock(...args),
  },
}))

function mockLessons(rows: Array<Record<string, unknown>>) {
  getMock.mockResolvedValue({
    ok: true,
    json: async () => rows,
  })
}

const baseLesson = {
  id: 1,
  title: 'Pandas esencial',
  description: 'Series y DataFrames',
  difficulty: 'intermediate',
  category: 'data-science',
  estimated_duration: 20,
}

describe('Lessons — barra de progreso', () => {
  beforeEach(() => {
    getMock.mockReset()
  })

  it('la barra de la tarjeta llega a 100% cuando la lección está completada', async () => {
    mockLessons([{ ...baseLesson, progress: 100, status: 'completed' }])

    render(
      <MemoryRouter>
        <Lessons />
      </MemoryRouter>
    )

    // El título aparece cuando terminó de cargar.
    await screen.findByText('Pandas esencial')

    // La barra de la tarjeta usa width inline = `${progress}%`.
    const bar = document.querySelector<HTMLElement>(
      '.bg-primary-600[style*="width"]'
    )
    expect(bar).not.toBeNull()
    expect(bar!.style.width).toBe('100%')

    // Badge "Hecho" visible.
    expect(screen.getByText('Hecho')).toBeInTheDocument()
  })

  it('el progreso general refleja completadas / totales', async () => {
    mockLessons([
      { ...baseLesson, id: 1, progress: 100, status: 'completed' },
      {
        ...baseLesson,
        id: 2,
        title: 'NumPy básico',
        progress: 0,
        status: 'not_started',
      },
    ])

    render(
      <MemoryRouter>
        <Lessons />
      </MemoryRouter>
    )

    await screen.findByText('Pandas esencial')

    await waitFor(() => {
      // 1 de 2 completadas => 50%
      expect(screen.getByText('50%')).toBeInTheDocument()
    })
    expect(
      screen.getByText(/Has completado 1 de 2 lecciones/)
    ).toBeInTheDocument()
  })
})
