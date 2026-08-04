import apiClient from './client'
import type { Review, ReviewCreate } from '@/types'

export const reviewsService = {
  getAll() {
    return apiClient.get<Review[]>('/reviews/')
  },

  create(data: ReviewCreate) {
    return apiClient.post<Review>('/reviews/', data)
  },

  delete(id: number) {
    return apiClient.delete(`/reviews/${id}`)
  },
}
