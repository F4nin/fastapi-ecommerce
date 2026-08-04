import apiClient from './client'
import type { TokenResponse, User, UserCreate } from '@/types'

export const authService = {
  register(data: UserCreate) {
    return apiClient.post<User>('/users/', data)
  },

  login(username: string, password: string) {
    const formData = new URLSearchParams()
    formData.append('username', username)
    formData.append('password', password)

    return apiClient.post<TokenResponse>('/users/token', formData, {
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    })
  },

  refreshToken(refresh_token: string) {
    return apiClient.post<TokenResponse>('/users/refresh-token', { refresh_token })
  },
}
