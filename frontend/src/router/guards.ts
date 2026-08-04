import type { Router } from 'vue-router'
import { useAuthStore } from '@/stores/auth.store'

export function registerGuards(router: Router) {
  router.beforeEach((to, from, next) => {
    const auth = useAuthStore()

    if (to.meta.guestOnly && auth.isAuthenticated) {
      return next({ name: 'home' })
    }

    if (to.meta.requiresAuth && !auth.isAuthenticated) {
      return next({ name: 'login', query: { redirect: to.fullPath } })
    }

    if (to.meta.role && auth.currentUser?.role !== to.meta.role) {
      return next({ name: 'home' })
    }

    next()
  })
}
