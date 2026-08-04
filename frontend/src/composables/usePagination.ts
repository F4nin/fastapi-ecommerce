import { ref, computed, type Ref } from 'vue'

export function usePagination<T>(items: Ref<T[]>, perPage: number = 10) {
  const currentPage = ref(1)

  const totalPages = computed(() => Math.ceil(items.value.length / perPage) || 1)

  const paginatedItems = computed(() => {
    const start = (currentPage.value - 1) * perPage
    return items.value.slice(start, start + perPage)
  })

  function goTo(page: number) {
    if (page >= 1 && page <= totalPages.value) {
      currentPage.value = page
    }
  }

  function reset() {
    currentPage.value = 1
  }

  return {
    currentPage,
    totalPages,
    paginatedItems,
    goTo,
    reset,
  }
}
