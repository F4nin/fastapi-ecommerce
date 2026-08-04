<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const auth = useAuthStore()
const router = useRouter()

const email = ref('')
const password = ref('')
const role = ref<'buyer' | 'seller'>('buyer')
const error = ref('')
const loading = ref(false)

async function handleSubmit() {
  error.value = ''
  loading.value = true
  try {
    await auth.register({
      email: email.value,
      password: password.value,
      role: role.value,
    })
    router.push({ name: 'login' })
  } catch (e: any) {
    error.value = e?.response?.data?.detail || 'Ошибка регистрации'
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
    <BaseInput v-model="password" label="Пароль" type="password" required placeholder="Минимум 8 символов" />
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Роль</label>
      <select
        v-model="role"
        class="block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
      >
        <option value="buyer">Покупатель</option>
        <option value="seller">Продавец</option>
      </select>
    </div>
    <BaseButton type="submit" :loading="loading" size="lg" class="w-full">
      Зарегистрироваться
    </BaseButton>
    <p class="text-center text-sm text-gray-500">
      Уже есть аккаунт?
      <RouterLink :to="{ name: 'login' }" class="text-indigo-600 hover:text-indigo-500">
        Войти
      </RouterLink>
    </p>
  </form>
</template>
