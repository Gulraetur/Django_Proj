import { defineStore } from 'pinia'
import { ref } from 'vue'
import { getMyResponses } from '@/api/responses'

export const useResponsesStore = defineStore('responses', () => {
  const items = ref([])

  async function fetchMyResponses() {
    const response = await getMyResponses()
    items.value = response.data
    return items.value
  }

  return { items, fetchMyResponses }
})