import { FullConfig } from '@playwright/test';

async function globalTeardown(config: FullConfig) {
  console.log('🧹 Limpiando después de los tests...');
  // Cleanup tasks here if needed
}

export default globalTeardown;