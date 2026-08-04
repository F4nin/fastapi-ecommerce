<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProductsStore } from '@/stores/products.store'
import { useCategoriesStore } from '@/stores/categories.store'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import ProductForm from '@/components/product/ProductForm.vue'
import type { ProductCreate } from '@/types'

const route = useRoute()
const router = useRouter()
const productsStore = useProductsStore()
const categoriesStore = useCategoriesStore()

const productId = Number(route.params.id)

onMounted(async () => {
  await Promise.all([
    productsStore.fetchById(productId),
    categoriesStore.fetchAll(),
  ])
})

const initial = computed(() => {
  const p = productsStore.currentProduct
  if (!p) return undefined
  return {
    name: p.name,
    description: p.description,
    price: p.price,
    image_url: p.image_url,
    stock: p.stock,
    category_id: p.category_id,
  }
})

async function handleSubmit(data: ProductCreate) {
  const result = await productsStore.update(productId, data)
  if (result) {
    router.push({ name: 'seller-dashboard' })
  }
}
</script>

<template>
  <div class="max-w-2xl mx-auto px-4 py-8">
    <h1 class="text-2xl font-bold text-gray-900 mb-6">Редактирование товара</h1>
    <BaseSpinner v-if="productsStore.loading" />
    <BaseCard v-else-if="initial">
      <ProductForm
        :initial="initial"
        :categories="categoriesStore.categories"
        :loading="productsStore.loading"
        submit-label="Сохранить изменения"
        @submit="handleSubmit"
      />
    </BaseCard>
    <div v-else class="text-center py-16">
      <h2 class="text-xl font-semibold text-gray-900">Товар не найден</h2>
    </div>
  </div>
</template>
