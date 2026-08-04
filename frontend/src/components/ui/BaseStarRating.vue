<script setup lang="ts">
defineProps<{
  rating: number
  max?: number
  size?: 'sm' | 'md' | 'lg'
}>()
</script>

<template>
  <div class="flex items-center gap-0.5">
    <svg
      v-for="i in max || 5"
      :key="i"
      class="transition-colors"
      :class="{
        'w-4 h-4': size === 'sm' || !size,
        'w-5 h-5': size === 'md',
        'w-6 h-6': size === 'lg',
        'text-yellow-400': i <= Math.round(rating),
        'text-gray-300': i > Math.round(rating),
      }"
      fill="currentColor"
      viewBox="0 0 20 20"
    >
      <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
    </svg>
    <span v-if="rating > 0" class="ml-1 text-sm text-gray-500">{{ rating.toFixed(1) }}</span>
  </div>
</template>
