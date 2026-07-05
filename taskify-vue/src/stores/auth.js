import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import { login as apiLogin, register as apiRegister, getProfile, updateProfile } from '@/api/auth'

export const useAuthStore = defineStore('auth', () => {
  const user = ref(null)
  const token = ref(localStorage.getItem('access_token') || null)

  const isAuthenticated = computed(() => !!token.value)
  const isCustomer = computed(() => user.value?.client_profile !== undefined && user.value?.client_profile !== null)
  const isExecutor = computed(() => user.value?.executor_profile !== undefined && user.value?.executor_profile !== null)

  async function login(username, password) {
    const response = await apiLogin(username, password)
    token.value = response.data.access
    localStorage.setItem('access_token', token.value)
    localStorage.setItem('refresh_token', response.data.refresh)
    await fetchUser()
  }

  async function register(data) {
    await apiRegister(data)
  }

  async function fetchUser() {
    if (!token.value) {
      user.value = null
      return
    }
    try {
      const response = await getProfile()
      user.value = response.data
    } catch (error) {
      console.error('Ошибка загрузки профиля:', error)
      // если ошибка 401 – токен недействителен
      if (error.response?.status === 401) {
        logout()
      } else {
        user.value = null
      }
    }
  }

  function logout() {
    token.value = null
    user.value = null
    localStorage.removeItem('access_token')
    localStorage.removeItem('refresh_token')
  }

  async function updateUser(data) {
    const response = await updateProfile(data)
    user.value = response.data
  }

  // При инициализации хранилища сразу загружаем пользователя, если есть токен
  // Это можно сделать с помощью эффекта, но проще вызвать fetchUser() в App.vue
  // Для автоматического вызова при создании стора используем инициализацию:
  // Но лучше вызывать в App.vue, чтобы контролировать порядок.

  return { user, token, isAuthenticated, isCustomer, isExecutor, login, register, fetchUser, logout, updateUser }
})