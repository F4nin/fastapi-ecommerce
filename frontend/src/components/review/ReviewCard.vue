<script setup lang="ts">
import type { Review } from '@/types'
import BaseStarRating from '@/components/ui/BaseStarRating.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

defineProps<{
  review: Review
  canDelete?: boolean
}>()

defineEmits<{
  delete: [id: number]
}>()
</script>

<template>
  <div class="border-b border-gray-100 pb-4 last:border-b-0">
    <div class="flex items-start justify-between">
      <div>
        <div class="flex items-center gap-2">
          <BaseStarRating :rating="review.grade" />
          <BaseBadge variant="info">Пользователь #{{ review.user_id }}</BaseBadge>
        </div>
        <p v-if="review.comment" class="mt-2 text-sm text-gray-700">{{ review.comment }}</p>
        <p class="mt-1 text-xs text-gray-400">
          {{ new Date(review.comment_date).toLocaleDateString('ru-RU', { day: 'numeric', month: 'long', year: 'numeric' }) }}
        </p>
      </div>
      <BaseButton
        v-if="canDelete"
        variant="ghost"
        size="sm"
        @click="$emit('delete', review.id)"
      >
        <svg class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
        </svg>
      </BaseButton>
    </div>
  </div>
</template>
