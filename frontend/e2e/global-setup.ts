import { chromium, FullConfig } from '@playwright/test';

async function globalSetup(config: FullConfig) {
  const browser = await chromium.launch();
  const page = await browser.newPage();
  
  // Wait for backend to be ready
  console.log('🔄 Esperando que el backend esté listo...');
  let retries = 10;
  while (retries > 0) {
    try {
      const backendUrl = process.env.DOCKER_ENV ? 'http://backend:3001' : 'http://localhost:3001';
      const response = await page.goto(`${backendUrl}/api/auth/me`, { 
        waitUntil: 'networkidle',
        timeout: 10000 
      });
      if (response && (response.status() === 401 || response.status() === 403 || response.status() === 422)) {
        console.log('✅ Backend está listo');
        break;
      }
    } catch (error) {
      console.log(`⏳ Intento ${11 - retries}/10 - Backend no disponible, reintentando...`);
      retries--;
      if (retries === 0) {
        console.error('❌ Backend no está disponible después de 10 intentos');
        throw new Error('Backend no disponible');
      }
      await page.waitForTimeout(3000);
    }
  }

  // Wait for frontend to be ready
  console.log('🔄 Esperando que el frontend esté listo...');
  retries = 10;
  while (retries > 0) {
    try {
      const frontendUrl = process.env.DOCKER_ENV ? 'http://frontend:3000' : 'http://localhost:3000';
      const response = await page.goto(frontendUrl, { 
        waitUntil: 'networkidle',
        timeout: 10000 
      });
      if (response && response.status() === 200) {
        console.log('✅ Frontend está listo');
        break;
      }
    } catch (error) {
      console.log(`⏳ Intento ${11 - retries}/10 - Frontend no disponible, reintentando...`);
      retries--;
      if (retries === 0) {
        console.error('❌ Frontend no está disponible después de 10 intentos');
        throw new Error('Frontend no disponible');
      }
      await page.waitForTimeout(3000);
    }
  }

  await browser.close();
  console.log('🚀 Setup completado, iniciando tests...');
}

export default globalSetup;