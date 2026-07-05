import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getTasks, getTask, createTask, updateTask, deleteTask } from '@/api/tasks'
import { createResponse, getTaskResponses, acceptRejectResponse } from '@/api/responses'
import api from '@/api/axios'

export const useTasksStore = defineStore('tasks', () => {
  const items = ref([])
  const currentTask = ref(null)
  const responses = ref([])

  async function fetchTasks(role) {
    const res = await getTasks(role)
    items.value = res.data
  }

  async function fetchTasksWithFilters(params) {
    const res = await getTasks(null, params)
    items.value = res.data
  }

  async function fetchTasksWithRole(role) {
    const res = await getTasks(role)
    return res.data 
  }

  async function fetchTask(id) {
    const res = await getTask(id)
    currentTask.value = res.data
    return res.data
  }

  async function create(data) {
    const res = await createTask(data)
    items.value.push(res.data)
    return res.data
  }

  async function update(id, data) {
    const res = await updateTask(id, data)
    const idx = items.value.findIndex(t => t.id === id)
    if (idx !== -1) items.value[idx] = res.data
    if (currentTask.value?.id === id) currentTask.value = res.data
    return res.data
  }

  async function remove(id) {
    await deleteTask(id)
    items.value = items.value.filter(t => t.id !== id)
    if (currentTask.value?.id === id) currentTask.value = null
  }

 // --- Методы для откликов ---
  async function fetchResponses(taskId) {
    const res = await getTaskResponses(taskId)
    responses.value = res.data
    return res.data
  }

  async function respond(taskId, data) {
    const res = await createResponse(taskId, data)
    responses.value.push(res.data)
    return res.data
  }

  async function acceptResponse(responseId) {
    await acceptRejectResponse(responseId, 'accept')
    // обновляем список откликов и задачу
    await fetchResponses(currentTask.value.id)
    await fetchTask(currentTask.value.id)
  }

  async function rejectResponse(responseId) {
    await acceptRejectResponse(responseId, 'reject')
    await fetchResponses(currentTask.value.id)
  }
  async function acceptTask(taskId) {
    await api.post(`/tasks/${taskId}/accept/`)
  }

  async function requestRevision(taskId) {
    await api.post(`/tasks/${taskId}/revision/`)
  }
  // Принятие задачи
  async function acceptTask(taskId) {
    try {
      await api.post(`/tasks/${taskId}/accept/`)
    } catch (e) {
      console.error('Ошибка при подтверждении:', e)
      throw e
    }
  }

  // Отправка на доработку
  async function requestRevision(taskId) {
    try {
      await api.post(`/tasks/${taskId}/revision/`)
    } catch (e) {
      console.error('Ошибка при отправке на доработку:', e)
      throw e
    }
  }

  return {
    items,
    currentTask,
    responses,
    fetchTasks,
    fetchTasksWithFilters,
    fetchTasksWithRole,
    fetchTask,
    create,
    update,
    remove,
    fetchResponses,
    respond,
    acceptResponse,
    rejectResponse,
    acceptTask,
    requestRevision,   
  }
})