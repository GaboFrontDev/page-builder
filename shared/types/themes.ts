export interface Theme {
  name: string;
  styles: {
    body: Record<string, string>;
    container: Record<string, string>;
    [key: string]: Record<string, string>;
  };
}

export type ThemeName = 'default' | 'dark' | 'modern' | 'minimal';

export interface PageConfig {
  theme?: ThemeName;
  customStyles?: Record<string, any>;
  [key: string]: any;
}