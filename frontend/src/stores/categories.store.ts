import { defineStore } from 'pinia'
import { ref } from 'vue'
import { categoriesService } from '@/api/categories.service'
import type { Category, CategoryCreate } from '@/types'

export const useCategoriesStore = defineStore('categories', () => {
  const categories = ref<Category[]>([])
  const currentCategory = ref<Category | null>(null)
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchAll() {
    loading.value = true
    error.value = null
    try {
      const { data } = await categoriesService.getAll()
      categories.value = data
    } catch (e: any) {
      error.value = e?.response?.data?.detail || 'Ошибка загрузки категорий'
    } finally {
      loading.value = false
    }
  }

  async function fetchById(id: number) {
    loading.value = true
    error.value = null
    try {
      const { data } = await categoriesService.getById(id)
      currentCategory.value = data
    } catch (e: any) {
      error.value = e?.response?.data?.detail || 'Ошибка загрузки категории'
    } finally {
      loading.value = false
    }
  }

  async function create(data: CategoryCreate): Promise<Category | null> {
    loading.value = true
    error.value = null
    try {
      const { data: created } = await categoriesService.create(data)
      categories.value.push(created)
      return created
    } catch (e: any) {
      error.value = e?.response?.data?.detail || 'Ошибка создания категории'
      return null
    } finally {
      loading.value = false
    }
  }

  async function update(id: number, data: CategoryCreate): Promise<Category | null> {
    loading.value = true
    error.value = null
    try {
      const { data: updated } = await categoriesService.update(id, data)
      const index = categories.value.findIndex((c) => c.id === id)
      if (index !== -1) categories.value[index] = updated
      if (currentCategory.value?.id === id) currentCategory.value = updated
      return updated
    } catch (e: any) {
      error.value = e?.response?.data?.detail || 'Ошибка обновления категории'
      return null
    } finally {
      loading.value = false
    }
  }

  async function remove(id: number): Promise<boolean> {
    loading.value = true
    error.value = null
    try {
      await categoriesService.delete(id)
      categories.value = categories.value.filter((c) => c.id !== id)
      if (currentCategory.value?.id === id) currentCategory.value = null
      return true
    } catch (e: any) {
      error.value = e?.response?.data?.detail || 'Ошибка удаления категории'
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    categories,
    currentCategory,
    loading,
    error,
    fetchAll,
    fetchById,
    create,
    update,
    remove,
  }
})
