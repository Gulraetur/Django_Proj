import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getMyResponses } from '@/api/responses'

export const useResponsesStore = defineStore('responses', () => {
  const items = ref([])

  async function fetchMyResponses() {
    const res = await getMyResponses()
    items.value = res.data
  }

  function hasResponded(taskId) {
    return items.value.some(r => r.task === taskId)
  }

  return { items, fetchMyResponses, hasResponded }
})