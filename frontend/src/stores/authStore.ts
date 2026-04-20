/**
 * Authentication store using Zustand.
 * Manages user state, JWT token persistence, and auth actions.
 */

import { create } from 'zustand'

interface User {
  id: number
  username: string
  email: string
  is_active: boolean
  created_at: string
  last_login: string | null
}

interface AuthState {
  user: User | null
  token: string | null
  isAuthenticated: boolean
  isLoading: boolean

  // Actions
  login: (email: string, password: string) => Promise<void>
  register: (username: string, email: string, password: string) => Promise<void>
  logout: () => void
  checkAuth: () => Promise<void>
}

const API_BASE = '/api/v1'

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  token: localStorage.getItem('pycode_token'),
  isAuthenticated: !!localStorage.getItem('pycode_token'),
  isLoading: false,

  login: async (email: string, password: string) => {
    set({ isLoading: true })

    const response = await fetch(`${API_BASE}/auth/login`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, password }),
    })

    if (!response.ok) {
      set({ isLoading: false })
      const data = await response.json()
      throw new Error(data.detail || 'Error al iniciar sesión')
    }

    const data = await response.json()
    localStorage.setItem('pycode_token', data.access_token)

    set({
      token: data.access_token,
      isAuthenticated: true,
      user: {
        id: data.user_id,
        username: data.username,
        email: email,
        is_active: true,
        created_at: '',
        last_login: null,
      },
      isLoading: false,
    })
  },

  register: async (username: string, email: string, password: string) => {
    set({ isLoading: true })

    const response = await fetch(`${API_BASE}/auth/register`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ username, email, password }),
    })

    if (!response.ok) {
      set({ isLoading: false })
      const data = await response.json()
      throw new Error(data.detail || 'Error al registrar')
    }

    set({ isLoading: false })
  },

  logout: () => {
    localStorage.removeItem('pycode_token')
    set({
      user: null,
      token: null,
      isAuthenticated: false,
    })
  },

  checkAuth: async () => {
    const token = get().token
    if (!token) {
      set({ isAuthenticated: false, user: null })
      return
    }

    try {
      const response = await fetch(`${API_BASE}/auth/me`, {
        headers: {
          Authorization: `Bearer ${token}`,
        },
      })

      if (response.ok) {
        const user = await response.json()
        set({ user, isAuthenticated: true })
      } else {
        // Token expired or invalid
        localStorage.removeItem('pycode_token')
        set({ user: null, token: null, isAuthenticated: false })
      }
    } catch {
      // Network error — keep current state
    }
  },
}))
