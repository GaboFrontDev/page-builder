// Modern components that use shared components and centralized logic
export { default as ModernPageBuilder } from './ModernPageBuilder';
export { default as ModernComponentEditor } from './ModernComponentEditor';
export { default as SharedComponentPreview } from './SharedComponentPreview';

// Re-export shared components for convenience
export { ComponentRenderer } from '@shared/index';
export * from '@shared/utils/componentDefaults';
export * from '@shared/themes';