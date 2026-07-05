<template>
  <div class="container mt-5">
    <h1>Добро пожаловать, {{ authStore.user?.username || 'Гость' }}!</h1>
    <p>Найдите подходящие задачи или опубликуйте свою.</p>
    <div class="row mt-4">
      <div class="col-md-8 mx-auto">
        <form @submit.prevent="search">
          <div class="input-group">
            <input v-model="searchQuery" type="text" class="form-control" placeholder="Поиск задач..." />
            <button class="btn btn-primary" type="submit">Найти</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()
const searchQuery = ref('')

function search() {
  if (searchQuery.value.trim()) {
    router.push({ path: '/catalog', query: { search: searchQuery.value } })
  } else {
    router.push('/catalog')
  }
}
</script>