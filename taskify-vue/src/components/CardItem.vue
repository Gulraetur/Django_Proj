<template>
  <div class="card h-100" @click="$emit('click')" style="cursor: pointer;">
    <div class="card-body d-flex flex-column">
      <h5 class="card-title">{{ title }}</h5>
      <p class="card-text flex-grow-1">{{ description }}</p>
      <p class="card-text"><strong>{{ price }} ₽</strong></p>
      <router-link :to="`/detail/${id}`" class="btn btn-primary mt-auto" @click.stop>
        Подробнее
      </router-link>
    </div>
  </div>
</template>

<script setup>
defineProps({
  id: { type: [Number, String], required: true },
  title: { type: String, required: true },
  description: { type: String, default: '' },
  price: { type: Number, required: true },
})

defineEmits(['click'])
</script>