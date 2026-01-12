import axios from 'axios'
import type { 
  User, 
  LoginRequest, 
  RegisterRequest, 
  Token, 
  Resolution, 
  ResolutionCreate, 
  ResolutionUpdate 
} from '@/types'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000'

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

export const authAPI = {
  login: (data: LoginRequest): Promise<Token> =>
    api.post('/auth/login', data).then(res => res.data),
  
  register: (data: RegisterRequest): Promise<User> =>
    api.post('/auth/register', data).then(res => res.data),
  
  getCurrentUser: (): Promise<User> =>
    api.get('/auth/me').then(res => res.data),
  
  getUsers: (): Promise<User[]> =>
    api.get('/auth/users').then(res => res.data),
}

export const resolutionsAPI = {
  getResolutions: (): Promise<Resolution[]> =>
    api.get('/resolutions/').then(res => res.data),
  
  getAllResolutions: (): Promise<Resolution[]> =>
    api.get('/resolutions/all').then(res => res.data),
  
  getResolution: (id: string): Promise<Resolution> =>
    api.get(`/resolutions/${id}`).then(res => res.data),
  
  createResolution: (data: ResolutionCreate): Promise<Resolution> =>
    api.post('/resolutions/', data).then(res => res.data),
  
  updateResolution: (id: string, data: ResolutionUpdate): Promise<Resolution> =>
    api.put(`/resolutions/${id}`, data).then(res => res.data),
  
  deleteResolution: (id: string): Promise<void> =>
    api.delete(`/resolutions/${id}`).then(res => res.data),
}

export default api