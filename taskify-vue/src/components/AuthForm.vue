<template>
  <form @submit.prevent="handleSubmit" class="mt-4">
    <div class="mb-3">
      <label for="username" class="form-label">Имя пользователя</label>
      <input
        id="username"
        v-model="username"
        type="text"
        class="form-control"
        :class="{ 'is-invalid': errorUsername }"
        placeholder="Введите логин"
        required
      />
      <div v-if="errorUsername" class="invalid-feedback">
        {{ errorUsername }}
      </div>
    </div>
    <div class="mb-3">
      <label for="password" class="form-label">Пароль</label>
      <input
        id="password"
        v-model="password"
        type="password"
        class="form-control"
        :class="{ 'is-invalid': errorPassword }"
        placeholder="Пароль"
        required
      />
      <div v-if="errorPassword" class="invalid-feedback">
        {{ errorPassword }}
      </div>
    </div>
    <div v-if="error" class="alert alert-danger">
      {{ error }}
    </div>
    <button type="submit" class="btn btn-primary w-100">Войти</button>
  </form>
</template>

<script setup>
import { ref } from 'vue'

const username = ref('')
const password = ref('')
const error = ref(null)
const errorUsername = ref('')
const errorPassword = ref('')

const emit = defineEmits(['login'])

const handleSubmit = () => {
  // Client-side validation
  errorUsername.value = ''
  errorPassword.value = ''
  error.value = null

  if (!username.value.trim()) {
    errorUsername.value = 'Введите имя пользователя'
    return
  }
  if (!password.value) {
    errorPassword.value = 'Введите пароль'
    return
  }

  emit('login', { username: username.value.trim(), password: password.value })
}
</script>