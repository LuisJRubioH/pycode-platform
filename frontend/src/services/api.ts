/**
 * Centralized API service.
 * Auto-inyecta el access_token y, ante un 401, intenta una vez refrescar
 * con el refresh_token antes de propagar el error o forzar logout.
 */

import { useAuthStore } from '../stores/authStore'

const API_BASE = '/api/v1'

interface RequestOptions extends RequestInit {
  skipAuth?: boolean
}

interface RetryFlags {
  __pycodeRetry?: boolean
}

let refreshing: Promise<string | null> | null = null

async function refreshAccessToken(): Promise<string | null> {
  const refresh = useAuthStore.getState().refreshToken
  if (!refresh) return null

  if (!refreshing) {
    refreshing = (async () => {
      try {
        const r = await fetch(`${API_BASE}/auth/refresh`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ refresh_token: refresh }),
        })
        if (!r.ok) return null
        const data = await r.json()
        useAuthStore.getState().setTokens(data.access_token, data.refresh_token)
        return data.access_token as string
      } catch {
        return null
      }
    })().finally(() => {
      refreshing = null
    })
  }

  return refreshing
}

export async function apiRequest(
  endpoint: string,
  options: RequestOptions & RetryFlags = {}
): Promise<Response> {
  const { skipAuth = false, headers: customHeaders, __pycodeRetry, ...rest } = options

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(customHeaders as Record<string, string>),
  }

  if (!skipAuth) {
    const token = useAuthStore.getState().accessToken
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
  }

  const response = await fetch(`${API_BASE}${endpoint}`, { headers, ...rest })

  if (response.status === 401 && !skipAuth && !__pycodeRetry) {
    const newToken = await refreshAccessToken()
    if (newToken) {
      return apiRequest(endpoint, { ...options, __pycodeRetry: true })
    }
    useAuthStore.getState().clearTokens()
    if (typeof window !== 'undefined') {
      window.location.href = '/login'
    }
  }

  return response
}

export const api = {
  get: (endpoint: string, options?: RequestOptions) =>
    apiRequest(endpoint, { method: 'GET', ...options }),

  post: (endpoint: string, body?: unknown, options?: RequestOptions) =>
    apiRequest(endpoint, {
      method: 'POST',
      body: body ? JSON.stringify(body) : undefined,
      ...options,
    }),

  put: (endpoint: string, body?: unknown, options?: RequestOptions) =>
    apiRequest(endpoint, {
      method: 'PUT',
      body: body ? JSON.stringify(body) : undefined,
      ...options,
    }),

  delete: (endpoint: string, options?: RequestOptions) =>
    apiRequest(endpoint, { method: 'DELETE', ...options }),
}
