<template>
  <div class="container mt-4">
    <div class="row justify-content-center">
      <div class="col-md-8">
        <div class="card shadow-sm">
          <div class="card-body">
            <h2 class="card-title text-center mb-4">Создать задачу</h2>
            <form @submit.prevent="submit">
              <!-- Заголовок -->
              <div class="mb-3">
                <label for="title" class="form-label">Название</label>
                <input
                  id="title"
                  v-model="form.title"
                  type="text"
                  class="form-control"
                  :class="{ 'is-invalid': errors.title }"
                  placeholder="Введите название"
                  required
                />
                <div v-if="errors.title" class="invalid-feedback">{{ errors.title }}</div>
              </div>

              <!-- Поле для ввода слага (необязательное) -->
              <div class="mb-3">
                <label for="slug" class="form-label">URL-идентификатор (слаг)</label>
                <input
                  id="slug"
                  v-model="form.slug"
                  type="text"
                  class="form-control"
                  placeholder="например: moya-zadacha"
                />
                <div class="form-text">Оставьте пустым для автоматической генерации.</div>
              </div>

              <!-- Описание -->
              <div class="mb-3">
                <label for="description" class="form-label">Описание</label>
                <textarea
                  id="description"
                  v-model="form.description"
                  class="form-control"
                  rows="4"
                  placeholder="Опишите задачу"
                ></textarea>
              </div>

              <!-- Бюджет -->
              <div class="mb-3">
                <label for="budget" class="form-label">Бюджет (₽)</label>
                <input
                  id="budget"
                  v-model="form.budget"
                  type="number"
                  class="form-control"
                  :class="{ 'is-invalid': errors.budget }"
                  placeholder="0"
                  required
                />
                <div v-if="errors.budget" class="invalid-feedback">{{ errors.budget }}</div>
              </div>

              <!-- Дедлайн -->
              <div class="mb-3">
                <label for="deadline" class="form-label">Дедлайн</label>
                <input
                  id="deadline"
                  v-model="form.deadline"
                  type="datetime-local"
                  class="form-control"
                  :class="{ 'is-invalid': errors.deadline }"
                  required
                />
                <div v-if="errors.deadline" class="invalid-feedback">{{ errors.deadline }}</div>
              </div>

              <!-- Категория -->
              <div class="mb-3">
                <label for="category" class="form-label">Категория</label>
                <input
                  id="category"
                  v-model="form.category"
                  type="text"
                  class="form-control"
                  placeholder="Например: IT, Дизайн"
                />
              </div>

              <!-- Общая ошибка -->
              <div v-if="serverError" class="alert alert-danger">{{ serverError }}</div>

              <div class="d-flex gap-2">
                <button type="submit" class="btn btn-primary">Создать</button>
                <button type="button" class="btn btn-secondary" @click="$router.push('/')">Отмена</button>
              </div>
            </form>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useTasksStore } from '@/stores/tasks'
import { useRouter } from 'vue-router'

const tasksStore = useTasksStore()
const router = useRouter()

const form = reactive({
  title: '',
  description: '',
  budget: 0,
  deadline: '',
  category: '',
  slug: ''
})

const errors = reactive({
  title: '',
  budget: '',
  deadline: '',
})

const serverError = ref('')

function validate() {
  let valid = true
  if (!form.title.trim()) {
    errors.title = 'Название обязательно'
    valid = false
  } else {
    errors.title = ''
  }

  if (form.budget <= 0) {
    errors.budget = 'Бюджет должен быть больше 0'
    valid = false
  } else {
    errors.budget = ''
  }

  if (!form.deadline) {
    errors.deadline = 'Укажите дедлайн'
    valid = false
  } else {
    errors.deadline = ''
  }

  return valid
}

async function submit() {
  serverError.value = ''
  if (!validate()) return

  try {
    const task = await tasksStore.create(form)
    router.push(`/tasks/${task.id}`)
  } catch (e) {
    if (e.response && e.response.status === 400) {
      const data = e.response.data
      if (data.title) errors.title = data.title[0]
      if (data.budget) errors.budget = data.budget[0]
      if (data.deadline) errors.deadline = data.deadline[0]
      if (data.non_field_errors) serverError.value = data.non_field_errors[0]
    } else {
      serverError.value = 'Ошибка создания задачи. Попробуйте позже.'
    }
  }
}
</script>