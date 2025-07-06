export interface User {
  id: number;
  email: string;
  username: string;
  is_active: boolean;
  created_at: string;
}

export interface LoginCredentials {
  email: string;
  password: string;
}

export interface RegisterCredentials {
  email: string;
  username: string;
  password: string;
}

export interface AuthResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

export interface Page {
  id: number;
  title: string;
  slug: string;
  description: string;
  config: PageConfig;
  is_published: boolean;
  created_at: string;
  updated_at: string;
  owner_id: number;
  components?: Component[];
}

export interface PageConfig {
  theme: 'default' | 'dark' | 'modern' | 'minimal';
  [key: string]: any;
}

export interface Component {
  id: number;
  type: ComponentType;
  content: ComponentContent;
  styles: ComponentStyles;
  position: number;
  is_visible: boolean;
  page_id: number;
}

export type ComponentType = 'header' | 'hero' | 'text' | 'image' | 'button' | 'footer';

export interface ComponentContent {
  [key: string]: any;
  // Header
  title?: string;
  logo?: string;
  menu_items?: MenuItem[];
  // Hero
  subtitle?: string;
  cta_text?: string;
  cta_link?: string;
  image?: string;
  // Text
  text?: string;
  alignment?: 'left' | 'center' | 'right';
  // Image
  src?: string;
  alt?: string;
  caption?: string;
  // Button
  link?: string;
  variant?: 'primary' | 'secondary' | 'success' | 'danger';
  // Footer
  links?: FooterLink[];
}

export interface MenuItem {
  text: string;
  link: string;
}

export interface FooterLink {
  text: string;
  url: string;
}

export interface ComponentStyles {
  [key: string]: any;
  backgroundColor?: string;
  color?: string;
  padding?: string;
  margin?: string;
  fontSize?: string;
  fontWeight?: string;
  borderRadius?: string;
  border?: string;
  minHeight?: string;
  maxWidth?: string;
  textAlign?: string;
}

export interface DeploymentResponse {
  message: string;
  page_id: number;
  slug: string;
  url: string;
}

export interface DeploymentStatus {
  deployed: boolean;
  slug: string;
  url?: string;
  path?: string;
}

export interface ApiError {
  detail: string;
}