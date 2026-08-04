<script setup lang="ts">
defineProps<{
  padding?: 'none' | 'sm' | 'md' | 'lg'
}>()
</script>

<template>
  <div
    class="bg-white rounded-xl border border-gray-200 shadow-sm"
    :class="{
      'p-0': padding === 'none',
      'p-3': padding === 'sm',
      'p-6': padding === 'md' || !padding,
      'p-8': padding === 'lg',
    }"
  >
    <slot />
  </div>
</template>
