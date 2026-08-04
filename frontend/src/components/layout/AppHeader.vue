<script setup lang="ts">
import { RouterLink, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import BaseButton from '@/components/ui/BaseButton.vue'

const auth = useAuthStore()
const router = useRouter()

function handleLogout() {
  auth.logout()
  router.push({ name: 'home' })
}
</script>

<template>
  <header class="bg-white border-b border-gray-200 sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex items-center justify-between h-16">
        <div class="flex items-center gap-8">
          <RouterLink :to="{ name: 'home' }" class="text-xl font-bold text-indigo-600">
            Магазин
          </RouterLink>
          <nav class="hidden md:flex items-center gap-6">
            <RouterLink
              :to="{ name: 'products' }"
              class="text-sm text-gray-600 hover:text-gray-900 transition-colors"
            >
              Товары
            </RouterLink>
            <RouterLink
              :to="{ name: 'categories' }"
              class="text-sm text-gray-600 hover:text-gray-900 transition-colors"
            >
              Категории
            </RouterLink>
          </nav>
        </div>
        <div class="flex items-center gap-3">
          <template v-if="auth.isAuthenticated">
            <RouterLink
              v-if="auth.isSeller"
              :to="{ name: 'seller-dashboard' }"
              class="text-sm text-gray-600 hover:text-gray-900"
            >
              Дашборд
            </RouterLink>
            <span class="text-sm text-gray-500">{{ auth.currentUser?.sub }}</span>
            <BaseButton variant="ghost" size="sm" @click="handleLogout">
              Выйти
            </BaseButton>
          </template>
          <template v-else>
            <RouterLink :to="{ name: 'login' }">
              <BaseButton variant="ghost" size="sm">Войти</BaseButton>
            </RouterLink>
            <RouterLink :to="{ name: 'register' }">
              <BaseButton size="sm">Регистрация</BaseButton>
            </RouterLink>
          </template>
        </div>
      </div>
    </div>
  </header>
</template>
