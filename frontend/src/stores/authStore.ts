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
  accessToken: string | null
  refreshToken: string | null
  isAuthenticated: boolean
  isLoading: boolean

  setTokens: (access: string, refresh: string) => void
  clearTokens: () => void

  login: (email: string, password: string) => Promise<void>
  register: (username: string, email: string, password: string) => Promise<void>
  logout: () => Promise<void>
  checkAuth: () => Promise<void>
}

const API_BASE = '/api/v1'
const ACCESS_KEY = 'pycode_access_token'
const REFRESH_KEY = 'pycode_refresh_token'
const LEGACY_KEY = 'pycode_token'

function bootstrapAccess(): string | null {
  const stored = localStorage.getItem(ACCESS_KEY)
  if (stored) return stored
  const legacy = localStorage.getItem(LEGACY_KEY)
  if (legacy) {
    localStorage.setItem(ACCESS_KEY, legacy)
    localStorage.removeItem(LEGACY_KEY)
    return legacy
  }
  return null
}

const initialAccess = bootstrapAccess()
const initialRefresh = localStorage.getItem(REFRESH_KEY)

export const useAuthStore = create<AuthState>((set, get) => ({
  user: null,
  accessToken: initialAccess,
  refreshToken: initialRefresh,
  isAuthenticated: !!initialAccess,
  isLoading: false,

  setTokens: (access, refresh) => {
    localStorage.setItem(ACCESS_KEY, access)
    localStorage.setItem(REFRESH_KEY, refresh)
    set({ accessToken: access, refreshToken: refresh, isAuthenticated: true })
  },

  clearTokens: () => {
    localStorage.removeItem(ACCESS_KEY)
    localStorage.removeItem(REFRESH_KEY)
    localStorage.removeItem(LEGACY_KEY)
    set({
      accessToken: null,
      refreshToken: null,
      user: null,
      isAuthenticated: false,
    })
  },

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
    get().setTokens(data.access_token, data.refresh_token)
    set({
      user: {
        id: data.user_id,
        username: data.username,
        email,
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

  logout: async () => {
    const refresh = get().refreshToken
    if (refresh) {
      try {
        await fetch(`${API_BASE}/auth/logout`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh_token: refresh }),
        })
      } catch {
        // Network error: clear tokens locally anyway
      }
    }
    get().clearTokens()
  },

  checkAuth: async () => {
    const token = get().accessToken
    if (!token) {
      set({ isAuthenticated: false, user: null })
      return
    }
    try {
      const response = await fetch(`${API_BASE}/auth/me`, {
        headers: { Authorization: `Bearer ${token}` },
      })
      if (response.ok) {
        const user = await response.json()
        set({ user, isAuthenticated: true })
      } else {
        get().clearTokens()
      }
    } catch {
      // Network error — keep current state
    }
  },
}))
