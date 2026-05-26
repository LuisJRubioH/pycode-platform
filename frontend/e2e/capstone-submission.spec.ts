import { test, expect, type Page } from '@playwright/test'

/**
 * E2E del flujo completo de envio del capstone:
 * 1. Login
 * 2. Editar los 3 archivos con una solucion correcta
 * 3. Pulsar "Enviar capstone"
 * 4. Esperar a que Pyodide se inicialice + corra tests + persista
 * 5. Verificar que el badge muestra "Aprobado · 8/8 tests"
 */

const TEST_EMAIL = 'capstone_run@example.com'
const TEST_PASSWORD = 'TestPass123'
const TEST_USERNAME = 'capstonerun'
const API_BASE = 'http://localhost:8000/api/v1'

const STORE_PY = `"""Modulo de persistencia y CRUD de ventas."""

import json
from pathlib import Path


class SalesStore:
    def __init__(self, ruta_archivo=None):
        self.ruta_archivo = ruta_archivo
        self._ventas = []

    def add_venta(self, producto, cantidad, precio_unitario):
        if cantidad <= 0:
            raise ValueError(f"cantidad debe ser > 0, recibido {cantidad}")
        if precio_unitario <= 0:
            raise ValueError(f"precio_unitario debe ser > 0, recibido {precio_unitario}")
        self._ventas.append({
            "producto": producto,
            "cantidad": cantidad,
            "precio_unitario": precio_unitario,
        })

    def list_ventas(self):
        return list(self._ventas)

    def remove_producto(self, producto):
        antes = len(self._ventas)
        self._ventas = [v for v in self._ventas if v["producto"] != producto]
        return antes - len(self._ventas)

    def save(self):
        if not self.ruta_archivo:
            return
        Path(self.ruta_archivo).write_text(
            json.dumps(self._ventas, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def load(self):
        if not self.ruta_archivo:
            return
        path = Path(self.ruta_archivo)
        if not path.exists():
            return
        self._ventas = json.loads(path.read_text(encoding="utf-8"))
`

const REPORTS_PY = `"""Funciones puras para calcular reportes sobre una lista de ventas."""


def total_ventas(ventas):
    return sum(v["cantidad"] * v["precio_unitario"] for v in ventas)


def ventas_por_producto(ventas):
    out = {}
    for v in ventas:
        out[v["producto"]] = out.get(v["producto"], 0) + v["cantidad"] * v["precio_unitario"]
    return out


def top_n_productos(ventas, n):
    agrupado = ventas_por_producto(ventas)
    ordenado = sorted(agrupado.items(), key=lambda kv: kv[1], reverse=True)
    return ordenado[:n]
`

async function ensureUser(page: Page) {
  await page.request.post(`${API_BASE}/auth/register`, {
    data: { email: TEST_EMAIL, username: TEST_USERNAME, password: TEST_PASSWORD },
    failOnStatusCode: false,
  })
}

async function login(page: Page) {
  await ensureUser(page)
  await page.goto('/login', { waitUntil: 'domcontentloaded', timeout: 60_000 })
  await page.fill('input[type=email]', TEST_EMAIL)
  await page.fill('input[type=password]', TEST_PASSWORD)
  await page.click('button[type=submit]')
  await page.waitForURL(/\/(dashboard|$)/, { timeout: 15_000 })
}

async function editFile(page: Page, fileName: string, content: string) {
  // Scope al card del archivo (div con clase rounded-xl que contiene el label exacto)
  const card = page.locator('div.rounded-xl', {
    has: page.getByText(fileName, { exact: true }),
  })
  await expect(card).toHaveCount(1, { timeout: 5000 })
  const editBtn = card.getByRole('button', { name: /^Editar$/ })
  await editBtn.click()
  // Asegura que el textarea aparecio antes de llenarlo
  const textarea = card.locator('textarea')
  await expect(textarea).toBeVisible({ timeout: 5000 })
  await textarea.fill(content)
  // Verifica que el contenido quedo persistido en el state
  await expect(textarea).toHaveValue(content)
}

test('flujo completo: editar archivos + enviar capstone + 8/8 passed', async ({ page }) => {
  // Este test inicializa Pyodide (descarga ~10MB) y corre 8 tests reales.
  // Es lento, le damos margen amplio.
  test.setTimeout(180_000)

  await login(page)
  await page.goto('/capstones/track-1-cli-ventas', {
    waitUntil: 'domcontentloaded',
    timeout: 60_000,
  })
  await expect(
    page.getByRole('heading', { name: /CLI de gestion de ventas/i }),
  ).toBeVisible()

  // Edita los 3 archivos con la solucion correcta
  await editFile(page, 'store.py', STORE_PY)
  await editFile(page, 'reports.py', REPORTS_PY)

  // Pulsa "Enviar capstone"
  await page.getByRole('button', { name: /Enviar capstone/i }).click()

  // Espera a que termine y aparezca el resultado
  await expect(
    page.getByRole('heading', { name: /Resultado de los tests/i }),
  ).toBeVisible({ timeout: 120_000 })

  // Verifica el contador 8/8
  const heading = page.getByRole('heading', { name: /Resultado de los tests/i })
  await expect(heading).toContainText('8/8')

  // Verifica el badge "Aprobado" (puede haber toast + badge, tomamos el primero)
  await expect(page.getByText(/Aprobado . 8\/8 tests/i).first()).toBeVisible({
    timeout: 10_000,
  })

  // Screenshot para revision visual
  await page.screenshot({
    path: 'screenshots/capstone-submission-passed.png',
    fullPage: true,
  })
})
