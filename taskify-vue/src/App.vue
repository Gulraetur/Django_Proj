<template>
  <div id="app" class="d-flex flex-column min-vh-100">
    <AppHeader />
    <div class="d-flex flex-grow-1">
      <SidebarMenu />
      <main class="flex-grow-1 p-4">
        <router-view />
      </main>
      <AppFooter />
    </div>
  </div>
</template>

<script setup>
import { onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import AppHeader from '@/components/AppHeader.vue'
import AppFooter from '@/components/AppFooter.vue'
import SidebarMenu from '@/components/SidebarMenu.vue'
const authStore = useAuthStore()

onMounted(() => {
  if (authStore.token) {
    authStore.fetchUser()
  }
})
</script>