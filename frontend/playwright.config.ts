import { defineConfig, devices } from '@playwright/test'

/**
 * Config minima de Playwright para smoke tests E2E del frontend.
 *
 * - Asume que el servidor dev ya esta corriendo (`npm run dev`) en :5173.
 *   Si no lo esta, descomenta el bloque `webServer` para que Playwright lo
 *   levante automaticamente.
 * - Por defecto corre solo en Chromium (headless) para minimizar tiempo.
 */
export default defineConfig({
  testDir: './e2e',
  fullyParallel: false,
  forbidOnly: !!process.env.CI,
  retries: 0,
  workers: 1,
  reporter: [['list']],
  timeout: 60_000,
  use: {
    baseURL: 'http://localhost:5173',
    trace: 'retain-on-failure',
    screenshot: 'only-on-failure',
    navigationTimeout: 60_000,
  },
  projects: [
    // Setup que logea un solo usuario E2E y persiste storageState. Los
    // otros proyectos dependen de el para evitar reaplicar login en cada
    // test (rate limit 5/min en /login + 3/hour en /register).
    { name: 'setup', testMatch: /.*\.setup\.ts/ },
    {
      name: 'chromium',
      use: {
        ...devices['Desktop Chrome'],
        storageState: 'e2e/.auth/user.json',
      },
      dependencies: ['setup'],
    },
  ],
  // webServer: {
  //   command: 'npm run dev',
  //   url: 'http://localhost:5173',
  //   reuseExistingServer: true,
  //   timeout: 60_000,
  // },
})
