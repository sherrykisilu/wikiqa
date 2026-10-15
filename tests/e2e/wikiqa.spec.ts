import { expect, test, type APIRequestContext, type Page } from '@playwright/test';

const username = process.env.MEDIAWIKI_USER ?? 'Admin';
const password = process.env.MEDIAWIKI_PASSWORD ?? 'AdminPassword123!';

async function login(request: APIRequestContext, baseURL: string) {
  const tokenResponse = await request.get(`${baseURL}/api.php`, {
    params: { action: 'query', meta: 'tokens', type: 'login', format: 'json' }
  });
  const loginToken = (await tokenResponse.json()).query.tokens.logintoken;
  await request.post(`${baseURL}/api.php`, {
    form: { action: 'login', lgname: username, lgpassword: password, lgtoken: loginToken, format: 'json' }
  });
}

async function editPage(request: APIRequestContext, baseURL: string, title: string, text: string) {
  const csrfResponse = await request.get(`${baseURL}/api.php`, {
    params: { action: 'query', meta: 'tokens', format: 'json' }
  });
  const csrfToken = (await csrfResponse.json()).query.tokens.csrftoken;
  await request.post(`${baseURL}/api.php`, {
    form: { action: 'edit', title, text, token: csrfToken, format: 'json' }
  });
}

async function seedChecklistPage(page: Page, title: string, status: string) {
  const baseURL = test.info().project.use.baseURL as string;
  await login(page.request, baseURL);
  await editPage(page.request, baseURL, 'WikiQA_Checklist_Test', `{{#qaChecklist: ${title} | ${status}}}`);
  await page.goto('/index.php?title=WikiQA_Checklist_Test');
}

test('renders checklist parser function', async ({ page }) => {
  await seedChecklistPage(page, 'Release readiness', 'ready');

  const card = page.locator('.wikiqa-checklist');
  await expect(card).toBeVisible();
  await expect(card).toContainText('Release readiness');
  await expect(card).toContainText('Status: Ready');
  await expect(card).toContainText('Automated and manual coverage are linked.');
});

test('matches checklist visual baseline', async ({ page }) => {
  await seedChecklistPage(page, 'Release readiness', 'ready');
  await page.addStyleTag({
    content: `.wikiqa-checklist{background:#f8f9fa;border:1px solid #a2a9b1;border-left:6px solid #14866d;border-radius:0;box-sizing:border-box;height:80px;margin:0;padding:0;width:420px}.wikiqa-checklist *{visibility:hidden}`
  });

  await expect(page.locator('.wikiqa-checklist')).toHaveScreenshot('checklist-card.png');
});

test('documents blocked status', async ({ page }) => {
  await seedChecklistPage(page, 'Deployment risk', 'blocked');

  await expect(page.locator('.wikiqa-checklist')).toHaveAttribute('data-status', 'blocked');
  await expect(page.locator('.wikiqa-checklist')).toContainText('Status: Blocked');
});
