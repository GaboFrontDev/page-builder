import { Page, expect } from '@playwright/test';

export class AuthHelper {
  constructor(private page: Page) {}

  async register(email: string, username: string, password: string) {
    await this.page.goto('/register');
    await this.page.fill('input[name="email"]', email);
    await this.page.fill('input[name="username"]', username);
    await this.page.fill('input[name="password"]', password);
    await this.page.fill('input[name="confirmPassword"]', password);
    await this.page.click('button[type="submit"]');
    
    // Should redirect to dashboard after successful registration
    await expect(this.page).toHaveURL('/');
  }

  async login(email: string, password: string) {
    await this.page.goto('/login');
    await this.page.fill('input[name="email"]', email);
    await this.page.fill('input[name="password"]', password);
    await this.page.click('button[type="submit"]');
    
    // Should redirect to dashboard after successful login
    await expect(this.page).toHaveURL('/');
  }

  async logout() {
    await this.page.click('text=Cerrar sesión');
    await expect(this.page).toHaveURL('/login');
  }

  async ensureLoggedIn(email: string = 'test@example.com', password: string = 'testpass123') {
    // Check if already logged in
    const currentUrl = this.page.url();
    if (currentUrl.includes('/login') || currentUrl.includes('/register')) {
      try {
        await this.login(email, password);
      } catch {
        // If login fails, try to register first
        const username = email.split('@')[0];
        await this.register(email, username, password);
      }
    }
  }

  async ensureLoggedOut() {
    const currentUrl = this.page.url();
    if (!currentUrl.includes('/login') && !currentUrl.includes('/register')) {
      await this.logout();
    }
  }
}