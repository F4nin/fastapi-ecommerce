<script setup lang="ts">
import { ref, watch } from 'vue'
import type { ProductCreate, Category } from '@/types'
import BaseInput from '@/components/ui/BaseInput.vue'
import BaseButton from '@/components/ui/BaseButton.vue'

const props = defineProps<{
  initial?: Partial<ProductCreate>
  categories: Category[]
  loading?: boolean
  submitLabel?: string
}>()

const emit = defineEmits<{
  submit: [data: ProductCreate]
}>()

const name = ref(props.initial?.name || '')
const description = ref(props.initial?.description || '')
const price = ref(props.initial?.price || 0)
const imageUrl = ref(props.initial?.image_url || '')
const stock = ref(props.initial?.stock || 0)
const categoryId = ref(props.initial?.category_id || (props.categories[0]?.id ?? 0))

watch(
  () => props.initial,
  (val) => {
    if (val) {
      name.value = val.name || ''
      description.value = val.description || ''
      price.value = val.price || 0
      imageUrl.value = val.image_url || ''
      stock.value = val.stock || 0
      categoryId.value = val.category_id || props.categories[0]?.id || 0
    }
  },
  { immediate: true },
)

function handleSubmit() {
  emit('submit', {
    name: name.value,
    description: description.value || null,
    price: price.value,
    image_url: imageUrl.value || null,
    stock: stock.value,
    category_id: categoryId.value,
  })
}
</script>

<template>
  <form class="space-y-4" @submit.prevent="handleSubmit">
    <BaseInput v-model="name" label="Название" required placeholder="Введите название товара" />
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Описание</label>
      <textarea
        v-model="description"
        rows="4"
        placeholder="Введите описание товара"
        class="block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
      />
    </div>
    <BaseInput v-model.number="price" label="Цена" type="number" required placeholder="0.00" />
    <BaseInput v-model="imageUrl" label="URL изображения" placeholder="https://..." />
    <BaseInput v-model.number="stock" label="Остаток" type="number" required placeholder="0" />
    <div>
      <label class="block text-sm font-medium text-gray-700 mb-1">Категория</label>
      <select
        v-model.number="categoryId"
        class="block w-full rounded-lg border border-gray-300 px-3 py-2 text-sm shadow-sm focus:outline-none focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500"
      >
        <option v-for="cat in categories" :key="cat.id" :value="cat.id">
          {{ cat.name }}
        </option>
      </select>
    </div>
    <BaseButton type="submit" :loading="loading" size="lg" class="w-full">
      {{ submitLabel || 'Сохранить' }}
    </BaseButton>
  </form>
</template>
