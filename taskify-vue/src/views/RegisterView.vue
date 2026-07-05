<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">Регистрация</h2>
            <form @submit.prevent="handleRegister">
              <!-- Username -->
              <div class="mb-3">
                <label for="username" class="form-label">Имя пользователя</label>
                <input
                  id="username"
                  v-model="form.username"
                  type="text"
                  class="form-control"
                  :class="{ 'is-invalid': errors.username }"
                  placeholder="Введите логин"
                  required
                />
                <div v-if="errors.username" class="invalid-feedback">
                  {{ errors.username }}
                </div>
              </div>

              <!-- Email -->
              <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input
                  id="email"
                  v-model="form.email"
                  type="email"
                  class="form-control"
                  :class="{ 'is-invalid': errors.email }"
                  placeholder="example@mail.ru"
                  required
                />
                <div v-if="errors.email" class="invalid-feedback">
                  {{ errors.email }}
                </div>
              </div>

              <!-- Пароль -->
              <div class="mb-3">
                <label for="password" class="form-label">Пароль</label>
                <input
                  id="password"
                  v-model="form.password"
                  type="password"
                  class="form-control"
                  :class="{ 'is-invalid': errors.password }"
                  placeholder="Минимум 8 символов"
                  required
                />
                <div v-if="errors.password" class="invalid-feedback">
                  {{ errors.password }}
                </div>
              </div>

              <!-- Подтверждение пароля -->
              <div class="mb-3">
                <label for="password2" class="form-label">Подтверждение пароля</label>
                <input
                  id="password2"
                  v-model="form.password2"
                  type="password"
                  class="form-control"
                  :class="{ 'is-invalid': errors.password2 }"
                  placeholder="Повторите пароль"
                  required
                />
                <div v-if="errors.password2" class="invalid-feedback">
                  {{ errors.password2 }}
                </div>
              </div>

              <!-- Имя -->
              <div class="mb-3">
                <label for="first_name" class="form-label">Имя</label>
                <input
                  id="first_name"
                  v-model="form.first_name"
                  type="text"
                  class="form-control"
                  placeholder="Имя"
                />
              </div>

              <!-- Фамилия -->
              <div class="mb-3">
                <label for="last_name" class="form-label">Фамилия</label>
                <input
                  id="last_name"
                  v-model="form.last_name"
                  type="text"
                  class="form-control"
                  placeholder="Фамилия"
                />
              </div>

              <div class="mb-3">
                <label class="form-label">Роль</label>
                <div>
                  <div class="form-check form-check-inline">
                    <input
                      class="form-check-input"
                      type="radio"
                      id="roleCustomer"
                      value="customer"
                      v-model="form.role"
                    />
                    <label class="form-check-label" for="roleCustomer">Заказчик</label>
                  </div>
                  <div class="form-check form-check-inline">
                    <input
                      class="form-check-input"
                      type="radio"
                      id="roleExecutor"
                      value="executor"
                      v-model="form.role"
                    />
                    <label class="form-check-label" for="roleExecutor">Исполнитель</label>
                  </div>
                </div>
              </div>

              <!-- Общая ошибка -->
              <div v-if="serverError" class="alert alert-danger">
                {{ serverError }}
              </div>

              <button type="submit" class="btn btn-primary w-100">Зарегистрироваться</button>
            </form>
            <p class="mt-3 text-center">
              Уже есть аккаунт? <router-link to="/login">Войти</router-link>
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'

const authStore = useAuthStore()
const router = useRouter()

const form = reactive({
  username: '',
  email: '',
  password: '',
  password2: '',
  first_name: '',
  last_name: '',
  role: 'customer',
})

const errors = reactive({
  username: '',
  email: '',
  password: '',
  password2: '',
})

const serverError = ref('')

function validate() {
  let valid = true
  // Username
  if (!form.username.trim()) {
    errors.username = 'Имя пользователя обязательно'
    valid = false
  } else if (form.username.length < 3) {
    errors.username = 'Имя пользователя должно содержать минимум 3 символа'
    valid = false
  } else {
    errors.username = ''
  }

  // Email
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/
  if (!form.email.trim()) {
    errors.email = 'Email обязателен'
    valid = false
  } else if (!emailRegex.test(form.email)) {
    errors.email = 'Введите корректный email'
    valid = false
  } else {
    errors.email = ''
  }

  // Password
  if (!form.password) {
    errors.password = 'Пароль обязателен'
    valid = false
  } else if (form.password.length < 8) {
    errors.password = 'Пароль должен содержать минимум 8 символов'
    valid = false
  } else {
    errors.password = ''
  }

  // Password2
  if (!form.password2) {
    errors.password2 = 'Подтвердите пароль'
    valid = false
  } else if (form.password !== form.password2) {
    errors.password2 = 'Пароли не совпадают'
    valid = false
  } else {
    errors.password2 = ''
  }

  return valid
}

async function handleRegister() {
  serverError.value = ''
  if (!validate()) return

  try {
    await authStore.register(form)
    router.push('/login')
  } catch (e) {
    if (e.response && e.response.status === 400) {
      const data = e.response.data
      if (data.username) {
        errors.username = data.username[0]
      }
      if (data.email) {
        errors.email = data.email[0]
      }
      if (data.password) {
        errors.password = data.password[0]
      }
      if (data.non_field_errors) {
        serverError.value = data.non_field_errors[0]
      }
      if (!serverError.value && !Object.values(errors).some(v => v)) {
        serverError.value = 'Ошибка регистрации. Проверьте введённые данные.'
      }
    } else {
      serverError.value = 'Ошибка сервера. Попробуйте позже.'
    }
  }
}
</script>