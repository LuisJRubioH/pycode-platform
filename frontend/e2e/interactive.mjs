// Script ad-hoc para abrir el navegador en la pagina del capstone y
// dejarlo abierto. Ctrl+C en la terminal cierra todo.
//
// Uso (con backend + frontend dev corriendo):
//   node e2e/interactive.mjs

import { chromium } from '@playwright/test'

const TEST_EMAIL = 'capstone_test@example.com'
const TEST_PASSWORD = 'TestPass123'
const TEST_USERNAME = 'capstonetest'
const API_BASE = 'http://localhost:8000/api/v1'
const FRONT = 'http://localhost:5173'

const browser = await chromium.launch({ headless: false, slowMo: 50 })
const context = await browser.newContext({
  viewport: { width: 1440, height: 900 },
})
const page = await context.newPage()

// Registro idempotente
try {
  await page.request.post(`${API_BASE}/auth/register`, {
    data: {
      email: TEST_EMAIL,
      username: TEST_USERNAME,
      password: TEST_PASSWORD,
    },
    failOnStatusCode: false,
  })
} catch {
  // ya existe
}

console.log('Login...')
await page.goto(`${FRONT}/login`, {
  waitUntil: 'domcontentloaded',
  timeout: 60_000,
})
await page.fill('input[type=email]', TEST_EMAIL)
await page.fill('input[type=password]', TEST_PASSWORD)
await page.click('button[type=submit]')
await page.waitForURL(/\/(dashboard|$)/)

console.log('Yendo al capstone...')
await page.goto(`${FRONT}/capstones/track-1-cli-ventas`, {
  waitUntil: 'networkidle',
})

console.log('')
console.log('Navegador abierto en:', page.url())
console.log('Explora la pagina libremente. Ctrl+C aqui para cerrar.')
console.log('')

// Mantener vivo el script hasta Ctrl+C
await new Promise(() => {})
