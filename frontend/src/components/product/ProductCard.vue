<script setup lang="ts">
import type { Product } from '@/types'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseStarRating from '@/components/ui/BaseStarRating.vue'

defineProps<{
  product: Product
}>()
</script>

<template>
  <RouterLink :to="{ name: 'product-detail', params: { id: product.id } }" class="block group">
    <BaseCard padding="none" class="overflow-hidden hover:shadow-md transition-shadow">
      <div class="aspect-video bg-gray-100 flex items-center justify-center">
        <img
          v-if="product.image_url"
          :src="product.image_url"
          :alt="product.name"
          class="w-full h-full object-cover"
        />
        <svg
          v-else
          class="w-12 h-12 text-gray-300"
          fill="none"
          stroke="currentColor"
          viewBox="0 0 24 24"
        >
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
        </svg>
      </div>
      <div class="p-4">
        <h3 class="font-medium text-gray-900 group-hover:text-indigo-600 transition-colors line-clamp-1">
          {{ product.name }}
        </h3>
        <p v-if="product.description" class="mt-1 text-sm text-gray-500 line-clamp-2">
          {{ product.description }}
        </p>
        <div class="mt-3 flex items-center justify-between">
          <span class="text-lg font-semibold text-gray-900">
            {{ product.price.toLocaleString('ru-RU') }} ₽
          </span>
          <BaseStarRating :rating="product.rating" />
        </div>
        <div class="mt-2 flex items-center gap-2">
          <span
            class="text-xs font-medium px-2 py-0.5 rounded-full"
            :class="product.stock > 0 ? 'bg-green-100 text-green-700' : 'bg-red-100 text-red-700'"
          >
            {{ product.stock > 0 ? `В наличии: ${product.stock}` : 'Нет в наличии' }}
          </span>
        </div>
      </div>
    </BaseCard>
  </RouterLink>
</template>
