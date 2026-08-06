<script setup lang="ts">
import { onMounted, ref, computed, watch } from 'vue'
import { useProductsStore } from '@/stores/products.store'
import { useCategoriesStore } from '@/stores/categories.store'
import ProductGrid from '@/components/product/ProductGrid.vue'
import CategoryTree from '@/components/category/CategoryTree.vue'
import BaseSpinner from '@/components/ui/BaseSpinner.vue'
import BasePagination from '@/components/ui/BasePagination.vue'
import { useDebounce } from '@/composables/useDebounce'

const productsStore = useProductsStore()
const categoriesStore = useCategoriesStore()

const selectedCategoryId = ref<number | null>(null)
const searchQuery = ref('')
const debouncedSearch = useDebounce(searchQuery, 400)
const createdAfter = ref('')
const createdBefore = ref('')
const sortBy = ref('id')
const order = ref('asc')

onMounted(async () => {
  await Promise.all([loadProducts(), categoriesStore.fetchAll()])
})

function buildFilters() {
  return {
    search: debouncedSearch.value || undefined,
    category_id: selectedCategoryId.value,
    created_after: createdAfter.value || undefined,
    created_before: createdBefore.value || undefined,
    sort_by: sortBy.value,
    order: order.value,
    page: productsStore.currentPage,
    page_size: productsStore.pageSize,
  }
}

async function loadProducts() {
  await productsStore.fetchAll(buildFilters())
}

watch([selectedCategoryId, sortBy, order, debouncedSearch], () => {
  productsStore.currentPage = 1
  loadProducts()
})

function handleCategorySelect(id: number | null) {
  selectedCategoryId.value = id
}

function handlePageChange(page: number) {
  productsStore.currentPage = page
  loadProducts()
}

function handleDateFilter() {
  productsStore.currentPage = 1
  loadProducts()
}

function clearFilters() {
  selectedCategoryId.value = null
  searchQuery.value = ''
  createdAfter.value = ''
  createdBefore.value = ''
  sortBy.value = 'id'
  order.value = 'asc'
  productsStore.currentPage = 1
  loadProducts()
}

const totalPages = computed(() => Math.ceil(productsStore.total / productsStore.pageSize) || 1)
</script>

<template>
  <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
    <h1 class="text-2xl font-bold text-gray-900 mb-8">Каталог товаров</h1>
    <div class="flex flex-col lg:flex-row gap-8">
      <aside class="lg:w-64 flex-shrink-0">
        <div class="bg-white rounded-xl border border-gray-200 p-4 space-y-6">
          <div>
            <h2 class="font-medium text-gray-900 mb-3">Категории</h2>
            <BaseSpinner v-if="categoriesStore.loading" size="sm" />
            <CategoryTree
              v-else
              :categories="categoriesStore.categories"
              :selected-id="selectedCategoryId"
              @select="handleCategorySelect"
            />
          </div>

          <div class="border-t pt-4">
            <h2 class="font-medium text-gray-900 mb-3">Дата создания</h2>
            <div class="space-y-2">
              <div>
                <label class="text-xs text-gray-500">С</label>
                <input
                  v-model="createdAfter"
                  type="date"
                  class="w-full border border-gray-300 rounded-lg px-2 py-1.5 text-sm"
                  @change="handleDateFilter"
                />
              </div>
              <div>
                <label class="text-xs text-gray-500">По</label>
                <input
                  v-model="createdBefore"
                  type="date"
                  class="w-full border border-gray-300 rounded-lg px-2 py-1.5 text-sm"
                  @change="handleDateFilter"
                />
              </div>
            </div>
          </div>

          <div class="border-t pt-4">
            <h2 class="font-medium text-gray-900 mb-3">Сортировка</h2>
            <div class="space-y-2">
              <select
                v-model="sortBy"
                class="w-full border border-gray-300 rounded-lg px-2 py-1.5 text-sm"
              >
                <option value="id">По умолчанию</option>
                <option value="created_at">По дате создания</option>
                <option value="price">По цене</option>
                <option value="rating">По рейтингу</option>
              </select>
              <select
                v-model="order"
                class="w-full border border-gray-300 rounded-lg px-2 py-1.5 text-sm"
              >
                <option value="asc">По возрастанию</option>
                <option value="desc">По убыванию</option>
              </select>
            </div>
          </div>

          <div class="border-t pt-4">
            <button
              class="w-full text-sm text-indigo-600 hover:text-indigo-800"
              @click="clearFilters"
            >
              Сбросить фильтры
            </button>
          </div>
        </div>
      </aside>

      <div class="flex-1">
        <div class="mb-4">
          <input
            v-model="searchQuery"
            type="text"
            placeholder="Поиск по названию товара..."
            class="w-full border border-gray-300 rounded-lg px-4 py-2.5 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
          />
        </div>
        <BaseSpinner v-if="productsStore.loading" />
        <template v-else>
          <p class="text-sm text-gray-500 mb-4">Всего: {{ productsStore.total }}</p>
          <ProductGrid :products="productsStore.products" />
          <div v-if="totalPages > 1" class="mt-8 flex justify-center">
            <BasePagination
              :current-page="productsStore.currentPage"
              :total-pages="totalPages"
              @update:current-page="handlePageChange"
            />
          </div>
        </template>
      </div>
    </div>
  </div>
</template>
