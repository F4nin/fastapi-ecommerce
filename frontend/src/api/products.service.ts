import apiClient from './client'
import type { Product, ProductCreate, ProductListResponse, ProductFilters, Review, DeleteResponse } from '@/types'

export const productsService = {
  getAll(params?: ProductFilters) {
    return apiClient.get<ProductListResponse>('/products/', { params })
  },

  getById(id: number) {
    return apiClient.get<Product>(`/products/${id}`)
  },

  getByCategory(categoryId: number) {
    return apiClient.get<Product[]>(`/products/category/${categoryId}`)
  },

  create(data: ProductCreate) {
    return apiClient.post<Product>('/products/', data)
  },

  update(id: number, data: ProductCreate) {
    return apiClient.put<Product>(`/products/${id}`, data)
  },

  delete(id: number) {
    return apiClient.delete<DeleteResponse>(`/products/${id}`)
  },

  getReviews(productId: number) {
    return apiClient.get<Review[]>(`/products/${productId}/reviews/`)
  },
}
