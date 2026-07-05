<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-5">
        <div class="card shadow-sm">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">Вход</h2>
            <AuthForm @login="handleLogin" />
            <p class="mt-3 text-center">
              Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
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
    if (e.response && e.response.status === 401) {
      alert('Неверное имя пользователя или пароль')
    } else {
      alert('Ошибка входа. Попробуйте позже.')
    }
  }
}
</script>