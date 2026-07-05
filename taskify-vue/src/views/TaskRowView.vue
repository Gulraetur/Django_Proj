<template>
  <div class="task-row">
    <h3>{{ task.title }}</h3>
    <p>{{ task.budget }} ₽</p>
    <router-link :to="`/tasks/${task.id}`">Подробнее</router-link>
    <button v-if="showRespondButton" @click="$emit('respond', task)">Откликнуться</button>
    <button v-if="isOwner" @click="$emit('edit', task)">✏️</button>
    <button v-if="isOwner" @click="$emit('delete', task)">🗑️</button>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useAuthStore } from '@/stores/auth'

const props = defineProps({
  task: Object,
  showRespondButton: Boolean,
})
const emit = defineEmits(['respond', 'edit', 'delete'])

const authStore = useAuthStore()
const isOwner = computed(() => authStore.user?.id === props.task.customer?.id)
</script>