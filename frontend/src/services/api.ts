/**
 * Centralized API service.
 * Automatically injects the JWT token into request headers.
 */

const API_BASE = '/api/v1'

interface RequestOptions extends RequestInit {
  skipAuth?: boolean
}

/**
 * Make an authenticated API request.
 * Automatically includes the JWT token from localStorage.
 */
export async function apiRequest(
  endpoint: string,
  options: RequestOptions = {}
): Promise<Response> {
  const { skipAuth = false, headers: customHeaders, ...rest } = options

  const headers: Record<string, string> = {
    'Content-Type': 'application/json',
    ...(customHeaders as Record<string, string>),
  }

  if (!skipAuth) {
    const token = localStorage.getItem('pycode_token')
    if (token) {
      headers['Authorization'] = `Bearer ${token}`
    }
  }

  const response = await fetch(`${API_BASE}${endpoint}`, {
    headers,
    ...rest,
  })

  // If unauthorized, clear the token
  if (response.status === 401 && !skipAuth) {
    localStorage.removeItem('pycode_token')
    window.location.href = '/login'
  }

  return response
}

/**
 * Convenience methods for common HTTP verbs.
 */
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
