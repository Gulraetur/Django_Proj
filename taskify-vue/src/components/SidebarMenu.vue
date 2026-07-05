<template>
  <nav class="bg-light vh-100 p-3 border-end" style="width: 250px; min-height: 100%;">
    <ul class="nav flex-column">
      <li class="nav-item">
        <router-link class="nav-link" to="/">Главная</router-link>
      </li>
      <li class="nav-item">
        <router-link class="nav-link" to="/catalog">Каталог</router-link>
      </li>
      <li class="nav-item">
        <router-link class="nav-link" to="/feedback">Обратная связь</router-link>
      </li>
      <li class="nav-item">
        <router-link class="nav-link" to="/profile">Профиль</router-link>
      </li>
    </ul>
  </nav>
</template>

<script setup>
// Никакой логики
</script>

<style scoped>
/* Можно добавить свои стили для активного пункта */
.router-link-active {
  font-weight: bold;
  color: #0d6efd !important;
}
</style>