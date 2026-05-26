import { test } from '@playwright/test'

/**
 * No es un test — solo un script para tomar screenshots de la pagina del
 * capstone para revision visual humana.
 */
const TEST_EMAIL = 'capstone_test@example.com'
const TEST_PASSWORD = 'TestPass123'
const TEST_USERNAME = 'capstonetest'
const API_BASE = 'http://localhost:8000/api/v1'

test('screenshot capstone detail', async ({ page }) => {
  await page.request.post(`${API_BASE}/auth/register`, {
    data: { email: TEST_EMAIL, username: TEST_USERNAME, password: TEST_PASSWORD },
    failOnStatusCode: false,
  })

  await page.goto('/login', { waitUntil: 'domcontentloaded', timeout: 60_000 })
  await page.fill('input[type=email]', TEST_EMAIL)
  await page.fill('input[type=password]', TEST_PASSWORD)
  await page.click('button[type=submit]')
  await page.waitForURL(/\/(dashboard|$)/, { timeout: 15_000 })

  await page.goto('/capstones/track-1-cli-ventas', {
    waitUntil: 'networkidle',
    timeout: 60_000,
  })
  await page.setViewportSize({ width: 1440, height: 900 })
  await page.screenshot({
    path: 'screenshots/capstone-detail-full.png',
    fullPage: true,
  })
  await page.screenshot({ path: 'screenshots/capstone-detail-fold.png' })

  await page.goto('/competencias', { waitUntil: 'networkidle' })
  await page.screenshot({
    path: 'screenshots/competencias-with-cta.png',
    fullPage: true,
  })
})
