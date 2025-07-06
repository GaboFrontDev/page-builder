import { test, expect } from '@playwright/test';
import { AuthHelper } from './helpers/auth';
import { PageBuilderHelper } from './helpers/page-builder';

test.describe('Performance Tests', () => {
  let auth: AuthHelper;
  let builder: PageBuilderHelper;

  test.beforeEach(async ({ page }) => {
    auth = new AuthHelper(page);
    builder = new PageBuilderHelper(page);
    await auth.ensureLoggedIn();
  });

  test('debería cargar el dashboard rápidamente', async ({ page }) => {
    const startTime = Date.now();
    await page.goto('/');
    await page.waitForLoadState('networkidle');
    const loadTime = Date.now() - startTime;
    
    console.log(`Dashboard load time: ${loadTime}ms`);
    expect(loadTime).toBeLessThan(5000); // Should load in under 5 seconds
  });

  test('debería cargar el page builder rápidamente', async ({ page }) => {
    const startTime = Date.now();
    await builder.createNewPage();
    const loadTime = Date.now() - startTime;
    
    console.log(`Page builder load time: ${loadTime}ms`);
    expect(loadTime).toBeLessThan(10000); // Should load in under 10 seconds
  });

  test('debería agregar componentes sin lag significativo', async ({ page }) => {
    await builder.createNewPage();
    
    const components = ['Header', 'Hero Section', 'Texto', 'Imagen', 'Botón', 'Footer'];
    const times: number[] = [];
    
    for (const component of components) {
      const startTime = Date.now();
      await builder.addComponent(component);
      await page.waitForSelector('.component-preview');
      const addTime = Date.now() - startTime;
      times.push(addTime);
      console.log(`${component} add time: ${addTime}ms`);
    }
    
    const avgTime = times.reduce((a, b) => a + b, 0) / times.length;
    console.log(`Average component add time: ${avgTime}ms`);
    expect(avgTime).toBeLessThan(2000); // Average should be under 2 seconds
  });

  test('debería manejar drag & drop sin lag', async ({ page }) => {
    await builder.createNewPage();
    await builder.addComponent('Header');
    await builder.addComponent('Hero Section');
    await builder.addComponent('Texto');
    
    // Measure drag & drop performance
    const startTime = Date.now();
    await builder.reorderComponents();
    const dragTime = Date.now() - startTime;
    
    console.log(`Drag & drop time: ${dragTime}ms`);
    expect(dragTime).toBeLessThan(1000); // Should complete in under 1 second
  });

  test('debería manejar edición de componentes en tiempo real', async ({ page }) => {
    await builder.createNewPage();
    await builder.addComponent('Hero Section');
    
    // Select component
    await page.click('.component-preview');
    
    // Measure typing response time
    const input = page.locator('input').first();
    const startTime = Date.now();
    
    await input.fill('Test Performance Input');
    await page.waitForTimeout(100); // Small delay for debouncing
    
    const responseTime = Date.now() - startTime;
    console.log(`Input response time: ${responseTime}ms`);
    expect(responseTime).toBeLessThan(500); // Should respond in under 500ms
  });

  test('debería medir Core Web Vitals', async ({ page }) => {
    await page.goto('/');
    
    // Measure performance metrics
    const metrics = await page.evaluate(() => {
      return new Promise((resolve) => {
        // Wait for page to be fully loaded
        setTimeout(() => {
          const navigation = performance.getEntriesByType('navigation')[0] as PerformanceNavigationTiming;
          const paintEntries = performance.getEntriesByType('paint');
          
          const fcp = paintEntries.find(entry => entry.name === 'first-contentful-paint')?.startTime || 0;
          const lcp = paintEntries.find(entry => entry.name === 'largest-contentful-paint')?.startTime || 0;
          
          resolve({
            loadTime: navigation.loadEventEnd - navigation.loadEventStart,
            domContentLoaded: navigation.domContentLoadedEventEnd - navigation.domContentLoadedEventStart,
            firstContentfulPaint: fcp,
            largestContentfulPaint: lcp,
            totalLoadTime: navigation.loadEventEnd - navigation.fetchStart
          });
        }, 2000);
      });
    });
    
    console.log('Performance metrics:', metrics);
    
    // Check Core Web Vitals thresholds
    expect((metrics as any).firstContentfulPaint).toBeLessThan(3000); // FCP < 3s
    expect((metrics as any).totalLoadTime).toBeLessThan(10000); // Total load < 10s
  });

  test('debería manejar múltiples operaciones concurrentes', async ({ page }) => {
    await builder.createNewPage();
    
    // Perform multiple operations quickly
    const startTime = Date.now();
    
    await Promise.all([
      builder.addComponent('Header'),
      page.waitForTimeout(100).then(() => builder.addComponent('Hero Section')),
      page.waitForTimeout(200).then(() => builder.addComponent('Texto'))
    ]);
    
    const totalTime = Date.now() - startTime;
    console.log(`Concurrent operations time: ${totalTime}ms`);
    
    // Should handle concurrent operations
    const components = page.locator('.component-preview');
    await expect(components).toHaveCount(3);
    expect(totalTime).toBeLessThan(5000);
  });

  test('debería medir tiempo de guardado', async ({ page }) => {
    await builder.createNewPage();
    await builder.addComponent('Header');
    
    // Measure save time
    const startTime = Date.now();
    await page.click('text=Guardar Cambios');
    
    // Wait for save confirmation (if any)
    await page.waitForTimeout(1000);
    const saveTime = Date.now() - startTime;
    
    console.log(`Save time: ${saveTime}ms`);
    expect(saveTime).toBeLessThan(3000); // Should save in under 3 seconds
  });

  test('debería medir memoria usage con muchos componentes', async ({ page }) => {
    await builder.createNewPage();
    
    // Add many components to test memory usage
    const componentTypes = ['Header', 'Hero Section', 'Texto', 'Imagen', 'Botón', 'Footer'];
    
    for (let i = 0; i < 10; i++) {
      for (const component of componentTypes) {
        await builder.addComponent(component);
        
        // Check if page is still responsive
        await page.waitForTimeout(100);
      }
    }
    
    // Should have all components
    const components = page.locator('.component-preview');
    await expect(components).toHaveCount(60);
    
    // Page should still be responsive
    await page.click('text=Configuración');
    await expect(page.locator('text=Tema Visual')).toBeVisible({ timeout: 2000 });
  });
});