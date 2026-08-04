<script setup lang="ts">
import { onMounted, ref, computed } from 'vue'
import { useProductsStore } from '@/stores/products.store'
import { useCategoriesStore } from '@/stores/categories.store'
import ProductGrid from '@/components/product/ProductGrid.vue'
import CategoryTree from '@/components/category/CategoryTree.vue'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import BasePagination from '@/components/ui/BasePagination.vue'

const productsStore = useProductsStore()
const categoriesStore = useCategoriesStore()

const selectedCategoryId = ref<number | null>(null)
const currentPage = ref(1)
const perPage = 8

onMounted(async () => {
  await Promise.all([productsStore.fetchAll(), categoriesStore.fetchAll()])
})

const filteredProducts = computed(() => {
  if (selectedCategoryId.value === null) return productsStore.products
  return productsStore.products.filter((p) => p.category_id === selectedCategoryId.value)
})

const totalPages = computed(() => Math.ceil(filteredProducts.value.length / perPage) || 1)

const paginatedProducts = computed(() => {
  const start = (currentPage.value - 1) * perPage
  return filteredProducts.value.slice(start, start + perPage)
})

function handleCategorySelect(id: number | null) {
  selectedCategoryId.value = id
  currentPage.value = 1
}
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-2xl font-bold text-gray-900 mb-8">Каталог товаров</h1>
    <div class="flex flex-col lg:flex-row gap-8">
      <aside class="lg:w-64 flex-shrink-0">
        <div class="bg-white rounded-xl border border-gray-200 p-4">
          <h2 class="font-medium text-gray-900 mb-3">Категории</h2>
          <BaseSpinner v-if="categoriesStore.loading" size="sm" />
          <CategoryTree
            v-else
            :categories="categoriesStore.categories"
            :selected-id="selectedCategoryId"
            @select="handleCategorySelect"
          />
        </div>
      </aside>
      <div class="flex-1">
        <BaseSpinner v-if="productsStore.loading" />
        <template v-else>
          <ProductGrid :products="paginatedProducts" />
          <div class="mt-8 flex justify-center">
            <BasePagination v-model:current-page="currentPage" :total-pages="totalPages" />
          </div>
        </template>
      </div>
    </div>
  </div>
</template>
