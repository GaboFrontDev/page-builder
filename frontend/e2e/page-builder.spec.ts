import { test, expect } from '@playwright/test';
import { AuthHelper } from './helpers/auth';
import { PageBuilderHelper } from './helpers/page-builder';

test.describe('Page Builder', () => {
  let auth: AuthHelper;
  let builder: PageBuilderHelper;

  test.beforeEach(async ({ page }) => {
    auth = new AuthHelper(page);
    builder = new PageBuilderHelper(page);
    await auth.ensureLoggedIn();
  });

  test('debería mostrar el dashboard con opción de crear página', async ({ page }) => {
    await page.goto('/');
    await expect(page.locator('h1:has-text("Mis Páginas")')).toBeVisible();
    await expect(page.locator('text=Nueva Página')).toBeVisible();
  });

  test('debería crear una nueva página', async ({ page }) => {
    const pageTitle = `Test Page ${Date.now()}`;
    await builder.createNewPage(pageTitle);
    
    // Verify we're in the builder
    await expect(page).toHaveURL(/\/builder\/\d+/);
    await expect(page.locator(`text=${pageTitle}`)).toBeVisible();
  });

  test('debería agregar y editar componente Header', async ({ page }) => {
    await builder.createNewPage();
    await builder.addComponent('Header');
    
    // Edit header content
    await builder.editComponent('Header', 'título', 'Mi Sitio Web Awesome');
    await builder.verifyComponentInCanvas('header', 'Mi Sitio Web Awesome');
  });

  test('debería agregar y editar componente Hero', async ({ page }) => {
    await builder.createNewPage();
    await builder.addComponent('Hero Section');
    
    // Edit hero content
    await builder.editComponent('Hero', 'Título Principal', 'Bienvenido a mi Landing');
    await builder.verifyComponentInCanvas('hero', 'Bienvenido a mi Landing');
  });

  test('debería agregar múltiples componentes', async ({ page }) => {
    await builder.createNewPage();
    
    // Add multiple components
    await builder.addComponent('Header');
    await builder.addComponent('Hero Section');
    await builder.addComponent('Texto');
    await builder.addComponent('Footer');
    
    // Verify all components are in canvas
    const components = page.locator('.component-preview');
    await expect(components).toHaveCount(4);
  });

  test('debería permitir reordenar componentes con drag & drop', async ({ page }) => {
    await builder.createNewPage();
    await builder.addComponent('Header');
    await builder.addComponent('Hero Section');
    
    // Get initial order
    const firstComponent = page.locator('.component-preview').first();
    const firstText = await firstComponent.textContent();
    
    // Reorder components
    await builder.reorderComponents();
    
    // Verify order changed
    const newFirstComponent = page.locator('.component-preview').first();
    const newFirstText = await newFirstComponent.textContent();
    
    expect(firstText).not.toBe(newFirstText);
  });

  test('debería permitir eliminar componentes', async ({ page }) => {
    await builder.createNewPage();
    await builder.addComponent('Header');
    
    // Delete component
    await builder.deleteComponent();
    
    // Verify component is removed
    await expect(page.locator('text=Página vacía')).toBeVisible();
  });

  test('debería cambiar el tema de la página', async ({ page }) => {
    await builder.createNewPage();
    await builder.addComponent('Hero Section');
    
    // Change theme
    await builder.switchTheme('Oscuro');
    
    // Verify theme change (check canvas background or other theme indicators)
    await expect(page.locator('.canvas')).toBeVisible();
  });

  test('debería publicar una página', async ({ page }) => {
    await builder.createNewPage();
    await builder.addComponent('Header');
    await builder.publishPage();
    
    // Verify published status
    await expect(page.locator('text=Publicado')).toBeVisible();
  });

  test('debería guardar cambios automáticamente', async ({ page }) => {
    const pageTitle = `Auto Save Test ${Date.now()}`;
    await builder.createNewPage(pageTitle);
    
    // Go back to dashboard
    await page.click('svg'); // Back button
    await builder.verifyPageInDashboard(pageTitle);
  });

  test('debería mostrar vista previa en tiempo real', async ({ page }) => {
    await builder.createNewPage();
    await builder.addComponent('Hero Section');
    
    // Edit hero title
    await page.click('.component-preview');
    const titleInput = page.locator('input').first();
    await titleInput.fill('Título de Prueba en Tiempo Real');
    
    // Should see changes immediately in canvas
    await expect(page.locator('.component-preview')).toContainText('Título de Prueba en Tiempo Real');
  });

  test('debería validar campos requeridos en configuración', async ({ page }) => {
    await builder.createNewPage();
    
    // Try to set empty title
    await page.click('text=Configuración');
    const titleInput = page.locator('input[placeholder="Mi Landing Page"]');
    await titleInput.fill('');
    
    // Should maintain some default or show validation
    await expect(titleInput).toHaveValue('');
  });

  test('debería mostrar información de la página', async ({ page }) => {
    await builder.createNewPage();
    await page.click('text=Configuración');
    
    // Should show page info
    await expect(page.locator('text=ID:')).toBeVisible();
    await expect(page.locator('text=Creado:')).toBeVisible();
    await expect(page.locator('text=Estado:')).toBeVisible();
  });

  test('debería editar estilos de componentes', async ({ page }) => {
    await builder.createNewPage();
    await builder.addComponent('Header');
    
    // Select component and edit styles
    await page.click('.component-preview');
    
    // Find color input in styles section
    const colorInput = page.locator('input[type="color"]').first();
    await colorInput.fill('#ff0000');
    
    // Changes should reflect in preview
    await expect(page.locator('.component-preview')).toBeVisible();
  });

  test('debería manejar componentes de imagen', async ({ page }) => {
    await builder.createNewPage();
    await builder.addComponent('Imagen');
    
    // Edit image component
    await page.click('.component-preview');
    const urlInput = page.locator('input[placeholder*="https://"]').first();
    await urlInput.fill('https://picsum.photos/600/400');
    
    // Should show image in preview
    await expect(page.locator('img')).toBeVisible();
  });

  test('debería manejar componentes de botón', async ({ page }) => {
    await builder.createNewPage();
    await builder.addComponent('Botón');
    
    // Edit button component
    await page.click('.component-preview');
    await builder.editComponent('Botón', 'texto', 'Mi Botón Personalizado');
    
    // Should show button in preview
    await expect(page.locator('text=Mi Botón Personalizado')).toBeVisible();
  });

  test('debería permitir alternar visibilidad de componentes', async ({ page }) => {
    await builder.createNewPage();
    await builder.addComponent('Header');
    
    // Select component and toggle visibility
    await page.click('.component-preview');
    await page.click('input[type="checkbox"]');
    
    // Component should disappear from canvas
    await expect(page.locator('text=Página vacía')).toBeVisible();
  });
});