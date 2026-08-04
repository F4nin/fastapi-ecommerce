import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { authService } from '@/api/auth.service'
import type { JwtPayload, User, UserCreate } from '@/types'

function decodeJwt(token: string): JwtPayload | null {
  try {
    const payload = token.split('.')[1]
    return JSON.parse(atob(payload))
  } catch {
    return null
  }
}

export const useAuthStore = defineStore('auth', () => {
  const accessToken = ref<string | null>(localStorage.getItem('access_token'))
  const refreshToken = ref<string | null>(localStorage.getItem('refresh_token'))

  const payload = computed<JwtPayload | null>(() => {
    if (!accessToken.value) return null
    return decodeJwt(accessToken.value)
  })

  const isAuthenticated = computed(() => {
    if (!payload.value) return false
    return payload.value.exp * 1000 > Date.now()
  })

  const currentUser = computed<Pick<JwtPayload, 'sub' | 'id' | 'role'> | null>(() => {
    if (!payload.value) return null
    return {
      sub: payload.value.sub,
      id: payload.value.id,
      role: payload.value.role,
    }
  })

  const isBuyer = computed(() => currentUser.value?.role === 'buyer')
  const isSeller = computed(() => currentUser.value?.role === 'seller')
  const isAdmin = computed(() => currentUser.value?.role === 'admin')

  function setTokens(access: string, refresh: string) {
    accessToken.value = access
    refreshToken.value = refresh
    localStorage.setItem('access_token', access)
    localStorage.setItem('refresh_token', refresh)
  }

  function clearTokens() {
    accessToken.value = null
    refreshToken.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  async function login(email: string, password: string) {
    const { data } = await authService.login(email, password)
    setTokens(data.access_token, data.refresh_token)
  }

  async function register(userData: UserCreate): Promise<User> {
    const { data } = await authService.register(userData)
    return data
  }

  function logout() {
    clearTokens()
  }

  return {
    accessToken,
    refreshToken,
    payload,
    isAuthenticated,
    currentUser,
    isBuyer,
    isSeller,
    isAdmin,
    setTokens,
    clearTokens,
    login,
    register,
    logout,
  }
})
