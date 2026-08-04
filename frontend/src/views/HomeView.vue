<script setup lang="ts">
import { onMounted, ref } from 'vue'
import { useProductsStore } from '@/stores/products.store'
import ProductGrid from '@/components/product/ProductGrid.vue'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import { RouterLink } from 'vue-router'

const productsStore = useProductsStore()
const featured = ref<typeof productsStore.products>([])

onMounted(async () => {
  await productsStore.fetchAll()
  featured.value = productsStore.products.slice(0, 4)
})
</script>

<template>
  <div>
    <section class="bg-gradient-to-br from-indigo-50 to-white">
      <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-20 text-center">
        <h1 class="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
          Добро пожаловать в интернет-магазин
        </h1>
        <p class="text-lg text-gray-600 mb-8 max-w-2xl mx-auto">
          Найдите лучшие товары по отличным ценам. Присоединяйтесь как покупатель или начните продавать сами.
        </p>
        <div class="flex items-center justify-center gap-4">
          <RouterLink
            :to="{ name: 'products' }"
            class="px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors"
          >
            Смотреть товары
          </RouterLink>
          <RouterLink
            :to="{ name: 'categories' }"
            class="px-6 py-3 bg-white text-gray-700 font-medium rounded-lg border border-gray-300 hover:bg-gray-50 transition-colors"
          >
            Категории
          </RouterLink>
        </div>
      </div>
    </section>

    <section class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-16">
      <h2 class="text-2xl font-bold text-gray-900 mb-8">Популярные товары</h2>
      <BaseSpinner v-if="productsStore.loading" />
      <ProductGrid v-else :products="featured" />
    </section>
  </div>
</template>
