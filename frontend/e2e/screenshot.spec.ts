import { test } from '@playwright/test'

/**
 * No es un test — solo un script para tomar screenshots de la pagina del
 * capstone para revision visual humana. Reusa storageState de auth.setup.
 */

test('screenshot capstone detail', async ({ page }) => {
  await page.setViewportSize({ width: 1440, height: 900 })

  await page.goto('/capstones/track-1-cli-ventas', {
    waitUntil: 'networkidle',
    timeout: 60_000,
  })
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
