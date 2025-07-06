import { test, expect } from '@playwright/test';
import { AuthHelper } from './helpers/auth';

test.describe('Autenticación', () => {
  let auth: AuthHelper;

  test.beforeEach(async ({ page }) => {
    auth = new AuthHelper(page);
  });

  test('debería mostrar la página de login por defecto', async ({ page }) => {
    await page.goto('/');
    await expect(page).toHaveURL('/login');
    await expect(page.locator('h2')).toContainText('Inicia sesión en tu cuenta');
  });

  test('debería permitir registro de nuevo usuario', async ({ page }) => {
    const timestamp = Date.now();
    const email = `test${timestamp}@example.com`;
    const username = `testuser${timestamp}`;
    const password = 'testpass123';

    await page.goto('/register');
    
    // Llenar formulario de registro
    await page.fill('input[name="email"]', email);
    await page.fill('input[name="username"]', username);
    await page.fill('input[name="password"]', password);
    await page.fill('input[name="confirmPassword"]', password);
    
    // Enviar formulario
    await page.click('button[type="submit"]');
    
    // Debería redirigir al dashboard
    await expect(page).toHaveURL('/');
    await expect(page.locator('h1:has-text("Mis Páginas")')).toBeVisible();
    await expect(page.locator('text=Hola,')).toContainText(`Hola, ${username}`);
  });

  test('debería mostrar error para email duplicado', async ({ page }) => {
    const email = 'duplicate@example.com';
    const username1 = 'user1';
    const username2 = 'user2';
    const password = 'testpass123';

    // Registrar primer usuario
    await auth.register(email, username1, password);
    await auth.logout();

    // Intentar registrar segundo usuario con el mismo email
    await page.goto('/register');
    await page.fill('input[name="email"]', email);
    await page.fill('input[name="username"]', username2);
    await page.fill('input[name="password"]', password);
    await page.fill('input[name="confirmPassword"]', password);
    await page.click('button[type="submit"]');

    // Debería mostrar error
    await expect(page.locator('text=Email already registered')).toBeVisible();
  });

  test('debería mostrar error para contraseñas que no coinciden', async ({ page }) => {
    await page.goto('/register');
    await page.fill('input[name="email"]', 'test@example.com');
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'password123');
    await page.fill('input[name="confirmPassword"]', 'differentpassword');
    await page.click('button[type="submit"]');

    await expect(page.locator('text=Las contraseñas no coinciden')).toBeVisible();
  });

  test('debería permitir login con credenciales válidas', async ({ page }) => {
    const timestamp = Date.now();
    const email = `logintest${timestamp}@example.com`;
    const username = `loginuser${timestamp}`;
    const password = 'loginpass123';

    // Registrar usuario primero
    await auth.register(email, username, password);
    await auth.logout();

    // Hacer login
    await auth.login(email, password);
    
    // Verificar que está en el dashboard
    await expect(page).toHaveURL('/');
    await expect(page.locator(`text=Hola, ${username}`)).toBeVisible();
  });

  test('debería mostrar error para credenciales incorrectas', async ({ page }) => {
    await page.goto('/login');
    await page.fill('input[name="email"]', 'nonexistent@example.com');
    await page.fill('input[name="password"]', 'wrongpassword');
    await page.click('button[type="submit"]');

    await expect(page.locator('text=Incorrect email or password')).toBeVisible();
  });

  test('debería permitir cerrar sesión', async ({ page }) => {
    await auth.ensureLoggedIn();
    await auth.logout();
    await expect(page).toHaveURL('/login');
  });

  test('debería redirigir a login para rutas protegidas', async ({ page }) => {
    await page.goto('/builder');
    await expect(page).toHaveURL('/login');
  });

  test('debería navegar entre login y registro', async ({ page }) => {
    await page.goto('/login');
    await page.click('text=crea una cuenta nueva');
    await expect(page).toHaveURL('/register');

    await page.click('text=inicia sesión en tu cuenta existente');
    await expect(page).toHaveURL('/login');
  });

  test('debería validar campos requeridos', async ({ page }) => {
    await page.goto('/register');
    await page.click('button[type="submit"]');

    // Los campos requeridos deberían mostrar validación nativa del navegador
    const emailInput = page.locator('input[name="email"]');
    await expect(emailInput).toHaveAttribute('required');
  });

  test('debería validar formato de email', async ({ page }) => {
    await page.goto('/register');
    await page.fill('input[name="email"]', 'email-invalido');
    await page.fill('input[name="username"]', 'testuser');
    await page.fill('input[name="password"]', 'testpass123');
    await page.fill('input[name="confirmPassword"]', 'testpass123');
    await page.click('button[type="submit"]');

    // El input type="email" debería validar el formato
    const emailInput = page.locator('input[name="email"]');
    await expect(emailInput).toHaveAttribute('type', 'email');
  });
});