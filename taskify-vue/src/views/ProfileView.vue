<template>
  <div class="container mt-4">
    <h2>Профиль</h2>
    <div class="row">
      <div class="col-md-4">
        <p><strong>Имя:</strong> {{ user?.first_name }}</p>
        <p><strong>Email:</strong> {{ user?.email }}</p>
        <p><strong>Роль:</strong> 
          <span v-if="isCustomer && isExecutor">Заказчик и Исполнитель</span>
          <span v-else-if="isCustomer">Заказчик</span>
          <span v-else-if="isExecutor">Исполнитель</span>
          <span v-else>Не определена</span>
        </p>
      </div>
      <div class="col-md-8">
        <!-- Только заказчик -->
        <div v-if="isCustomer && !isExecutor">
          <h3>Мои заказы</h3>
          <TaskRow 
            v-for="task in myTasks" 
            :key="task.id" 
            :task="task" 
            :showRespondButton="false"
            @click="goToTask(task.id)"
          />
          <p v-if="myTasks.length === 0">Нет созданных заказов.</p>
        </div>

        <!-- Только исполнитель -->
        <div v-if="isExecutor && !isCustomer">
          <h3>Мои отклики</h3>
          <div v-for="resp in responses" :key="resp.id" class="border-bottom py-2">
            <router-link :to="`/tasks/${resp.task.id}`">
              <strong>{{ resp.task.title }}</strong>
            </router-link>
            <span class="text-muted ms-2">Статус: {{ resp.status }}</span>
            <span class="float-end">{{ resp.proposed_price }} ₽</span>
          </div>
          <p v-if="responses.length === 0">Вы ещё не откликались на задачи.</p>
        </div>

        <!-- Обе роли (вкладки) -->
        <div v-if="isCustomer && isExecutor">
          <ul class="nav nav-tabs">
            <li class="nav-item">
              <button class="nav-link" :class="{ active: activeTab === 'my' }" @click="activeTab = 'my'">Мои заказы</button>
            </li>
            <li class="nav-item">
              <button class="nav-link" :class="{ active: activeTab === 'responses' }" @click="activeTab = 'responses'">Мои отклики</button>
            </li>
          </ul>
          <div class="mt-3">
            <div v-if="activeTab === 'my'">
              <TaskRow 
                v-for="task in myTasks" 
                :key="task.id" 
                :task="task" 
                :showRespondButton="false"
                @click="goToTask(task.id)"
              />
              <p v-if="myTasks.length === 0">Нет созданных заказов.</p>
            </div>
            <div v-else>
              <div v-for="resp in responses" :key="resp.id" class="border-bottom py-2">
                <router-link :to="`/tasks/${resp.task.id}`">
                  <strong>{{ resp.task.title }}</strong>
                </router-link>
                <span class="text-muted ms-2">Статус: {{ resp.status }}</span>
                <span class="float-end">{{ resp.proposed_price }} ₽</span>
              </div>
              <p v-if="responses.length === 0">Вы ещё не откликались на задачи.</p>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTasksStore } from '@/stores/tasks'
import { useResponsesStore } from '@/stores/responses'
import { useRouter } from 'vue-router'
import TaskRow from '@/components/TaskRow.vue'

const authStore = useAuthStore()
const tasksStore = useTasksStore()
const responsesStore = useResponsesStore()
const router = useRouter()

const activeTab = ref('my')
const user = computed(() => authStore.user)
const isCustomer = computed(() => authStore.isCustomer)
const isExecutor = computed(() => authStore.isExecutor)

const myTasks = ref([])
const responses = ref([])

async function loadMyTasks() {
  const tasks = await tasksStore.fetchTasksWithRole('customer')
  myTasks.value = tasks
}

async function loadResponses() {
  await responsesStore.fetchMyResponses()
  responses.value = responsesStore.items
}

function goToTask(id) {
  router.push(`/tasks/${id}`)
}

onMounted(async () => {
  if (isCustomer.value) await loadMyTasks()
  if (isExecutor.value) await loadResponses()
})
</script>