<script setup lang="ts">
import type { Category } from '@/types'
import BaseCard from '@/components/ui/BaseCard.vue'

defineProps<{
  category: Category
}>()
</script>

<template>
  <RouterLink :to="{ name: 'category-detail', params: { id: category.id } }" class="block group">
    <BaseCard padding="md" class="hover:shadow-md transition-shadow text-center">
      <h3 class="font-medium text-gray-900 group-hover:text-indigo-600 transition-colors">
        {{ category.name }}
      </h3>
    </BaseCard>
  </RouterLink>
</template>
