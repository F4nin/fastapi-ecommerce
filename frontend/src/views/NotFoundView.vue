<script setup lang="ts">
import { RouterLink } from 'vue-router'
</script>

<template>
  <div class="flex flex-col items-center justify-center py-24 text-center px-4">
    <h1 class="text-6xl font-bold text-gray-200 mb-4">404</h1>
    <h2 class="text-xl font-semibold text-gray-900 mb-2">Страница не найдена</h2>
    <p class="text-gray-500 mb-8">Возможно, страница была удалена или вы перешли по неверной ссылке.</p>
    <RouterLink
      :to="{ name: 'home' }"
      class="px-6 py-3 bg-indigo-600 text-white font-medium rounded-lg hover:bg-indigo-700 transition-colors"
    >
      На главную
    </RouterLink>
  </div>
</template>
