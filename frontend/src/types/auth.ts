export interface User {
  id: number;
  phone_number: string;
  name: string;
  email?: string;
  state: string;
  district: string;
  village?: string;
  pincode?: string;
  latitude?: number;
  longitude?: number;
  farm_size?: number;
  primary_crops?: string;
  farming_experience?: number;
  preferred_language: string;
  is_verified: boolean;
  created_at?: string;
}

export interface LoginResponse {
  access_token: string;
  token_type: string;
  user: User;
}

export interface PhoneNumberRequest {
  phone_number: string;
}

export interface OTPVerification {
  phone_number: string;
  otp: string;
  name?: string;
  state?: string;
  district?: string;
  language?: string;
}

export interface UserRegistration {
  phone_number: string;
  name: string;
  email?: string;
  state: string;
  district: string;
  village?: string;
  pincode?: string;
  latitude?: number;
  longitude?: number;
  farm_size?: number;
  primary_crops?: string;
  farming_experience?: number;
  preferred_language: string;
}
