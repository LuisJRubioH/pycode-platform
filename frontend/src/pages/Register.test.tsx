import { describe, it, expect, vi, beforeEach } from 'vitest'
import { render, screen, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import { MemoryRouter } from 'react-router-dom'

import Register from './Register'
import { ErrorDeApi } from '../services/erroresApi'

const registerMock = vi.fn()

vi.mock('../stores/authStore', () => ({
  useAuthStore: (selector: (estado: unknown) => unknown) =>
    selector({ register: registerMock }),
}))

function montar() {
  return render(
    <MemoryRouter>
      <Register />
    </MemoryRouter>
  )
}

async function rellenar(
  usuario: ReturnType<typeof userEvent.setup>,
  campos: { username?: string; email?: string; password?: string; confirm?: string }
) {
  if (campos.username)
    await usuario.type(screen.getByLabelText(/nombre de usuario/i), campos.username)
  if (campos.email) await usuario.type(screen.getByLabelText(/^email$/i), campos.email)
  if (campos.password)
    await usuario.type(screen.getByLabelText(/^contraseña$/i), campos.password)
  if (campos.confirm)
    await usuario.type(screen.getByLabelText(/confirmar contraseña/i), campos.confirm)
}

describe('Register', () => {
  beforeEach(() => {
    registerMock.mockReset()
    registerMock.mockResolvedValue(undefined)
  })

  it('muestra las reglas del usuario y de la contraseña antes de enviar nada', () => {
    montar()
    expect(screen.getByText(/solo letras sin tilde, números/i)).toBeInTheDocument()
    expect(screen.getByText(/al menos 8 caracteres/i)).toBeInTheDocument()
    expect(screen.getByText(/al menos un número/i)).toBeInTheDocument()
  })

  it('el error del nombre de usuario sale en su campo, no en la contraseña', async () => {
    // La regresión exacta: un username inválido no debe parecer un problema
    // de la contraseña.
    const usuario = userEvent.setup()
    montar()

    await rellenar(usuario, {
      username: 'con espacio',
      email: 'a@b.com',
      password: 'ClaveValida123',
      confirm: 'ClaveValida123',
    })
    await usuario.click(screen.getByRole('button', { name: /crear cuenta/i }))

    const campo = screen.getByLabelText(/nombre de usuario/i)
    expect(campo).toHaveAttribute('aria-invalid', 'true')
    expect(screen.getByLabelText(/^contraseña$/i)).toHaveAttribute(
      'aria-invalid',
      'false'
    )
    expect(registerMock).not.toHaveBeenCalled()
  })

  it('no deja enviar si las contraseñas no coinciden', async () => {
    const usuario = userEvent.setup()
    montar()

    await rellenar(usuario, {
      username: 'valido',
      email: 'a@b.com',
      password: 'ClaveValida123',
      confirm: 'OtraDistinta123',
    })
    await usuario.click(screen.getByRole('button', { name: /crear cuenta/i }))

    expect(await screen.findByText(/no coinciden/i)).toBeInTheDocument()
    expect(registerMock).not.toHaveBeenCalled()
  })

  it('reparte por campo los errores que devuelve el backend', async () => {
    registerMock.mockRejectedValue(
      new ErrorDeApi(
        'Error al registrar',
        { username: 'Ese nombre ya está pillado' },
        422
      )
    )
    const usuario = userEvent.setup()
    montar()

    await rellenar(usuario, {
      username: 'valido',
      email: 'a@b.com',
      password: 'ClaveValida123',
      confirm: 'ClaveValida123',
    })
    await usuario.click(screen.getByRole('button', { name: /crear cuenta/i }))

    expect(await screen.findByText(/ya está pillado/i)).toBeInTheDocument()
    await waitFor(() =>
      expect(screen.getByLabelText(/nombre de usuario/i)).toHaveAttribute(
        'aria-invalid',
        'true'
      )
    )
  })

  it('borra el error de un campo en cuanto se corrige', async () => {
    const usuario = userEvent.setup()
    montar()

    await rellenar(usuario, {
      username: 'ab',
      email: 'a@b.com',
      password: 'ClaveValida123',
      confirm: 'ClaveValida123',
    })
    await usuario.click(screen.getByRole('button', { name: /crear cuenta/i }))
    expect(await screen.findByText(/al menos 3 caracteres/i)).toBeInTheDocument()

    await usuario.type(screen.getByLabelText(/nombre de usuario/i), 'c')
    await waitFor(() =>
      expect(screen.queryByText(/al menos 3 caracteres/i)).not.toBeInTheDocument()
    )
  })

  it('con todo correcto llama al registro', async () => {
    const usuario = userEvent.setup()
    montar()

    await rellenar(usuario, {
      username: 'alumno_1',
      email: 'a@b.com',
      password: 'ClaveValida123',
      confirm: 'ClaveValida123',
    })
    await usuario.click(screen.getByRole('button', { name: /crear cuenta/i }))

    await waitFor(() =>
      expect(registerMock).toHaveBeenCalledWith(
        'alumno_1',
        'a@b.com',
        'ClaveValida123'
      )
    )
  })
})
