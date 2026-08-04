<script setup lang="ts">
import { computed } from 'vue'

const props = defineProps<{
  currentPage: number
  totalPages: number
}>()

const emit = defineEmits<{
  'update:currentPage': [page: number]
}>()

const pages = computed(() => {
  const items: (number | '...')[] = []
  const p = props.currentPage
  const t = props.totalPages

  if (t <= 7) {
    for (let i = 1; i <= t; i++) items.push(i)
    return items
  }

  items.push(1)
  if (p > 3) items.push('...')

  for (let i = Math.max(2, p - 1); i <= Math.min(t - 1, p + 1); i++) {
    items.push(i)
  }

  if (p < t - 2) items.push('...')
  items.push(t)

  return items
})
</script>

<template>
  <nav v-if="totalPages > 1" class="flex items-center gap-1">
    <button
      :disabled="currentPage === 1"
      class="px-3 py-1.5 text-sm rounded-lg border hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      @click="emit('update:currentPage', currentPage - 1)"
    >
      Назад
    </button>
    <template v-for="item in pages" :key="item">
      <span v-if="item === '...'" class="px-2 text-gray-400">...</span>
      <button
        v-else
        class="px-3 py-1.5 text-sm rounded-lg border"
        :class="item === currentPage ? 'bg-indigo-600 text-white border-indigo-600' : 'hover:bg-gray-50'"
        @click="emit('update:currentPage', item)"
      >
        {{ item }}
      </button>
    </template>
    <button
      :disabled="currentPage === totalPages"
      class="px-3 py-1.5 text-sm rounded-lg border hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
      @click="emit('update:currentPage', currentPage + 1)"
    >
      Вперёд
    </button>
  </nav>
</template>
