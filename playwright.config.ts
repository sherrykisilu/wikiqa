import { defineConfig, devices } from '@playwright/test';

export default defineConfig({
  testDir: './tests/e2e',
  reporter: [['list'], ['junit', { outputFile: 'test-results/playwright-junit.xml' }]],
  snapshotPathTemplate: '{testDir}/{testFilePath}-snapshots/{arg}{ext}',
  use: {
    baseURL: process.env.MEDIAWIKI_BASE_URL ?? 'http://localhost:8080',
    trace: 'on-first-retry'
  },
  projects: [
    {
      name: 'chromium',
      use: { ...devices['Desktop Chrome'] }
    }
  ],
  expect: {
    toHaveScreenshot: {
      maxDiffPixelRatio: 0.01
    }
  }
});
