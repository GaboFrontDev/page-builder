import axios from 'axios';
import { 
  User, 
  LoginCredentials, 
  RegisterCredentials, 
  AuthResponse, 
  Page, 
  Component, 
  DeploymentResponse, 
  DeploymentStatus,
  DeployedSitesResponse,
  ApiError 
} from '../types';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001';

const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor para agregar token automáticamente
apiClient.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('authToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor para manejar errores
apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expirado o inválido
      localStorage.removeItem('authToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authApi = {
  login: async (credentials: LoginCredentials): Promise<AuthResponse> => {
    const response = await apiClient.post('/api/auth/login', credentials);
    return response.data;
  },

  register: async (credentials: RegisterCredentials): Promise<User> => {
    const response = await apiClient.post('/api/auth/register', credentials);
    return response.data;
  },

  getProfile: async (token?: string): Promise<User> => {
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await apiClient.get('/api/auth/me', { headers });
    return response.data;
  },

  updateProfile: async (username: string): Promise<User> => {
    const response = await apiClient.put('/api/auth/me', null, {
      params: { username }
    });
    return response.data;
  },

  changePassword: async (currentPassword: string, newPassword: string): Promise<void> => {
    await apiClient.post('/api/auth/change-password', null, {
      params: { current_password: currentPassword, new_password: newPassword }
    });
  },

  refreshToken: async (): Promise<AuthResponse> => {
    const response = await apiClient.post('/api/auth/refresh-token');
    return response.data;
  },
};

// Pages API
export const pagesApi = {
  getPages: async (): Promise<Page[]> => {
    const response = await apiClient.get('/api/pages/');
    return response.data;
  },

  getPage: async (id: number): Promise<Page> => {
    const response = await apiClient.get(`/api/pages/${id}`);
    return response.data;
  },

  createPage: async (pageData: Partial<Page>): Promise<Page> => {
    const response = await apiClient.post('/api/pages/', pageData);
    return response.data;
  },

  updatePage: async (id: number, pageData: Partial<Page>): Promise<Page> => {
    const response = await apiClient.put(`/api/pages/${id}`, pageData);
    return response.data;
  },

  deletePage: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/pages/${id}`);
  },

  publishPage: async (id: number): Promise<Page> => {
    const response = await apiClient.post(`/api/pages/${id}/publish`);
    return response.data;
  },
};

// Components API
export const componentsApi = {
  getComponents: async (pageId: number): Promise<Component[]> => {
    const response = await apiClient.get(`/api/components/page/${pageId}`);
    return response.data;
  },

  getComponent: async (id: number): Promise<Component> => {
    const response = await apiClient.get(`/api/components/${id}`);
    return response.data;
  },

  createComponent: async (pageId: number, componentData: Partial<Component>): Promise<Component> => {
    const response = await apiClient.post(`/api/components/?page_id=${pageId}`, componentData);
    return response.data;
  },

  updateComponent: async (id: number, componentData: Partial<Component>): Promise<Component> => {
    const response = await apiClient.put(`/api/components/${id}`, componentData);
    return response.data;
  },

  deleteComponent: async (id: number): Promise<void> => {
    await apiClient.delete(`/api/components/${id}`);
  },

  reorderComponents: async (pageId: number, componentIds: number[]): Promise<Component[]> => {
    const response = await apiClient.post(`/api/components/reorder`, {
      page_id: pageId,
      component_ids: componentIds
    });
    return response.data;
  },
};

// Deployment API
export const deploymentApi = {
  deployPage: async (pageId: number): Promise<DeploymentResponse> => {
    const response = await apiClient.post(`/api/deploy/${pageId}`);
    return response.data;
  },

  getDeploymentStatus: async (slug: string): Promise<DeploymentStatus> => {
    const response = await apiClient.get(`/api/deploy/status/${slug}`);
    return response.data;
  },

  undeployPage: async (pageId: number): Promise<void> => {
    await apiClient.delete(`/api/deploy/${pageId}`);
  },

  undeployPageBySlug: async (slug: string): Promise<void> => {
    await apiClient.delete(`/api/deploy/slug/${slug}`);
  },

  listDeployedSites: async (): Promise<DeployedSitesResponse> => {
    const response = await apiClient.get('/api/deploy/list');
    return response.data;
  },

  rebuildAllSites: async (): Promise<{ message: string; pages: Array<{ id: number; slug: string }> }> => {
    const response = await apiClient.post('/api/deploy/rebuild-all');
    return response.data;
  },
};

// Error handling helper
export const handleApiError = (error: any): string => {
  if (error.response?.data?.detail) {
    return error.response.data.detail;
  }
  if (error.message) {
    return error.message;
  }
  return 'An unexpected error occurred';
};