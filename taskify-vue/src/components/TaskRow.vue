<template>
  <div class="task-row d-flex align-items-stretch py-3 px-4 border-bottom" style="cursor: pointer;">
    <!-- Левая часть: название (ссылка) и описание -->
    <div class="flex-grow-1 d-flex flex-column justify-content-center">
      <router-link :to="`/tasks/${task.id}`" class="text-decoration-none text-dark fw-bold h5 mb-1">
        {{ task.title }}
      </router-link>
      <p class="mb-0 text-muted small">
        {{ task.description || 'Описание отсутствует' }}
      </p>
    </div>

    <!-- Правая часть: бюджет и кнопки -->
    <div class="d-flex flex-column align-items-end justify-content-between ms-4">
      <span class="fw-bold text-success fs-5">{{ task.budget }} ₽</span>
      <div>
        <button v-if="showRespondButton" class="btn btn-primary btn-sm me-2" @click.stop="$emit('respond', task)">
          Откликнуться
        </button>
        <button v-if="isOwner" class="btn btn-outline-secondary btn-sm me-1" @click="$router.push(`/tasks/${task.id}/edit`)">
          ✏️
        </button>
        <button v-if="isOwner" class="btn btn-outline-danger btn-sm" @click="deleteTask">
          🗑️
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  task: { type: Object, required: true },
  showRespondButton: { type: Boolean, default: false }
})

const emit = defineEmits(['click', 'respond', 'edit', 'delete'])

const authStore = useAuthStore()
const isOwner = computed(() => {
  const user = authStore.user
  if (!user || !props.task.client) return false
  return user.id === props.task.client.id
})
</script>

<style scoped>
.task-row:hover {
  background-color: #f8f9fa;
  transition: background-color 0.15s;
}
.task-row a {
  display: inline-block; /* чтобы клик по ссылке не перехватывался */
}
</style>