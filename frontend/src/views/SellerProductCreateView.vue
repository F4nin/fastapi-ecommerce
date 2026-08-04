<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useProductsStore } from '@/stores/products.store'
import { useCategoriesStore } from '@/stores/categories.store'
import BaseCard from '@/components/ui/BaseCard.vue'
import ProductForm from '@/components/product/ProductForm.vue'
import type { ProductCreate } from '@/types'

const router = useRouter()
const productsStore = useProductsStore()
const categoriesStore = useCategoriesStore()

onMounted(() => categoriesStore.fetchAll())

async function handleSubmit(data: ProductCreate) {
  const result = await productsStore.create(data)
  if (result) {
    router.push({ name: 'seller-dashboard' })
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">Создание товара</h1>
    <BaseCard>
      <ProductForm
        :categories="categoriesStore.categories"
        :loading="productsStore.loading"
        submit-label="Создать товар"
        @submit="handleSubmit"
      />
    </BaseCard>
  </div>
</template>
