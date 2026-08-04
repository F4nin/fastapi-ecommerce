<script setup lang="ts">
import type { Product } from '@/types'
import ProductCard from './ProductCard.vue'
import BaseEmptyState from '@/components/ui/BaseEmptyState.vue'

defineProps<{
  products: Product[]
}>()
</script>

<template>
  <div v-if="products.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
    <ProductCard v-for="product in products" :key="product.id" :product="product" />
  </div>
  <BaseEmptyState v-else title="Товары не найдены" description="Попробуйте изменить параметры поиска" />
</template>
