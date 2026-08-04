<script setup lang="ts">
defineProps<{
  size?: 'sm' | 'md' | 'lg'
}>()
</script>

<template>
  <div class="flex items-center justify-center">
    <div
      class="animate-spin rounded-full border-2 border-gray-200 border-t-indigo-600"
      :class="{
        'h-5 w-5': size === 'sm',
        'h-8 w-8': size === 'md' || !size,
        'h-12 w-12': size === 'lg',
      }"
    />
  </div>
</template>
