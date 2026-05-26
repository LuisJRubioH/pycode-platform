import { test, expect } from '@playwright/test'
import { readFileSync } from 'fs'

/**
 * E2E del flujo de certificado (Pieza E):
 * 1. Postea una submission passed via API para abrir el gate.
 * 2. Dashboard muestra el boton "Descargar certificado" y baja un PDF real.
 * 3. La pagina publica /verify/:code confirma el certificado.
 * 4. Un codigo invalido muestra "no encontrado".
 *
 * Usa el storageState compartido de auth.setup.ts (usuario `e2e_runner`).
 */

const API_BASE = 'http://localhost:8000/api/v1'
const E2E_USER = { email: 'e2e_runner@example.com', password: 'TestPass123' }

test('certificado: gate -> descarga PDF -> verificacion publica', async ({
  page,
}) => {
  test.setTimeout(60_000)

  // Token via login (1 sola llamada)
  const loginRes = await page.request.post(`${API_BASE}/auth/login`, {
    data: E2E_USER,
  })
  const { access_token } = await loginRes.json()
  const auth = { Authorization: `Bearer ${access_token}` }

  // Submission passed para abrir el gate del certificado
  const testsRes = await page.request.get(
    `${API_BASE}/capstones/track-1-cli-ventas/hidden-tests`,
    { headers: auth },
  )
  const total = (await testsRes.json()).tests.length
  const post = await page.request.post(
    `${API_BASE}/capstones/track-1-cli-ventas/submissions`,
    {
      headers: auth,
      data: {
        files: [{ path: 'store.py', content: '# passed' }],
        tests_passed: total,
        tests_total: total,
        test_results: [],
      },
    },
  )
  expect(post.status()).toBe(201)

  // Dashboard: boton de descarga visible
  await page.goto('/dashboard', { waitUntil: 'domcontentloaded' })
  await expect(
    page.getByText(/Certificado desbloqueado/i),
  ).toBeVisible({ timeout: 10_000 })
  const downloadBtn = page.getByRole('button', {
    name: /Descargar certificado/i,
  })
  await expect(downloadBtn).toBeVisible()
  await page.screenshot({
    path: 'screenshots/cert-dashboard.png',
    fullPage: true,
  })

  // Descargar el PDF y verificar que es un PDF real
  const [download] = await Promise.all([
    page.waitForEvent('download'),
    downloadBtn.click(),
  ])
  expect(download.suggestedFilename()).toMatch(/certificado-pycode-track-1\.pdf/)
  const path = await download.path()
  const bytes = readFileSync(path!)
  expect(bytes.subarray(0, 4).toString()).toBe('%PDF')

  // Codigo de verificacion via API
  const issue = await page.request.post(
    `${API_BASE}/certificates/track-1/issue`,
    { headers: auth },
  )
  const code = (await issue.json()).verification_code

  // Pagina publica de verificacion: valido
  await page.goto(`/verify/${code}`, { waitUntil: 'domcontentloaded' })
  await expect(
    page.getByRole('heading', { name: /Certificado válido/i }),
  ).toBeVisible({ timeout: 10_000 })
  await expect(page.getByText('e2erunner')).toBeVisible()
  await page.screenshot({ path: 'screenshots/cert-verify-valid.png' })

  // Codigo invalido: no encontrado
  await page.goto('/verify/PYC-FAKE-FAKE', { waitUntil: 'domcontentloaded' })
  await expect(
    page.getByRole('heading', { name: /Certificado no encontrado/i }),
  ).toBeVisible({ timeout: 10_000 })
  await page.screenshot({ path: 'screenshots/cert-verify-invalid.png' })
})
