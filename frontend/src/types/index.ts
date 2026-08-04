export interface Category {
  id: number
  name: string
  parent_id: number | null
  is_active: boolean
}

export interface CategoryCreate {
  name: string
  parent_id?: number | null
}

export interface Product {
  id: number
  name: string
  description: string | null
  price: number
  image_url: string | null
  stock: number
  category_id: number
  seller_id: number
  is_active: boolean
  rating: number
}

export interface ProductCreate {
  name: string
  description?: string | null
  price: number
  image_url?: string | null
  stock: number
  category_id: number
}

export interface User {
  id: number
  email: string
  is_active: boolean
  role: 'buyer' | 'seller' | 'admin'
}

export interface UserCreate {
  email: string
  password: string
  role?: 'buyer' | 'seller' | 'admin'
}

export interface TokenResponse {
  access_token: string
  refresh_token: string
  token_type: string
}

export interface RefreshTokenRequest {
  refresh_token: string
}

export interface Review {
  id: number
  user_id: number
  product_id: number
  comment: string | null
  comment_date: string
  grade: number
  is_active: boolean
}

export interface ReviewCreate {
  product_id: number
  comment?: string | null
  grade: number
}

export interface DeleteResponse {
  status: string
  message: string
}

export interface JwtPayload {
  sub: string
  id: number
  role: 'buyer' | 'seller' | 'admin'
  exp: number
  type: 'access' | 'refresh'
}

export interface ApiError {
  detail: string
}
