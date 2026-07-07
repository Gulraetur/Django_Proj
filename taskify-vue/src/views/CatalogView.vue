<template>
  <div class="container mt-4">
    <h1>Каталог задач</h1>
    <!-- Фильтры -->
    <div class="row mb-4">
      <div class="col-md-3">
        <input v-model="filters.search" class="form-control" placeholder="Поиск по названию" @input="applyFilters" />
      </div>
      <div class="col-md-2">
        <select v-model="filters.category" class="form-select" @change="applyFilters">
          <option value="">Все категории</option>
          <option v-for="cat in categories" :key="cat" :value="cat">{{ cat }}</option>
        </select>
      </div>
      <div class="col-md-2">
        <select v-model="filters.status" class="form-select" @change="applyFilters">
          <option value="">Все статусы</option>
          <option value="search">Поиск исполнителя</option>
          <option value="work">В работе</option>
          <option value="review">Приёмка</option>
        </select>
      </div>
      <div class="col-md-2">
        <input v-model="filters.minBudget" type="number" class="form-control" placeholder="Бюджет от" @input="applyFilters" />
      </div>
      <div class="col-md-2">
        <input v-model="filters.maxBudget" type="number" class="form-control" placeholder="Бюджет до" @input="applyFilters" />
      </div>
    </div>
    <button class="btn btn-primary mb-3" @click="$router.push('/tasks/create')">
      Создать задачу
    </button>

    <div v-if="loading">Загрузка...</div>
    <div v-else>
      <TaskRow
        v-for="task in tasks"
        :key="task.id"
        :task="task"
        :showRespondButton="showRespondButton(task)"
        @respond="handleRespond"
        @edit="editTask"
        @delete="deleteTask"
      />
      <p v-if="tasks.length === 0">Нет задач, соответствующих фильтрам.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useTasksStore } from '@/stores/tasks'
import { useAuthStore } from '@/stores/auth'
import { useResponsesStore } from '@/stores/responses'
import { useRoute } from 'vue-router'
import TaskRow from '@/components/TaskRow.vue'

const tasksStore = useTasksStore()
const authStore = useAuthStore()
const responsesStore = useResponsesStore()
const route = useRoute()
const loading = ref(true)


const user = computed(() => authStore.user)
const isExecutor = computed(() => authStore.isExecutor)
const isCustomer = computed(() => authStore.isCustomer)

const tasks = computed(() => tasksStore.items)

const filters = ref({
  search: '',
  category: '',
  status: '',
  minBudget: '',
  maxBudget: '',
})

const categories = ['IT', 'Дизайн', 'Маркетинг', 'Разработка', 'Другое']

async function applyFilters() {
  loading.value = true
  const params = new URLSearchParams()
  if (filters.value.search) params.append('search', filters.value.search)
  if (filters.value.category) params.append('category', filters.value.category)
  if (filters.value.status) params.append('status', filters.value.status)
  if (filters.value.minBudget) params.append('min_budget', filters.value.minBudget)
  if (filters.value.maxBudget) params.append('max_budget', filters.value.maxBudget)
  // Не передаём role, чтобы получить все заказы
  await tasksStore.fetchTasksWithFilters(params.toString())
  loading.value = false
}

onMounted(async () => {
  const role = isExecutor.value ? 'executor' : 'customer'
  await tasksStore.fetchTasks(role)
  if (isExecutor.value) {
    await responsesStore.fetchMyResponses()
  }
  loading.value = false
  if (route.query.search) {
    filters.value.search = route.query.search
  }
  await applyFilters()
})

function handleRespond(task) {
  alert('Отклик на задачу ' + task.id)
}

const showRespondButton = (task) => {
  return isExecutor.value && 
         task.status === 'search' && 
         task.client.id !== user.value?.id && 
         !responsesStore.hasResponded(task.id)
}

function editTask(task) {
  route.push(`/tasks/${task.id}/edit`)
}

async function deleteTask(task) {
  if (confirm(`Удалить задачу "${task.title}"?`)) {
    await tasksStore.remove(task.id)
  }
}
</script>