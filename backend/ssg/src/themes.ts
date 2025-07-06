import { Theme } from './types';

export const themes: Record<string, Theme> = {
  default: {
    name: 'Default',
    styles: {
      body: {
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif',
        lineHeight: '1.6',
        color: '#333',
        backgroundColor: '#fff',
        margin: '0',
        padding: '0'
      },
      container: {
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '0 20px'
      }
    }
  },
  dark: {
    name: 'Dark',
    styles: {
      body: {
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif',
        lineHeight: '1.6',
        color: '#fff',
        backgroundColor: '#1a1a1a',
        margin: '0',
        padding: '0'
      },
      container: {
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '0 20px'
      }
    }
  },
  modern: {
    name: 'Modern',
    styles: {
      body: {
        fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Oxygen, Ubuntu, Cantarell, sans-serif',
        lineHeight: '1.6',
        color: '#fff',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
        margin: '0',
        padding: '0'
      },
      container: {
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '0 20px'
      }
    }
  },
  minimal: {
    name: 'Minimal',
    styles: {
      body: {
        fontFamily: 'Georgia, serif',
        lineHeight: '1.6',
        color: '#333',
        backgroundColor: '#fafafa',
        margin: '0',
        padding: '0'
      },
      container: {
        maxWidth: '1200px',
        margin: '0 auto',
        padding: '0 20px'
      }
    }
  }
};