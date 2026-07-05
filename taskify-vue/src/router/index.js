import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const routes = [
  { path: '/login', component: () => import('@/views/LoginView.vue') },
  { path: '/register', component: () => import('@/views/RegisterView.vue') },
  { path: '/', component: () => import('@/views/HomeView.vue') },
  { path: '/catalog', component: () => import('@/views/CatalogView.vue') },
  { path: '/tasks/:id', component: () => import('@/views/TaskDetailView.vue') },
  { path: '/tasks/create', component: () => import('@/views/TaskCreateView.vue') },
  { path: '/tasks/:id/edit', component: () => import('@/views/TaskEditView.vue') },
  { path: '/profile', component: () => import('@/views/ProfileView.vue') },
  { path: '/feedback', component: () => import('@/views/FeedbackView.vue') },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach((to, from, next) => {
  const auth = useAuthStore()
  if (to.path !== '/login' && to.path !== '/register' && !auth.isAuthenticated) {
    next('/login')
  } else {
    next()
  }
})

export default router