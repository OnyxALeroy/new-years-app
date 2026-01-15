export enum UserRole {
  UNAUTHENTICATED = "unauthenticated",
  USER = "user",
  ADMIN = "admin",
}

export interface User {
  id: string;
  email: string;
  username: string;
  role: UserRole;
  created_at: string;
  is_active: boolean;
}

export interface LoginRequest {
  username: string;
  password: string;
}

export interface RegisterRequest {
  username: string;
  email: string;
  password: string;
}

export interface Token {
  access_token: string;
  token_type: string;
}

export interface Participant {
  user_id: string;
  tags: string[];
  due_payment: number;
  paid_amount: number;
}

export interface Event {
  id: string;
  organizers: string[];
  locations: string[];
  description: string;
  dates: string[];
  images: string[];
  notes: string[];
  participants: Participant[];
  created_at: string;
  updated_at?: string;
}

export interface EventCreate {
  organizers: string[];
  locations: string[];
  description: string;
  dates: string[];
  images?: string[];
  notes?: string[];
  participants?: Participant[];
}

export interface EventUpdate {
  organizers?: string[];
  locations?: string[];
  description?: string;
  dates?: string[];
  images?: string[];
  notes?: string[];
  participants?: Participant[];
}
