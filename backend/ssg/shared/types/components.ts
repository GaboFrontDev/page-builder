export interface ComponentData {
  id: number;
  type: ComponentType;
  content: ComponentContent;
  styles: ComponentStyles;
  position: number;
  is_visible: boolean;
  page_id?: number;
}

export type ComponentType = 
  | 'hero' 
  | 'hero-intro-scroll'
  | 'text' 
  | 'image' 
  | 'button' 
  | 'header' 
  | 'footer';

export interface ComponentContent {
  // Hero component
  title?: string;
  subtitle?: string;
  image?: string;
  cta_text?: string;
  cta_link?: string;
  
  // Hero Intro Scroll component
  description?: string;
  button?: {
    label?: string;
    href?: string;
  };
  
  // Text component
  text?: string;
  alignment?: 'left' | 'center' | 'right';
  
  // Image component
  src?: string;
  alt?: string;
  caption?: string;
  
  // Button component
  link?: string;
  variant?: 'primary' | 'secondary' | 'outline' | 'success' | 'danger';
  
  // Header component
  logo?: string;
  menu_items?: Array<{
    text: string;
    link: string;
  }>;
  
  // Footer component
  links?: Array<{
    text: string;
    url: string;
  }>;
  
  // Generic properties
  [key: string]: any;
}

export interface ComponentStyles {
  // Layout
  width?: string;
  height?: string;
  margin?: string;
  padding?: string;
  
  // Typography
  fontSize?: string;
  fontWeight?: string;
  fontFamily?: string;
  color?: string;
  textAlign?: 'left' | 'center' | 'right';
  lineHeight?: string;
  
  // Background
  backgroundColor?: string;
  backgroundImage?: string;
  backgroundSize?: string;
  backgroundPosition?: string;
  
  // Border
  border?: string;
  borderRadius?: string;
  borderColor?: string;
  borderWidth?: string;
  
  // Effects
  boxShadow?: string;
  opacity?: string;
  transform?: string;
  
  // Generic CSS properties
  [key: string]: any;
}

export interface ComponentPreviewProps {
  component: ComponentData;
  theme: string;
  isEditing?: boolean;
  isPreview?: boolean;
  onClick?: () => void;
  onContentChange?: (content: ComponentContent) => void;
  onStyleChange?: (styles: ComponentStyles) => void;
}

export interface ComponentRenderProps {
  component: ComponentData;
  theme: string;
  isPreview?: boolean;
}