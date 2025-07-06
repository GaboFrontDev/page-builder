export interface ComponentData {
  id: number;
  type: string;
  content: Record<string, any>;
  styles: Record<string, any>;
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
    [key: string]: any;
  };
  components: ComponentData[];
}

export interface Theme {
  name: string;
  styles: {
    body: Record<string, string>;
    container: Record<string, string>;
    [key: string]: Record<string, string>;
  };
}