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

// Import shared types for re-export
export type { 
  ComponentData as Component,
  ComponentType,
  ComponentContent,
  ComponentStyles,
  PageConfig,
  ThemeName
} from '@shared/index';

// Import types for local use
import type { PageData, PageConfig, ComponentData } from '@shared/index';

// Frontend-specific extension of PageData
export interface Page extends Omit<PageData, 'config' | 'components'> {
  config: PageConfig;
  is_published: boolean;
  created_at: string;
  updated_at: string;
  owner_id: number;
  components?: ComponentData[];
}

// Re-export PageData as well
export type { PageData } from '@shared/index';

export interface MenuItem {
  text: string;
  link: string;
}

export interface FooterLink {
  text: string;
  url: string;
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

export interface DeployedSite {
  slug: string;
  url: string;
  path: string;
  is_owner: boolean;
  page_id?: number;
  title?: string;
}

export interface DeployedSitesResponse {
  deployed_sites: DeployedSite[];
}

export interface ApiError {
  detail: string;
}