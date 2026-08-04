import { defineStore } from 'pinia'
import { ref } from 'vue'
import { productsService } from '@/api/products.service'
import type { Product, ProductCreate, Review } from '@/types'

export const useProductsStore = defineStore('products', () => {
  const products = ref<Product[]>([])
  const currentProduct = ref<Product | null>(null)
  const productReviews = ref<Review[]>([])
  const loading = ref(false)
  const error = ref<string | null>(null)

  async function fetchAll() {
    loading.value = true
    error.value = null
    try {
      const { data } = await productsService.getAll()
      products.value = data
    } catch (e: any) {
      error.value = e?.response?.data?.detail || 'Ошибка загрузки товаров'
    } finally {
      loading.value = false
    }
  }

  async function fetchById(id: number) {
    loading.value = true
    error.value = null
    try {
      const { data } = await productsService.getById(id)
      currentProduct.value = data
    } catch (e: any) {
      error.value = e?.response?.data?.detail || 'Ошибка загрузки товара'
    } finally {
      loading.value = false
    }
  }

  async function fetchByCategory(categoryId: number) {
    loading.value = true
    error.value = null
    try {
      const { data } = await productsService.getByCategory(categoryId)
      products.value = data
    } catch (e: any) {
      error.value = e?.response?.data?.detail || 'Ошибка загрузки товаров категории'
    } finally {
      loading.value = false
    }
  }

  async function fetchReviews(productId: number) {
    try {
      const { data } = await productsService.getReviews(productId)
      productReviews.value = data
    } catch {
      productReviews.value = []
    }
  }

  async function create(data: ProductCreate): Promise<Product | null> {
    loading.value = true
    error.value = null
    try {
      const { data: created } = await productsService.create(data)
      products.value.push(created)
      return created
    } catch (e: any) {
      error.value = e?.response?.data?.detail || 'Ошибка создания товара'
      return null
    } finally {
      loading.value = false
    }
  }

  async function update(id: number, data: ProductCreate): Promise<Product | null> {
    loading.value = true
    error.value = null
    try {
      const { data: updated } = await productsService.update(id, data)
      const index = products.value.findIndex((p) => p.id === id)
      if (index !== -1) products.value[index] = updated
      if (currentProduct.value?.id === id) currentProduct.value = updated
      return updated
    } catch (e: any) {
      error.value = e?.response?.data?.detail || 'Ошибка обновления товара'
      return null
    } finally {
      loading.value = false
    }
  }

  async function remove(id: number): Promise<boolean> {
    loading.value = true
    error.value = null
    try {
      await productsService.delete(id)
      products.value = products.value.filter((p) => p.id !== id)
      if (currentProduct.value?.id === id) currentProduct.value = null
      return true
    } catch (e: any) {
      error.value = e?.response?.data?.detail || 'Ошибка удаления товара'
      return false
    } finally {
      loading.value = false
    }
  }

  return {
    products,
    currentProduct,
    productReviews,
    loading,
    error,
    fetchAll,
    fetchById,
    fetchByCategory,
    fetchReviews,
    create,
    update,
    remove,
  }
})
