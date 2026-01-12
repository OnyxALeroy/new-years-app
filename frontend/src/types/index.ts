export enum UserRole {
  UNAUTHENTICATED = 'unauthenticated',
  USER = 'user',
  ADMIN = 'admin'
}

export interface User {
  id: string
  email: string
  username: string
  role: UserRole
  created_at: string
  is_active: boolean
}

export interface LoginRequest {
  username: string
  password: string
}

export interface RegisterRequest {
  username: string
  email: string
  password: string
}

export interface Token {
  access_token: string
  token_type: string
}

export interface Resolution {
  id: string
  title: string
  description?: string
  user_id: string
  completed: boolean
  created_at: string
  updated_at: string
}

export interface ResolutionCreate {
  title: string
  description?: string
}

export interface ResolutionUpdate {
  title?: string
  description?: string
  completed?: boolean
}