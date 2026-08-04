<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCategoriesStore } from '@/stores/categories.store'
import { useProductsStore } from '@/stores/products.store'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import ProductGrid from '@/components/product/ProductGrid.vue'

const route = useRoute()
const categoriesStore = useCategoriesStore()
const productsStore = useProductsStore()

const categoryId = Number(route.params.id)

onMounted(async () => {
  await Promise.all([
    categoriesStore.fetchById(categoryId),
    productsStore.fetchByCategory(categoryId),
  ])
})
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <BaseSpinner v-if="categoriesStore.loading" />
    <template v-else-if="categoriesStore.currentCategory">
      <h1 class="text-2xl font-bold text-gray-900 mb-2">
        {{ categoriesStore.currentCategory.name }}
      </h1>
      <p class="text-gray-500 mb-8">Товары в этой категории</p>
      <ProductGrid :products="productsStore.products" />
    </template>
    <div v-else class="text-center py-16">
      <h2 class="text-xl font-semibold text-gray-900">Категория не найдена</h2>
    </div>
  </div>
</template>
