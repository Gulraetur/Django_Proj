<template>
  <div class="container py-4">
    <div class="row justify-content-center">
        <div class="col-md-8 col-lg-6">
            <form @submit.prevent="submitForm" class="card p-4 shadow-sm">
            <h3 class="card-title text-center mb-3">Обратная связь</h3>
            <div class="mb-3">
                <label for="name" class="form-label">Имя</label>
                <input
                id="name"
                v-model="form.name"
                type="text"
                class="form-control"
                placeholder="Введите ваше имя"
                required
                />
            </div>

            <div class="mb-3">
                <label for="email" class="form-label">Email</label>
                <input
                id="email"
                v-model="form.email"
                type="email"
                class="form-control"
                placeholder="example@mail.ru"
                required
                />
            </div>

            <div class="mb-3">
                <label for="subject" class="form-label">Тема</label>
                <select id="subject" v-model="form.subject" class="form-select" required>
                <option value="">Выберите тему</option>
                <option value="question">Вопрос по проекту</option>
                <option value="suggestion">Предложение</option>
                <option value="problem">Проблема или ошибка</option>
                <option value="other">Другое</option>
                </select>
            </div>

            <div class="mb-3">
                <label for="message" class="form-label">Сообщение</label>
                <textarea
                id="message"
                v-model="form.message"
                class="form-control"
                rows="5"
                placeholder="Опишите ваш вопрос или предложение..."
                required
                ></textarea>
            </div>

            <button type="submit" class="btn btn-primary">Отправить</button>
            </form>

            <!-- Уведомление об успешной отправке -->
            <div v-if="showSuccess" class="alert alert-success mt-3" role="alert">
            Спасибо! Ваше сообщение отправлено.
            </div>
        </div>
        </div>
    </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

// Данные формы
const form = reactive({
  name: '',
  email: '',
  subject: '',
  message: '',
})

// Флаг для отображения уведомления
const showSuccess = ref(false)

// Обработчик отправки
const submitForm = () => {
  // Простейшая валидация (браузер уже проверяет required, но можно добавить свою)
  if (!form.name || !form.email || !form.subject || !form.message) {
    alert('Пожалуйста, заполните все поля.')
    return
  }

  // Имитация отправки данных на сервер
  console.log('Форма отправлена:', form)

  // Показываем уведомление
  showSuccess.value = true

  // Очищаем форму
  form.name = ''
  form.email = ''
  form.subject = ''
  form.message = ''

  // Через 5 секунд скрываем уведомление
  setTimeout(() => {
    showSuccess.value = false
  }, 5000)
}
</script>

<style scoped>
.card {
  border: none;
  background-color: #f8f9fa;
}
</style>