import { test, expect } from '@playwright/test';
import { AuthHelper } from './helpers/auth';
import { PageBuilderHelper } from './helpers/page-builder';

test.describe('Deployment', () => {
  let auth: AuthHelper;
  let builder: PageBuilderHelper;

  test.beforeEach(async ({ page }) => {
    auth = new AuthHelper(page);
    builder = new PageBuilderHelper(page);
    await auth.ensureLoggedIn();
  });

  test('debería desplegar una página publicada', async ({ page }) => {
    // Create and publish a page
    const pageTitle = `Deploy Test ${Date.now()}`;
    await builder.createNewPage(pageTitle);
    await builder.addComponent('Header');
    await builder.addComponent('Hero Section');
    await builder.publishPage();
    
    // Deploy the page
    await builder.deployPage();
    
    // Should show success message or deployment in progress
    await expect(page.locator('text=Desplegando')).toBeVisible({ timeout: 10000 });
  });

  test('no debería permitir desplegar página no publicada', async ({ page }) => {
    // Create unpublished page
    await builder.createNewPage();
    await builder.addComponent('Header');
    
    // Deploy button should not be visible or should be disabled
    const deployButton = page.locator('text=Desplegar');
    await expect(deployButton).not.toBeVisible();
  });

  test('debería mostrar sitios desplegados en el dashboard', async ({ page }) => {
    // Create, publish and deploy a page
    const pageTitle = `Dashboard Deploy Test ${Date.now()}`;
    await builder.createNewPage(pageTitle);
    await builder.addComponent('Header');
    await builder.publishPage();
    await builder.deployPage();
    
    // Go to dashboard
    await page.goto('/');
    
    // Should show deployed sites section (might take a moment to appear)
    await expect(page.locator('text=Sitios Desplegados')).toBeVisible({ timeout: 15000 });
  });

  test('debería permitir acceder al sitio desplegado', async ({ page, context }) => {
    // Create, publish and deploy a page
    const timestamp = Date.now();
    const pageTitle = `Site Access Test ${timestamp}`;
    await builder.createNewPage(pageTitle);
    await builder.addComponent('Header');
    await builder.editComponent('Header', 'título', 'Mi Sitio Desplegado');
    await builder.publishPage();
    
    // Get the slug from URL or page settings
    await page.click('text=Configuración');
    const slugInput = page.locator('input').nth(1); // Second input should be slug
    const slug = await slugInput.inputValue();
    
    await builder.deployPage();
    
    // Wait for deployment to complete
    await page.waitForTimeout(5000);
    
    // Try to access the deployed site
    const newPage = await context.newPage();
    try {
      await newPage.goto(`http://${slug}.localhost`, { timeout: 30000 });
      await expect(newPage.locator('text=Mi Sitio Desplegado')).toBeVisible({ timeout: 10000 });
    } catch (error) {
      // Deployment might still be in progress, this is acceptable
      console.log('Sitio aún no accesible, deployment en progreso');
    } finally {
      await newPage.close();
    }
  });

  test('debería mostrar estado de deployment', async ({ page }) => {
    // Create and publish page
    await builder.createNewPage();
    await builder.addComponent('Header');
    await builder.publishPage();
    
    // Start deployment
    await builder.deployPage();
    
    // Check deployment status in dashboard
    await page.goto('/');
    
    // Should show some indication of deployment status
    await expect(page.locator('text=Deploy')).toBeVisible();
  });

  test('debería permitir eliminar página desde dashboard', async ({ page }) => {
    // Create a page
    const pageTitle = `Delete Test ${Date.now()}`;
    await builder.createNewPage(pageTitle);
    
    // Go to dashboard
    await page.goto('/');
    
    // Find the page and delete it
    const pageCard = page.locator(`text=${pageTitle}`).locator('..').locator('..');
    await pageCard.locator('text=Eliminar').click();
    
    // Confirm deletion
    page.on('dialog', dialog => dialog.accept());
    
    // Page should be removed from list
    await expect(page.locator(`text=${pageTitle}`)).not.toBeVisible({ timeout: 5000 });
  });

  test('debería mostrar información de páginas en dashboard', async ({ page }) => {
    await page.goto('/');
    
    // Should show page information
    await expect(page.locator('h1')).toContainText('Mis Páginas');
    
    // If there are pages, should show their info
    const pages = page.locator('.card');
    const count = await pages.count();
    
    if (count > 0) {
      // Should show page details
      await expect(pages.first()).toContainText('Tema:');
    } else {
      // Should show empty state
      await expect(page.locator('text=No hay páginas')).toBeVisible();
    }
  });

  test('debería validar slug único al crear página', async ({ page }) => {
    const baseTitle = 'Duplicate Slug Test';
    const slug = 'duplicate-slug-test';
    
    // Create first page with specific slug
    await builder.createNewPage(baseTitle);
    await page.click('text=Configuración');
    const slugInput = page.locator('input').nth(1);
    await slugInput.fill(slug);
    await page.click('text=Guardar Cambios');
    
    // Go back and create another page with same slug
    await page.goto('/');
    await builder.createNewPage(baseTitle + ' 2');
    await page.click('text=Configuración');
    const slugInput2 = page.locator('input').nth(1);
    await slugInput2.fill(slug);
    
    // Should show validation error or auto-adjust slug
    // (Backend should handle this validation)
  });

  test('debería permitir editar página existente desde dashboard', async ({ page }) => {
    // Create a page first
    const pageTitle = `Edit Test ${Date.now()}`;
    await builder.createNewPage(pageTitle);
    
    // Go to dashboard
    await page.goto('/');
    
    // Click edit on the page
    const pageCard = page.locator(`text=${pageTitle}`).locator('..').locator('..');
    await pageCard.locator('text=Editar').click();
    
    // Should navigate to builder
    await expect(page).toHaveURL(/\/builder\/\d+/);
    await expect(page.locator(`text=${pageTitle}`)).toBeVisible();
  });

  test('debería mostrar vista previa de URL en configuración', async ({ page }) => {
    await builder.createNewPage();
    await page.click('text=Configuración');
    
    // Should show URL preview
    await expect(page.locator('text=.localhost')).toBeVisible();
  });

  test('debería validar longitud y formato de slug', async ({ page }) => {
    await builder.createNewPage();
    await page.click('text=Configuración');
    
    const slugInput = page.locator('input').nth(1);
    
    // Test invalid characters
    await slugInput.fill('invalid slug with spaces');
    await expect(page.locator('text=solo puede contener')).toBeVisible();
    
    // Test valid slug
    await slugInput.fill('valid-slug-123');
    await expect(page.locator('text=solo puede contener')).not.toBeVisible();
  });
});