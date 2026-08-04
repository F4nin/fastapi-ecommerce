import apiClient from './client'
import type { Category, CategoryCreate } from '@/types'

export const categoriesService = {
  getAll() {
    return apiClient.get<Category[]>('/categories/')
  },

  getById(id: number) {
    return apiClient.get<Category>(`/categories/${id}`)
  },

  create(data: CategoryCreate) {
    return apiClient.post<Category>('/categories/', data)
  },

  update(id: number, data: CategoryCreate) {
    return apiClient.put<Category>(`/categories/${id}`, data)
  },

  delete(id: number) {
    return apiClient.delete(`/categories/${id}`)
  },
}
