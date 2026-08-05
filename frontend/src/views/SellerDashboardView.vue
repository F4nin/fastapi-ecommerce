<script setup lang="ts">
import { onMounted, computed } from 'vue'
import { useAuthStore } from '@/stores/auth.store'
import { useProductsStore } from '@/stores/products.store'
import BaseButton from '@/components/ui/BaseButton.vue'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import BaseEmptyState from '@/components/ui/BaseEmptyState.vue'
import BaseBadge from '@/components/ui/BaseBadge.vue'

const auth = useAuthStore()
const productsStore = useProductsStore()

onMounted(() => productsStore.fetchAll({ seller_id: auth.currentUser?.id, page_size: 100 }))

const myProducts = computed(() => productsStore.products)

async function handleDelete(id: number) {
  if (!confirm('Удалить этот товар?')) return
  await productsStore.remove(id)
}
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <div class="flex items-center justify-between mb-8">
      <h1 class="text-2xl font-bold text-gray-900">Дашборд продавца</h1>
      <RouterLink :to="{ name: 'seller-product-create' }">
        <BaseButton>Добавить товар</BaseButton>
      </RouterLink>
    </div>

    <BaseSpinner v-if="productsStore.loading" />

    <template v-else-if="myProducts.length > 0">
      <div class="overflow-x-auto">
        <table class="w-full bg-white rounded-xl border border-gray-200">
          <thead class="bg-gray-50 border-b">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Товар</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Цена</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Остаток</th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase">Рейтинг</th>
              <th class="px-6 py-3 text-right text-xs font-medium text-gray-500 uppercase">Действия</th>
            </tr>
          </thead>
          <tbody class="divide-y divide-gray-200">
            <tr v-for="product in myProducts" :key="product.id" class="hover:bg-gray-50">
              <td class="px-6 py-4">
                <div class="font-medium text-gray-900">{{ product.name }}</div>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">
                {{ product.price.toLocaleString('ru-RU') }} ₽
              </td>
              <td class="px-6 py-4">
                <BaseBadge :variant="product.stock > 0 ? 'success' : 'danger'">
                  {{ product.stock }}
                </BaseBadge>
              </td>
              <td class="px-6 py-4 text-sm text-gray-600">{{ product.rating.toFixed(1) }}</td>
              <td class="px-6 py-4 text-right">
                <div class="flex items-center justify-end gap-2">
                  <RouterLink :to="{ name: 'seller-product-edit', params: { id: product.id } }">
                    <BaseButton variant="secondary" size="sm">Изменить</BaseButton>
                  </RouterLink>
                  <BaseButton variant="danger" size="sm" @click="handleDelete(product.id)">Удалить</BaseButton>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </template>

    <BaseEmptyState v-else title="У вас пока нет товаров" description="Нажмите «Добавить товар», чтобы создать первый товар" />
  </div>
</template>
