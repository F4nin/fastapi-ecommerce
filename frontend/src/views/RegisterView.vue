<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
import RegisterForm from '@/components/auth/RegisterForm.vue'
</script>

<template>
  <div class="max-w-md mx-auto px-4 py-16">
    <BaseCard>
      <h1 class="text-2xl font-bold text-gray-900 text-center mb-6">Регистрация</h1>
      <RegisterForm />
    </BaseCard>
  </div>
</template>
