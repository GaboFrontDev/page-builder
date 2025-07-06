import { test, expect } from '@playwright/test';
import { AuthHelper } from './helpers/auth';
import { PageBuilderHelper } from './helpers/page-builder';

test.describe('Visual Regression Tests', () => {
  let auth: AuthHelper;
  let builder: PageBuilderHelper;

  test.beforeEach(async ({ page }) => {
    auth = new AuthHelper(page);
    builder = new PageBuilderHelper(page);
    await auth.ensureLoggedIn();
  });

  test('debería tomar screenshot del dashboard', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveScreenshot('dashboard.png');
  });

  test('debería tomar screenshot del page builder vacío', async ({ page }) => {
    await builder.createNewPage();
    await expect(page).toHaveScreenshot('builder-empty.png');
  });

  test('debería tomar screenshot de página con componentes', async ({ page }) => {
    await builder.createNewPage();
    await builder.addComponent('Header');
    await builder.addComponent('Hero Section');
    await builder.addComponent('Texto');
    await builder.addComponent('Footer');
    
    // Wait for components to load
    await page.waitForTimeout(1000);
    await expect(page).toHaveScreenshot('builder-with-components.png');
  });

  test('debería tomar screenshot del editor de componentes', async ({ page }) => {
    await builder.createNewPage();
    await builder.addComponent('Hero Section');
    
    // Open component editor
    await page.click('.component-preview');
    await page.waitForTimeout(500);
    
    await expect(page).toHaveScreenshot('component-editor.png');
  });

  test('debería tomar screenshot de configuración de página', async ({ page }) => {
    await builder.createNewPage();
    await page.click('text=Configuración');
    await page.waitForTimeout(500);
    
    await expect(page).toHaveScreenshot('page-settings.png');
  });

  test('debería tomar screenshot de cada tema', async ({ page }) => {
    await builder.createNewPage();
    await builder.addComponent('Header');
    await builder.addComponent('Hero Section');
    
    const themes = ['Por Defecto', 'Oscuro', 'Moderno', 'Minimalista'];
    
    for (const theme of themes) {
      await builder.switchTheme(theme);
      await page.waitForTimeout(1000);
      await expect(page).toHaveScreenshot(`theme-${theme.toLowerCase().replace(' ', '-')}.png`);
    }
  });

  test('debería tomar screenshot responsive en móvil', async ({ page }) => {
    await page.setViewportSize({ width: 375, height: 667 }); // iPhone SE
    
    await page.goto('/');
    await expect(page).toHaveScreenshot('dashboard-mobile.png');
    
    await builder.createNewPage();
    await builder.addComponent('Header');
    await builder.addComponent('Hero Section');
    await page.waitForTimeout(1000);
    
    await expect(page).toHaveScreenshot('builder-mobile.png');
  });

  test('debería tomar screenshot de formularios', async ({ page }) => {
    await page.goto('/login');
    await expect(page).toHaveScreenshot('login-form.png');
    
    await page.goto('/register');
    await expect(page).toHaveScreenshot('register-form.png');
  });

  test('debería tomar screenshot de estados de error', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[name="email"]', 'invalid@email.com');
    await page.fill('input[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');
    
    await expect(page.locator('text=Incorrect email or password')).toBeVisible();
    await expect(page).toHaveScreenshot('login-error.png');
  });

  test('debería tomar screenshot de componentes individuales', async ({ page }) => {
    await builder.createNewPage();
    
    const components = [
      'Header',
      'Hero Section', 
      'Texto',
      'Imagen',
      'Botón',
      'Footer'
    ];
    
    for (const component of components) {
      // Create new page for each component to test in isolation
      await page.goto('/builder');
      await builder.addComponent(component);
      await page.waitForTimeout(1000);
      
      await expect(page.locator('.component-preview')).toHaveScreenshot(`component-${component.toLowerCase().replace(' ', '-')}.png`);
    }
  });
});