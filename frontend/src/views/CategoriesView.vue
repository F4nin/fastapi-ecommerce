<script setup lang="ts">
import { onMounted } from 'vue'
import { useCategoriesStore } from '@/stores/categories.store'
import CategoryCard from '@/components/category/CategoryCard.vue'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import BaseEmptyState from '@/components/ui/BaseEmptyState.vue'

const store = useCategoriesStore()

onMounted(() => store.fetchAll())
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-2xl font-bold text-gray-900 mb-8">Категории</h1>
    <BaseSpinner v-if="store.loading" />
    <div v-else-if="store.categories.length > 0" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
      <CategoryCard v-for="cat in store.categories" :key="cat.id" :category="cat" />
    </div>
    <BaseEmptyState v-else title="Категории не найдены" />
  </div>
</template>
