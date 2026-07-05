<template>
  <div>
    <h2>Вход</h2>
    <AuthForm @login="handleLogin" />
    <p class="mt-3">Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link></p>
  </div>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import AuthForm from '@/components/AuthForm.vue'

const authStore = useAuthStore()
const router = useRouter()

async function handleLogin(credentials) {
  try {
    await authStore.login(credentials.username, credentials.password)
    router.push('/')
  } catch (e) {
    alert('Ошибка входа')
    console.error(e)
  }
}
</script>