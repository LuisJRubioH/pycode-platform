import { test, expect, type Page } from '@playwright/test'

/**
 * Smoke test E2E del flujo de Capstone Track 1.
 *
 * Prerequisitos:
 * - Backend en :8000 con migracion 0008 aplicada y seeder corrido (lifespan).
 * - Frontend dev (`npm run dev`) en :5173.
 * - Existe usuario `capstone_test@example.com / TestPass123` (se crea on-the-fly
 *   si no existe).
 */

const TEST_EMAIL = 'capstone_test@example.com'
const TEST_PASSWORD = 'TestPass123'
const TEST_USERNAME = 'capstonetest'
const API_BASE = 'http://localhost:8000/api/v1'

async function ensureUser(page: Page) {
  // Registrar es idempotente para el test: si el user ya existe, falla con
  // 400 y seguimos al login.
  const ctx = page.request
  await ctx.post(`${API_BASE}/auth/register`, {
    data: {
      email: TEST_EMAIL,
      username: TEST_USERNAME,
      password: TEST_PASSWORD,
    },
    failOnStatusCode: false,
  })
}

async function login(page: Page) {
  await ensureUser(page)
  // Vite cold-compila la primera ruta; subir el timeout y usar
  // 'domcontentloaded' para no esperar todos los assets.
  await page.goto('/login', { waitUntil: 'domcontentloaded', timeout: 60_000 })
  await page.fill('input[type=email]', TEST_EMAIL)
  await page.fill('input[type=password]', TEST_PASSWORD)
  await page.click('button[type=submit]')
  await page.waitForURL(/\/(dashboard|$)/, { timeout: 15_000 })
}

test('capstone detail muestra titulo, requisitos y archivos starter', async ({
  page,
}) => {
  await login(page)
  await page.goto('/capstones/track-1-cli-ventas')

  // Header
  await expect(page.getByRole('heading', { name: /CLI de gestion de ventas/i })).toBeVisible()
  await expect(page.getByText(/Track 1 . Python . Capstone/i)).toBeVisible()
  await expect(page.getByText(/Intermedio/i)).toBeVisible()

  // Requisitos
  await expect(page.getByRole('heading', { name: /Requisitos/i })).toBeVisible()
  await expect(page.getByText('R1', { exact: true })).toBeVisible()
  await expect(page.getByText('R8', { exact: true })).toBeVisible()

  // Archivos starter
  await expect(page.getByRole('heading', { name: /Archivos del proyecto/i })).toBeVisible()
  // exact: true para no chocar con "ventas_cli/ store.py" que tambien aparece
  // dentro del bloque markdown "Estructura sugerida".
  await expect(page.getByText('store.py', { exact: true })).toBeVisible()
  await expect(page.getByText('reports.py', { exact: true })).toBeVisible()
  await expect(page.getByText('cli.py', { exact: true })).toBeVisible()

  // 3 archivos -> 3 botones "Copiar" y 3 botones "Descargar"
  await expect(page.getByRole('button', { name: /^Copiar$/i })).toHaveCount(3)
  await expect(page.getByRole('button', { name: /^Descargar$/i })).toHaveCount(3)

  // CTA enviar capstone (habilitado desde Pieza D.3)
  const enviar = page.getByRole('button', { name: /Enviar capstone/i })
  await expect(enviar).toBeVisible()
  await expect(enviar).toBeEnabled()
})

test('capstone detail NO expone hidden_tests en el DOM', async ({ page }) => {
  await login(page)
  await page.goto('/capstones/track-1-cli-ventas')

  // Esperar el render completo
  await expect(page.getByRole('heading', { name: /Requisitos/i })).toBeVisible()

  const html = await page.content()
  // Strings de los hidden_tests del seeder de prueba (jamas deben aparecer):
  expect(html).not.toContain('hidden_tests')
  // El contenido del seeder real usa "store.add_venta" en los tests; en
  // requisitos tambien aparece, asi que no podemos chequear esa cadena. Pero
  // si chequear que NO aparezca el assertion del test:
  expect(html).not.toContain('raise AssertionError')
})

test('competencias muestra CTA Capstone Track 1', async ({ page }) => {
  await login(page)
  await page.goto('/competencias')
  const cta = page.getByRole('link', { name: /Capstone Track 1/i })
  await expect(cta).toBeVisible()
  await cta.click()
  await expect(page).toHaveURL(/\/capstones\/track-1-cli-ventas/)
  await expect(page.getByRole('heading', { name: /CLI de gestion de ventas/i })).toBeVisible()
})
