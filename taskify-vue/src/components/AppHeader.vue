<template>
  <header class="bg-light border-bottom">
    <div class="container-fluid d-flex justify-content-between align-items-center py-2">
      <router-link class="navbar-brand h1 mb-0" to="/">Taskify</router-link>
      <div v-if="authStore.isAuthenticated">
        <span class="me-2">{{ authStore.user?.username || 'Пользователь' }}</span>
        <button class="btn btn-outline-secondary btn-sm" @click="logout">Выйти</button>
      </div>
      <div v-else>
        <router-link to="/login" class="btn btn-outline-primary btn-sm">Войти</router-link>
      </div>
    </div>
  </header>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const logout = () => {
  authStore.logout()
  router.push('/login')
}
</script>