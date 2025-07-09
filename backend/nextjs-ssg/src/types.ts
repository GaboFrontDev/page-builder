export interface Component {
  id: number;
  type: string;
  content: Record<string, unknown>;
  styles: Record<string, unknown>;
  position: number;
  is_visible: boolean;
}

export interface PageData {
  id: number;
  title: string;
  description: string;
  slug: string;
  subdomain: string;
  config: {
    theme?: string;
    [key: string]: unknown;
  };
  components: Component[];
}

export interface ComponentRenderProps {
  component: Component;
  theme?: string;
  isPreview?: boolean;
}

export type ThemeName = 'default' | 'dark' | 'minimal' | 'modern';