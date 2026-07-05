<template>
  <div v-if="task" class="container mt-4">
    <h2>{{ task.title }}</h2>
    <div class="row mt-3">
      <div class="col-md-8">
        <p><strong>Описание:</strong> {{ task.description }}</p>
        <p><strong>Бюджет:</strong> {{ task.budget }} ₽</p>
        <p><strong>Статус:</strong> {{ task.status }}</p>
        <p><strong>Дедлайн:</strong> {{ new Date(task.deadline).toLocaleString() }}</p>
        <p><strong>Категория:</strong> {{ task.category }}</p>
        <p><strong>Заказчик:</strong> {{ task.client?.username || 'Не указан' }}</p>
        <p><strong>Исполнитель:</strong> {{ task.executor?.username || 'Не назначен' }}</p>
        <p><strong>Создан:</strong> {{ new Date(task.created_at).toLocaleString() }}</p>
      </div>
    </div>

    <!-- Кнопки для заказчика (владельца) -->
    <div v-if="isCustomer && task.client && user && Number(task.client.id) === Number(user.id)" class="mt-3">
      <button v-if="task.status === 'draft' || task.status === 'search'" 
              class="btn btn-primary me-2" 
              @click="$router.push(`/tasks/${task.id}/edit`)">
        Редактировать
      </button>
      <button v-if="task.status === 'draft' || task.status === 'search'" 
              class="btn btn-danger" 
              @click="deleteTask">
        Удалить
      </button>
    </div>

    <!-- Кнопка отклика (для исполнителя, если он не владелец и задача в поиске) -->
    <div v-if="isExecutor && task.status === 'search' && task.client && user && Number(task.client.id) !== Number(user.id)" class="mt-3">
      <button class="btn btn-success" @click="openResponseModal">Откликнуться</button>
    </div>

    <!-- Блок для исполнителя: сдать результат -->
    <div v-if="isExecutor && task.status === 'work' && task.executor && user && Number(task.executor.id) === Number(user.id)" class="mt-4">
      <h4>Сдать результат</h4>
      <form @submit.prevent="submitResult">
        <div class="mb-3">
          <label for="resultTitle" class="form-label">Название</label>
          <input id="resultTitle" v-model="resultTitle" class="form-control" placeholder="Название файла/результата" required />
        </div>
        <div class="mb-3">
          <label for="resultFile" class="form-label">Файл</label>
          <input id="resultFile" type="file" class="form-control" @change="handleFileUpload" />
        </div>
        <div class="mb-3">
          <label for="resultUrl" class="form-label">Или ссылка</label>
          <input id="resultUrl" v-model="resultUrl" class="form-control" placeholder="https://..." />
        </div>
        <button type="submit" class="btn btn-success">Отправить результат</button>
      </form>
    </div>

    <!-- Отображение материалов (для всех) -->
    <div v-if="materials.length > 0" class="mt-4">
      <h4>Результаты</h4>
      <ul class="list-group">
        <li v-for="mat in materials" :key="mat.id" class="list-group-item">
          <strong>{{ mat.title }}</strong>
          <span v-if="mat.result_file"><a :href="mat.result_file" target="_blank">Скачать файл</a></span>
          <span v-if="mat.url"><a :href="mat.url" target="_blank">Открыть ссылку</a></span>
          <span class="text-muted ms-2">{{ new Date(mat.created_at).toLocaleString() }}</span>
        </li>
      </ul>
    </div>

    <!-- Блок для заказчика: принять/доработка -->
    <div v-if="isCustomer && task.status === 'review' && task.client && user && Number(task.client.id) === Number(user.id)" class="mt-4">
      <button class="btn btn-success me-2" @click="acceptTask">Подтвердить выполнение</button>
      <button class="btn btn-warning" @click="requestRevision">Отправить на доработку</button>
    </div>

    <!-- Отображение откликов (для заказчика – владельца) -->
    <div v-if="isCustomer && task.client && user && Number(task.client.id) === Number(user.id)" class="mt-4">
      <h3>Отклики</h3>
      <div v-if="responses.length === 0">Нет откликов</div>
      <div v-for="resp in responses" :key="resp.id" class="border-bottom py-2">
        <strong>{{ resp.executor?.username }}</strong>
        <span class="text-muted ms-2">Статус: {{ resp.status }}</span>
        <span class="float-end">{{ resp.proposed_price }} ₽</span>
        <div v-if="resp.comment" class="text-muted small">{{ resp.comment }}</div>
        <div v-if="task.status === 'search' && resp.status === 'pending'">
          <button class="btn btn-success btn-sm me-1" @click="acceptResponse(resp.id)">Принять</button>
          <button class="btn btn-danger btn-sm" @click="rejectResponse(resp.id)">Отклонить</button>
        </div>
      </div>
    </div>

    <!-- Модальное окно для отклика -->
    <div v-if="showModal" class="modal-overlay" @click.self="closeModal">
      <div class="modal-content">
        <h4>Откликнуться на задачу</h4>
        <p><strong>{{ task.title }}</strong></p>
        <div class="mb-3">
          <label for="comment" class="form-label">Сопроводительное письмо</label>
          <textarea id="comment" v-model="responseComment" class="form-control" rows="4" placeholder="Опишите, почему вы подходите для этой задачи..."></textarea>
        </div>
        <div class="d-flex justify-content-end gap-2">
          <button class="btn btn-secondary" @click="closeModal">Отмена</button>
          <button class="btn btn-primary" @click="submitResponse">Отправить</button>
        </div>
      </div>
    </div>
  </div>
  <div v-else class="container mt-4">
    <p>Загрузка...</p>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useTasksStore } from '@/stores/tasks'
