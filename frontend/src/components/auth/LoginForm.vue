<script setup lang="ts">
import { ref } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const auth = useAuthStore()
const router = useRouter()
const route = useRoute()

const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

async function handleSubmit() {
  error.value = ''
  loading.value = true
  try {
    await auth.login(email.value, password.value)
    const redirect = (route.query.redirect as string) || '/'
    router.push(redirect)
  } catch (e: any) {
    error.value = e?.response?.data?.detail || 'Неверный email или пароль'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <form class="space-y-4" @submit.prevent="handleSubmit">
    <div v-if="error" class="p-3 text-sm text-red-700 bg-red-50 rounded-lg border border-red-200">
      {{ error }}
    </div>
    <BaseInput v-model="email" label="Email" type="email" required placeholder="user@example.com" />
    <BaseInput v-model="password" label="Пароль" type="password" required placeholder="••••••••" />
    <BaseButton type="submit" :loading="loading" size="lg" class="w-full">
      Войти
    </BaseButton>
    <p class="text-center text-sm text-gray-500">
      Нет аккаунта?
      <RouterLink :to="{ name: 'register' }" class="text-indigo-600 hover:text-indigo-500">
        Зарегистрироваться
      </RouterLink>
    </p>
  </form>
</template>
