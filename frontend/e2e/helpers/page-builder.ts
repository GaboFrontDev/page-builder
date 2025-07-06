import { Page, expect } from '@playwright/test';

export class PageBuilderHelper {
  constructor(private page: Page) {}

  async createNewPage(title: string = 'Mi Nueva Página') {
    await this.page.goto('/');
    await this.page.click('text=Nueva Página');
    
    // Should navigate to builder
    await expect(this.page).toHaveURL(/\/builder\/\d+/);
    
    // Update page title
    await this.page.click('text=Configuración');
    await this.page.fill('input[placeholder="Mi Landing Page"]', title);
    await this.page.click('text=Guardar Cambios');
    
    return title;
  }

  async addComponent(componentType: string) {
    await this.page.click('text=Componentes');
    await this.page.click(`text=${componentType}`);
    
    // Component should appear in canvas
    await expect(this.page.locator('.component-preview')).toBeVisible();
  }

  async editComponent(componentType: string, field: string, value: string) {
    // Select component in canvas
    await this.page.click('.component-preview');
    
    // Component editor should open
    await expect(this.page.locator('text=Editar')).toBeVisible();
    
    // Fill field
    const input = this.page.locator(`input[placeholder*="${field}"], textarea[placeholder*="${field}"], input:near(text="${field}")`).first();
    await input.fill(value);
  }

  async publishPage() {
    await this.page.click('text=Publicar');
    await expect(this.page.locator('text=Publicado')).toBeVisible();
  }

  async deployPage() {
    await this.page.click('text=Desplegar');
    // Should show deployment in progress or success
    await expect(this.page.locator('text=Desplegando', { timeout: 10000 })).toBeVisible();
  }

  async verifyComponentInCanvas(componentType: string, content?: string) {
    const component = this.page.locator('.component-preview');
    await expect(component).toBeVisible();
    
    if (content) {
      await expect(component).toContainText(content);
    }
  }

  async reorderComponents() {
    const components = this.page.locator('.component-preview');
    const count = await components.count();
    
    if (count >= 2) {
      // Drag first component below the second
      const firstComponent = components.first();
      const secondComponent = components.nth(1);
      
      await firstComponent.dragTo(secondComponent);
    }
  }

  async deleteComponent() {
    await this.page.click('.component-preview');
    await this.page.click('text=Eliminar Componente');
    
    // Component should be removed
    await expect(this.page.locator('text=Página vacía')).toBeVisible();
  }

  async switchTheme(theme: string) {
    await this.page.click('text=Configuración');
    await this.page.click(`text=${theme}`);
    await this.page.click('text=Guardar Cambios');
  }

  async verifyPageInDashboard(title: string) {
    await this.page.goto('/');
    await expect(this.page.locator(`text=${title}`)).toBeVisible();
  }
}