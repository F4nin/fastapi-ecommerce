import { defineStore } from 'pinia'
import { ref } from 'vue'
import { reviewsService } from '@/api/reviews.service'
import type { Review, ReviewCreate } from '@/types'

export const useReviewsStore = defineStore('reviews', () => {
  const reviews = ref<Review[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchAll() {
    loading.value = true
    error.value = null
    try {
      const { data } = await reviewsService.getAll()
      reviews.value = data
    } catch (e: any) {
      error.value = e?.response?.data?.detail || 'Ошибка загрузки отзывов'
    } finally {
      loading.value = false
    }
  }

  async function create(data: ReviewCreate): Promise<Review | null> {
    loading.value = true
    error.value = null
    try {
      const { data: created } = await reviewsService.create(data)
      reviews.value.push(created)
      return created
    } catch (e: any) {
      error.value = e?.response?.data?.detail || 'Ошибка создания отзыва'
      return null
    } finally {
      loading.value = false
    }
  }

  async function remove(id: number): Promise<boolean> {
    loading.value = true
    error.value = null
    try {
      await reviewsService.delete(id)
      reviews.value = reviews.value.filter((r) => r.id !== id)
      return true
    } catch (e: any) {
      error.value = e?.response?.data?.detail || 'Ошибка удаления отзыва'
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    reviews,
    loading,
    error,
    fetchAll,
    create,
    remove,
  }
})
