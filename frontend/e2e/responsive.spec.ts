import { test, expect, type Page } from '@playwright/test'

/**
 * Guard rail de responsive: ninguna pagina debe ser mas ancha que la ventana.
 *
 * Existe porque este fallo se encontro usando la plataforma en varios
 * monitores, no revisando codigo, y porque la mitad no se ve abriendo la
 * pagina ya estrecha: aparece al ENCOGER una ventana que estaba ancha. Monaco
 * mide su ancho al montarse y un hijo flex tiene `min-width: auto`, asi que
 * la columna del editor no bajaba de lo que Monaco ya media y empujaba el
 * panel de Salida fuera de la pantalla.
 *
 * No necesita backend: `/api` va stubeado y el token se inyecta a mano, asi
 * que mide layout y nada mas.
 */

// Anchos reales de uso, del movil al escritorio. 768 y 1024 son los saltos
// de breakpoint, que es donde se rompen las cosas.
const ANCHOS = [360, 390, 768, 1024, 1280, 1920]

const RUTAS = ['/editor', '/lessons', '/dashboard']

const USUARIO = {
  id: 1,
  username: 'e2e',
  email: 'e2e@example.com',
  is_active: true,
  created_at: '2026-01-01T00:00:00Z',
  last_login: null,
}

async function prepararPagina(page: Page) {
  await page.route('**/api/v1/**', (route) => {
    const url = route.request().url()
    let body: unknown = {}
    if (url.includes('/users/me')) body = USUARIO
    else if (url.includes('/lessons')) body = []
    else if (url.includes('/progress')) body = { items: [], tracks: [] }
    return route.fulfill({
      status: 200,
      contentType: 'application/json',
      body: JSON.stringify(body),
    })
  })

  await page.addInitScript(() => {
    localStorage.setItem('pycode_access_token', 'e2e.fake.token')
    localStorage.setItem('pycode_refresh_token', 'e2e.fake.refresh')
  })
}

/** Elementos que sobresalen del ancho de la ventana, para que el fallo diga cual. */
async function desbordes(page: Page) {
  return page.evaluate(() => {
    const raiz = document.documentElement
    const limite = raiz.clientWidth + 1
    const culpables: string[] = []
    for (const nodo of Array.from(document.querySelectorAll('body *'))) {
      const caja = nodo.getBoundingClientRect()
      // Monaco pinta sus capas internas con anchos enormes dentro de un
      // contenedor con overflow oculto: no desbordan la pagina.
      if (nodo.closest('.monaco-editor')) continue
      if (caja.width > 0 && caja.right > limite) {
        culpables.push(
          `<${nodo.tagName.toLowerCase()} class="${String(nodo.className).slice(0, 80)}"> llega a ${Math.round(caja.right)}px`
        )
      }
    }
    return {
      scrollWidth: raiz.scrollWidth,
      clientWidth: raiz.clientWidth,
      culpables: culpables.slice(0, 4),
    }
  })
}

for (const ruta of RUTAS) {
  for (const ancho of ANCHOS) {
    test(`${ruta} no desborda a ${ancho}px`, async ({ page }) => {
      await prepararPagina(page)
      await page.setViewportSize({ width: ancho, height: 900 })
      await page.goto(ruta, { waitUntil: 'networkidle' })
      // Monaco se carga del CDN; medir antes de que monte da un falso verde.
      await page.waitForTimeout(2500)

      const medida = await desbordes(page)
      expect(
        medida.scrollWidth,
        `desborda ${medida.scrollWidth - medida.clientWidth}px: ${medida.culpables.join(' | ')}`
      ).toBeLessThanOrEqual(medida.clientWidth + 1)
    })
  }
}

// El caso que no se ve abriendo la pagina ya estrecha.
for (const ancho of [1280, 1024, 900, 390]) {
  test(`/editor abierto a 1920px y encogido a ${ancho}px no corta la Salida`, async ({
    page,
  }) => {
    await prepararPagina(page)
    await page.setViewportSize({ width: 1920, height: 1080 })
    await page.goto('/editor', { waitUntil: 'networkidle' })
    await page.waitForTimeout(2500)

    await page.setViewportSize({ width: ancho, height: 900 })
    await page.waitForTimeout(2500)

    const medida = await desbordes(page)
    expect(
      medida.scrollWidth,
      `tras encoger desborda ${medida.scrollWidth - medida.clientWidth}px: ${medida.culpables.join(' | ')}`
    ).toBeLessThanOrEqual(medida.clientWidth + 1)
  })
}
