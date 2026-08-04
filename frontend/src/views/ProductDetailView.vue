<script setup lang="ts">
import { onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useProductsStore } from '@/stores/products.store'
import { useReviewsStore } from '@/stores/reviews.store'
import { useAuthStore } from '@/stores/auth.store'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import BaseCard from '@/components/ui/BaseCard.vue'
import BaseStarRating from '@/components/ui/BaseStarRating.vue'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'
import ReviewCard from '@/components/review/ReviewCard.vue'
import ReviewForm from '@/components/review/ReviewForm.vue'
import type { ReviewCreate } from '@/types'

const route = useRoute()
const router = useRouter()
const productsStore = useProductsStore()
const reviewsStore = useReviewsStore()
const auth = useAuthStore()

const productId = Number(route.params.id)

onMounted(async () => {
  await Promise.all([
    productsStore.fetchById(productId),
    productsStore.fetchReviews(productId),
  ])
})

const isOwner = () => {
  return auth.isAuthenticated && auth.currentUser?.id !== undefined
}

async function handleCreateReview(data: ReviewCreate) {
  await reviewsStore.create(data)
  await productsStore.fetchReviews(productId)
}

async function handleDeleteReview(id: number) {
  await reviewsStore.remove(id)
  await productsStore.fetchReviews(productId)
}

async function handleDeleteProduct() {
  const confirmed = window.confirm('Вы уверены, что хотите удалить этот товар?')
  if (!confirmed) return
  await productsStore.remove(productId)
  router.push({ name: 'products' })
}
</script>

<template>
  <div class="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <BaseSpinner v-if="productsStore.loading" size="lg" />

    <template v-else-if="productsStore.currentProduct">
      <BaseCard>
        <div class="flex flex-col md:flex-row gap-8">
          <div class="md:w-1/2">
            <div class="aspect-square bg-gray-100 rounded-lg flex items-center justify-center">
              <img
                v-if="productsStore.currentProduct.image_url"
                :src="productsStore.currentProduct.image_url"
                :alt="productsStore.currentProduct.name"
                class="w-full h-full object-cover rounded-lg"
              />
              <svg v-else class="w-24 h-24 text-gray-300" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
            </div>
          </div>
          <div class="md:w-1/2 flex flex-col">
            <div class="flex items-start justify-between">
              <h1 class="text-2xl font-bold text-gray-900">
                {{ productsStore.currentProduct.name }}
              </h1>
              <div v-if="auth.isSeller && auth.currentUser?.id === productsStore.currentProduct.seller_id" class="flex gap-2">
                <RouterLink :to="{ name: 'seller-product-edit', params: { id: productId } }">
                  <BaseButton variant="secondary" size="sm">Редактировать</BaseButton>
                </RouterLink>
                <BaseButton variant="danger" size="sm" @click="handleDeleteProduct">Удалить</BaseButton>
              </div>
            </div>

            <BaseStarRating :rating="productsStore.currentProduct.rating" :size="'md'" class="mt-3" />

            <p class="text-3xl font-bold text-gray-900 mt-4">
              {{ productsStore.currentProduct.price.toLocaleString('ru-RU') }} ₽
            </p>

            <BaseBadge
              class="mt-3 w-fit"
              :variant="productsStore.currentProduct.stock > 0 ? 'success' : 'danger'"
            >
              {{ productsStore.currentProduct.stock > 0 ? `В наличии: ${productsStore.currentProduct.stock} шт.` : 'Нет в наличии' }}
            </BaseBadge>

            <p v-if="productsStore.currentProduct.description" class="mt-4 text-gray-600">
              {{ productsStore.currentProduct.description }}
            </p>
          </div>
        </div>
      </BaseCard>

      <div class="mt-12">
        <h2 class="text-xl font-bold text-gray-900 mb-6">
          Отзывы ({{ productsStore.productReviews.length }})
        </h2>

        <div v-if="auth.isBuyer" class="mb-6">
          <ReviewForm :product-id="productId" :loading="reviewsStore.loading" @submit="handleCreateReview" />
        </div>

        <BaseCard v-if="productsStore.productReviews.length > 0" padding="md">
          <ReviewCard
            v-for="review in productsStore.productReviews"
            :key="review.id"
            :review="review"
            :can-delete="auth.isAdmin || auth.currentUser?.id === review.user_id"
            @delete="handleDeleteReview"
          />
        </BaseCard>
        <p v-else class="text-gray-500 text-center py-8">Пока нет отзывов. Будьте первым!</p>
      </div>
    </template>

    <div v-else class="text-center py-16">
      <h2 class="text-xl font-semibold text-gray-900">Товар не найден</h2>
      <RouterLink :to="{ name: 'products' }" class="mt-4 inline-block text-indigo-600 hover:text-indigo-500">
        Вернуться в каталог
      </RouterLink>
    </div>
  </div>
</template>
