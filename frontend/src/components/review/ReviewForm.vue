<script setup lang="ts">
import { ref } from 'vue'
import type { ReviewCreate } from '@/types'
import BaseButton from '@/components/ui/BaseButton.vue'

const props = defineProps<{
  productId: number
  loading?: boolean
}>()

const emit = defineEmits<{
  submit: [data: ReviewCreate]
}>()

const comment = ref('')
const grade = ref(5)

function handleSubmit() {
  emit('submit', {
    product_id: props.productId,
    comment: comment.value || null,
    grade: grade.value,
  })
  comment.value = ''
  grade.value = 5
}
</script>

<template>
  <form class="space-y-3" @submit.prevent="handleSubmit">
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Оценка</label>
      <div class="flex gap-1">
        <button
          v-for="i in 5"
          :key="i"
          type="button"
          class="transition-colors"
          @click="grade = i"
        >
          <svg
            class="w-6 h-6"
            :class="i <= grade ? 'text-yellow-400' : 'text-gray-300'"
            fill="currentColor"
            viewBox="0 0 20 20"
          >
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        </button>
      </div>
    </div>
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Комментарий</label>
      <textarea
        v-model="comment"
        rows="3"
        placeholder="Поделитесь своим мнением..."
        class="block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
      />
    </div>
    <BaseButton type="submit" :loading="loading" size="sm">
      Оставить отзыв
    </BaseButton>
  </form>
</template>
