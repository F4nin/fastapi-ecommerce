<script setup lang="ts">
import { computed } from 'vue'
import type { Category } from '@/types'

const props = defineProps<{
  categories: Category[]
  selectedId?: number | null
}>()

const emit = defineEmits<{
  select: [id: number | null]
}>()

interface FlatItem {
  id: number
  name: string
  depth: number
}

const flatTree = computed<FlatItem[]>(() => {
  const result: FlatItem[] = []
  const childrenMap = new Map<number | null, Category[]>()
  for (const cat of props.categories) {
    const key = cat.parent_id
    if (!childrenMap.has(key)) childrenMap.set(key, [])
    childrenMap.get(key)!.push(cat)
  }

  function walk(parentId: number | null, depth: number) {
    const children = childrenMap.get(parentId) || []
    for (const cat of children) {
      result.push({ id: cat.id, name: cat.name, depth })
      walk(cat.id, depth + 1)
    }
  }

  walk(null, 0)
  return result
})
</script>

<template>
  <div class="space-y-1">
    <button
      class="block w-full text-left px-3 py-1.5 rounded-lg text-sm font-medium transition-colors"
      :class="!selectedId ? 'bg-indigo-50 text-indigo-700' : 'text-gray-600 hover:bg-gray-50'"
      @click="emit('select', null)"
    >
      Все категории
    </button>
    <ul class="space-y-0.5">
      <li v-for="item in flatTree" :key="item.id">
        <button
          class="block w-full text-left px-3 py-1.5 rounded-lg text-sm transition-colors"
          :class="selectedId === item.id
            ? 'bg-indigo-50 text-indigo-700 font-medium'
            : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'"
          :style="{ paddingLeft: `${12 + item.depth * 16}px` }"
          @click="emit('select', item.id)"
        >
          {{ item.name }}
        </button>
      </li>
    </ul>
  </div>
</template>