import api from '@/api/axios'

const route = useRoute()
const router = useRouter()
const authStore = useAuthStore()
const tasksStore = useTasksStore()

const task = computed(() => tasksStore.currentTask)
const responses = computed(() => tasksStore.responses)
const isCustomer = computed(() => authStore.isCustomer)
const isExecutor = computed(() => authStore.isExecutor)
const user = computed(() => authStore.user)

const showModal = ref(false)
const responseComment = ref('')

// Для сдачи результата
const materials = ref([])
const resultTitle = ref('')
const resultFile = ref(null)
const resultUrl = ref('')

onMounted(async () => {
  const id = route.params.id
  await tasksStore.fetchTask(id)
  await fetchMaterials(id)
  // Если заказчик – загружаем отклики
  if (isCustomer.value && task.value && task.value.client && user.value && Number(task.value.client.id) === Number(user.value.id)) {
    await tasksStore.fetchResponses(id)
  }
})

// --- Отклики ---
function openResponseModal() {
  responseComment.value = ''
  showModal.value = true
}

function closeModal() {
  showModal.value = false
}

async function submitResponse() {
  try {
    await tasksStore.respond(task.value.id, {
      proposed_price: task.value.budget,
      proposed_deadline: task.value.deadline,
      comment: responseComment.value
    })
    closeModal()
    alert('Отклик отправлен!')
  } catch (e) {
    console.error(e)
    alert('Ошибка при отправке отклика')
  }
}

async function acceptResponse(responseId) {
  await tasksStore.acceptResponse(responseId)
}

async function rejectResponse(responseId) {
  await tasksStore.rejectResponse(responseId)
}

// --- Редактирование / удаление ---
async function deleteTask() {
  if (confirm('Удалить задачу?')) {
    await tasksStore.remove(task.value.id)
    router.push('/')
  }
}

// --- Сдача результата ---
async function fetchMaterials(taskId) {
  try {
    const res = await api.get(`/tasks/${taskId}/materials/`)
    materials.value = res.data
  } catch (e) {
    console.error('Ошибка загрузки материалов', e)
  }
}

function handleFileUpload(event) {
  resultFile.value = event.target.files[0]
}

async function submitResult() {
  if (!resultTitle.value) {
    alert('Укажите название')
    return
  }
  if (!resultFile.value && !resultUrl.value) {
    alert('Загрузите файл или укажите ссылку')
    return
  }

  const formData = new FormData()
  formData.append('title', resultTitle.value)
  if (resultFile.value) {
    formData.append('result_file', resultFile.value)
  }
  if (resultUrl.value) {
    formData.append('url', resultUrl.value)
  }

  try {
    const response = await api.post(`/tasks/${task.value.id}/deliver/`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
    console.log('Результат отправлен:', response.data)
    await fetchMaterials(task.value.id)
    await tasksStore.fetchTask(task.value.id)
    alert('Результат отправлен на проверку')
    resultTitle.value = ''
    resultFile.value = null
    resultUrl.value = ''
  } catch (e) {
    console.error(e)
    // Покажем ответ сервера
    if (e.response) {
      console.error('Ответ сервера:', e.response.data)
      alert('Ошибка: ' + JSON.stringify(e.response.data))
    } else {
      alert('Ошибка отправки результата')
    }
  }
}

// --- Принятие / доработка ---
async function acceptTask() {
  if (confirm('Подтвердить выполнение?')) {
    await tasksStore.acceptTask(task.value.id)
    await tasksStore.fetchTask(task.value.id)
  }
}

async function requestRevision() {
  if (confirm('Отправить на доработку?')) {
    await tasksStore.requestRevision(task.value.id)
    await tasksStore.fetchTask(task.value.id)
  }
}
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0,0,0,0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}
.modal-content {
  background: white;
  padding: 2rem;
  border-radius: 8px;
  min-width: 400px;
  max-width: 90%;
}
</style>