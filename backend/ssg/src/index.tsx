import React from 'react';
import ReactDOMServer from 'react-dom/server';
import Page from './Page';
import { PageData } from '@shared/index';

// This will be called from the Python backend
export function renderPageToString(pageData: PageData): string {
  const pageElement = React.createElement(Page, { pageData });
  return ReactDOMServer.renderToString(pageElement);
}

// Create a complete HTML document
export function renderPageToHTML(pageData: PageData): string {
  const pageContent = renderPageToString(pageData);
  
  return `<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>${pageData.title}</title>
    <meta name="description" content="${pageData.description}">
</head>
<body>
    ${pageContent}
</body>
</html>`;
}

// For Node.js environment, make functions available globally
if (typeof global !== 'undefined') {
  (global as any).renderPageToString = renderPageToString;
  (global as any).renderPageToHTML = renderPageToHTML;
}