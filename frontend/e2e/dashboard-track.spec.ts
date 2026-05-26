import { test, expect } from '@playwright/test'

/**
 * E2E del widget "Tu Track" en el Dashboard (Pieza D.4).
 *
 * Usa storageState compartido (`auth.setup.ts`). El usuario `e2e_runner`
 * probablemente ya tiene una submission passed por correr antes este suite
 * (capstone-submission.spec.ts). Este test no asume estado inicial — solo
 * postea una submission via API y verifica que el badge cambie a
 * "Certificado desbloqueado".
 */

const API_BASE = 'http://localhost:8000/api/v1'
const E2E_USER = { email: 'e2e_runner@example.com', password: 'TestPass123' }

test('dashboard widget muestra Certificado desbloqueado tras submission passed', async ({
  page,
}) => {
  test.setTimeout(60_000)

  // Obtener token via /login (5/min limite — solo 1 call por test)
  const loginRes = await page.request.post(`${API_BASE}/auth/login`, {
    data: E2E_USER,
  })
  const { access_token } = await loginRes.json()

  // Postea submission passed via API (mas rapido que UI Pyodide)
  const testsRes = await page.request.get(
    `${API_BASE}/capstones/track-1-cli-ventas/hidden-tests`,
    { headers: { Authorization: `Bearer ${access_token}` } },
  )
  const testsBody = await testsRes.json()
  const total = testsBody.tests.length

  const post = await page.request.post(
    `${API_BASE}/capstones/track-1-cli-ventas/submissions`,
    {
      headers: { Authorization: `Bearer ${access_token}` },
      data: {
        files: [{ path: 'store.py', content: '# fake passed' }],
        tests_passed: total,
        tests_total: total,
        test_results: testsBody.tests.map((t: { name: string }) => ({
          name: t.name,
          passed: true,
        })),
      },
    },
  )
  expect(post.status()).toBe(201)

  await page.goto('/dashboard', {
    waitUntil: 'domcontentloaded',
    timeout: 30_000,
  })

  await expect(page.getByRole('heading', { name: /Tu Track/i })).toBeVisible({
    timeout: 10_000,
  })
  await expect(page.getByText(/Track 1 . Python/i)).toBeVisible()
  await expect(page.getByText(/Certificado desbloqueado/i)).toBeVisible({
    timeout: 10_000,
  })
  await expect(page.getByText(/Aprobado . \d+\/\d+ tests/i)).toBeVisible()
  await expect(page.getByRole('link', { name: /Ver capstone/i })).toBeVisible()

  await page.screenshot({
    path: 'screenshots/dashboard-track-passed.png',
    fullPage: true,
  })
})
