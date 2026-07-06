<template>
  <div v-if="task" class="container mt-4">
    <h2>Редактировать задачу</h2>
    <form @submit.prevent="update">
      <div class="mb-3">
        <label for="title" class="form-label">Название</label>
        <input id="title" v-model="form.title" class="form-control" required />
      </div>
      <div class="mb-3">
        <label for="slug" class="form-label">URL-идентификатор (slug)</label>
        <input id="slug" type="text" v-model="form.slug" class="form-control" placeholder="оставьте пустым для автогенерации" @input="onSlugInput"/>
      </div>
      <div class="mb-3">
        <label for="description" class="form-label">Описание</label>
        <textarea id="description" v-model="form.description" class="form-control" rows="3"></textarea>
      </div>
      <div class="mb-3">
        <label for="budget" class="form-label">Бюджет (₽)</label>
        <input id="budget" v-model="form.budget" type="number" class="form-control" required />
      </div>
      <div class="mb-3">
        <label for="deadline" class="form-label">Дедлайн</label>
        <input id="deadline" v-model="form.deadline" type="datetime-local" class="form-control" required />
      </div>
      <div class="mb-3">
        <label for="category" class="form-label">Категория</label>
        <input id="category" v-model="form.category" class="form-control" />
      </div>
      <div class="d-flex gap-2">
        <button type="submit" class="btn btn-primary">Сохранить</button>
        <button type="button" class="btn btn-secondary" @click="$router.push(`/tasks/${route.params.id}`)">Отмена</button>
      </div>
    </form>
  </div>
  <div v-else class="container mt-4">
    <p>Загрузка...</p>
  </div>
</template>

<script setup>
import { reactive, onMounted, ref, watch } from 'vue'
import { useTasksStore } from '@/stores/tasks'
import { useAuthStore } from '@/stores/auth'
import { useRoute, useRouter } from 'vue-router'

const store = useTasksStore()
const authStore = useAuthStore()
const route = useRoute()
const router = useRouter()
let slugManuallyChanged = false

const form = reactive({
  title: '',
  slug: '',
  description: '',
  budget: 0,
  deadline: '',
  category: ''
})

const task = ref(null)

onMounted(async () => {
  const id = route.params.id
  await store.fetchTask(id)
  task.value = store.currentTask

  const user = authStore.user
  const taskData = task.value
  if (!user || !taskData || !taskData.client || Number(user.id) !== Number(taskData.client.id)) {
    router.push(`/tasks/${id}`)
    return
  }

  if (taskData.status !== 'draft' && taskData.status !== 'search') {
    alert('Редактирование недоступно для этой задачи в текущем статусе')
    router.push(`/tasks/${id}`)
    return
  }

  Object.assign(form, {
    title: taskData.title,
    slug: taskData.slug || '',
    description: taskData.description || '',
    budget: taskData.budget,
    deadline: taskData.deadline ? taskData.deadline.slice(0, 16) : '',
    category: taskData.category || ''
  })
})

async function update() {
  try {
    await store.update(route.params.id, form)
    router.push(`/tasks/${route.params.id}`)
  } catch (e) {
    alert('Ошибка обновления: ' + (e.response?.data?.detail || e.message))
  }
}

function onTitleChange(newTitle) {
  // Если пользователь вручную не менял slug, очищаем его
  if (!slugManuallyChanged) {
    form.slug = ''
  }
}

watch(() => form.title, (newTitle, oldTitle) => {
  if (newTitle !== oldTitle) {
    onTitleChange(newTitle)
  }
})

// При ручном вводе в поле slug помечаем, что пользователь его менял
function onSlugInput() {
  slugManuallyChanged = true
}
</script>