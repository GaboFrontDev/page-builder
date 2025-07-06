import { ComponentData } from './components';
import { PageConfig } from './themes';

export interface PageData {
  id: number;
  title: string;
  description: string;
  slug: string;
  subdomain: string;
  config: PageConfig;
  components: ComponentData[];
  is_published?: boolean;
  owner_id?: number;
  created_at?: string;
  updated_at?: string;
}