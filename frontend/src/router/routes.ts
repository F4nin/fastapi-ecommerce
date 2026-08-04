import type { RouteRecordRaw } from 'vue-router'

export const routes: RouteRecordRaw[] = [
  {
    path: '/',
    name: 'home',
    component: () => import('@/views/HomeView.vue'),
  },
  {
    path: '/products',
    name: 'products',
    component: () => import('@/views/ProductsView.vue'),
  },
  {
    path: '/products/:id',
    name: 'product-detail',
    component: () => import('@/views/ProductDetailView.vue'),
  },
  {
    path: '/categories',
    name: 'categories',
    component: () => import('@/views/CategoriesView.vue'),
  },
  {
    path: '/categories/:id',
    name: 'category-detail',
    component: () => import('@/views/CategoryDetailView.vue'),
  },
  {
    path: '/login',
    name: 'login',
    component: () => import('@/views/LoginView.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/register',
    name: 'register',
    component: () => import('@/views/RegisterView.vue'),
    meta: { guestOnly: true },
  },
  {
    path: '/seller',
    name: 'seller-dashboard',
    component: () => import('@/views/SellerDashboardView.vue'),
    meta: { requiresAuth: true, role: 'seller' },
  },
  {
    path: '/seller/products/new',
    name: 'seller-product-create',
    component: () => import('@/views/SellerProductCreateView.vue'),
    meta: { requiresAuth: true, role: 'seller' },
  },
  {
    path: '/seller/products/:id/edit',
    name: 'seller-product-edit',
    component: () => import('@/views/SellerProductEditView.vue'),
    meta: { requiresAuth: true, role: 'seller' },
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'not-found',
    component: () => import('@/views/NotFoundView.vue'),
  },
]
