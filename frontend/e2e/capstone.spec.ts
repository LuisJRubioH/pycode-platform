import { test, expect } from '@playwright/test'

/**
 * Smoke tests E2E del flujo de Capstone Track 1.
 *
 * Asume autenticacion previa via `auth.setup.ts` (storageState).
 */

test('capstone detail muestra titulo, requisitos y archivos starter', async ({
  page,
}) => {
  await page.goto('/capstones/track-1-cli-ventas')

  await expect(
    page.getByRole('heading', { name: /CLI de gestion de ventas/i }),
  ).toBeVisible()
  await expect(page.getByText(/Track 1 . Python . Capstone/i)).toBeVisible()
  await expect(page.getByText(/Intermedio/i)).toBeVisible()

  await expect(page.getByRole('heading', { name: /Requisitos/i })).toBeVisible()
  await expect(page.getByText('R1', { exact: true })).toBeVisible()
  await expect(page.getByText('R8', { exact: true })).toBeVisible()

  await expect(
    page.getByRole('heading', { name: /Archivos del proyecto/i }),
  ).toBeVisible()
  await expect(page.getByText('store.py', { exact: true })).toBeVisible()
  await expect(page.getByText('reports.py', { exact: true })).toBeVisible()
  await expect(page.getByText('cli.py', { exact: true })).toBeVisible()

  await expect(page.getByRole('button', { name: /^Copiar$/i })).toHaveCount(3)
  await expect(page.getByRole('button', { name: /^Descargar$/i })).toHaveCount(3)

  const enviar = page.getByRole('button', { name: /Enviar capstone/i })
  await expect(enviar).toBeVisible()
  await expect(enviar).toBeEnabled()
})

test('capstone detail NO expone hidden_tests en el DOM', async ({ page }) => {
  await page.goto('/capstones/track-1-cli-ventas')
  await expect(page.getByRole('heading', { name: /Requisitos/i })).toBeVisible()

  const html = await page.content()
  expect(html).not.toContain('hidden_tests')
  expect(html).not.toContain('raise AssertionError')
})

test('competencias muestra CTA Capstone Track 1', async ({ page }) => {
  await page.goto('/competencias')
  const cta = page.getByRole('link', { name: /Capstone Track 1/i })
  await expect(cta).toBeVisible()
  await cta.click()
  await expect(page).toHaveURL(/\/capstones\/track-1-cli-ventas/)
  await expect(
    page.getByRole('heading', { name: /CLI de gestion de ventas/i }),
  ).toBeVisible()
})
