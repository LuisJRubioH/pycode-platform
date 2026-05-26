import { test as setup } from '@playwright/test'

/**
 * Global setup que registra (idempotente) y logea un user E2E y guarda
 * el storageState en `e2e/.auth/user.json`. Los specs lo cargan via
 * `test.use({ storageState: ... })` para no quemar el rate limit de
 * /login (5/min) ni /register (3/hour) en cada test.
 */

const API_BASE = 'http://localhost:8000/api/v1'
export const E2E_USER = {
  email: 'e2e_runner@example.com',
  username: 'e2erunner',
  password: 'TestPass123',
}

const AUTH_FILE = 'e2e/.auth/user.json'

setup('authenticate E2E user once', async ({ page }) => {
  // Register (idempotente: 400 si ya existe, lo ignoramos)
  await page.request.post(`${API_BASE}/auth/register`, {
    data: E2E_USER,
    failOnStatusCode: false,
  })

  // Login UI -> obtiene tokens y los persiste en localStorage del browser
  await page.goto('/login', { waitUntil: 'domcontentloaded', timeout: 60_000 })
  await page.fill('input[type=email]', E2E_USER.email)
  await page.fill('input[type=password]', E2E_USER.password)
  await page.click('button[type=submit]')
  await page.waitForURL(/\/(dashboard|$)/, { timeout: 15_000 })

  // Persiste cookies + localStorage al archivo
  await page.context().storageState({ path: AUTH_FILE })
})
