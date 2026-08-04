<script setup lang="ts">
import BaseCard from '@/components/ui/BaseCard.vue'
import LoginForm from '@/components/auth/LoginForm.vue'
</script>

<template>
  <div class="max-w-md mx-auto px-4 py-16">
    <BaseCard>
      <h1 class="text-2xl font-bold text-gray-900 text-center mb-6">Вход</h1>
      <LoginForm />
    </BaseCard>
  </div>
</template>
