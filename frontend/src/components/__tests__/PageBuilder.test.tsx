import React from 'react';
import { render, screen } from '@testing-library/react';
import '@testing-library/jest-dom';

// Simple tests for PageBuilder logic
describe('PageBuilder Component Logic', () => {
  it('should validate component types', () => {
    const validComponentTypes = ['hero', 'text', 'image', 'button', 'header', 'footer'];
    
    const isValidComponent = (type: string): boolean => {
      return validComponentTypes.includes(type);
    };

    expect(isValidComponent('hero')).toBe(true);
    expect(isValidComponent('text')).toBe(true);
    expect(isValidComponent('invalid')).toBe(false);
  });

  it('should create component with correct structure', () => {
    interface Component {
      id: string;
      type: string;
      content: Record<string, any>;
      styles: Record<string, any>;
      position: number;
    }

    const createComponent = (type: string, position: number): Component => {
      return {
        id: `component-${Date.now()}`,
        type,
        content: {},
        styles: {},
        position
      };
    };

    const component = createComponent('hero', 1);
    
    expect(component.type).toBe('hero');
    expect(component.position).toBe(1);
    expect(component.id).toContain('component-');
    expect(typeof component.content).toBe('object');
    expect(typeof component.styles).toBe('object');
  });

  it('should sort components by position', () => {
    const components = [
      { id: '1', position: 3 },
      { id: '2', position: 1 },
      { id: '3', position: 2 }
    ];

    const sortedComponents = components.sort((a, b) => a.position - b.position);

    expect(sortedComponents[0].id).toBe('2');
    expect(sortedComponents[1].id).toBe('3');
    expect(sortedComponents[2].id).toBe('1');
  });

  it('should validate page configuration', () => {
    interface PageConfig {
      title: string;
      slug: string;
      subdomain: string;
      description?: string;
    }

    const isValidPageConfig = (config: Partial<PageConfig>): boolean => {
      return !!(config.title && config.slug && config.subdomain);
    };

    expect(isValidPageConfig({ 
      title: 'Test Page', 
      slug: 'test-page', 
      subdomain: 'test' 
    })).toBe(true);
    
    expect(isValidPageConfig({ 
      title: 'Test Page', 
      slug: 'test-page' 
    })).toBe(false);
    
    expect(isValidPageConfig({})).toBe(false);
  });
});