<script setup lang="ts">
import type { Review } from '@/types'
import ReviewCard from './ReviewCard.vue'
import BaseEmptyState from '@/components/ui/BaseEmptyState.vue'

defineProps<{
  reviews: Review[]
  canDelete?: (review: Review) => boolean
}>()

defineEmits<{
  delete: [id: number]
}>()
</script>

<template>
  <div v-if="reviews.length > 0" class="space-y-1">
    <ReviewCard
      v-for="review in reviews"
      :key="review.id"
      :review="review"
      :can-delete="canDelete?.(review)"
      @delete="$emit('delete', $event)"
    />
  </div>
  <BaseEmptyState v-else title="Нет отзывов" />
</template>
