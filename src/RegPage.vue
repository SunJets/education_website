<template>
    <div class="registration-form">
      <h2>Регистрация</h2>
      <form @submit.prevent="handleSubmit">
        <div>
          <label for="username">Имя пользователя:</label>
          <input v-model="form.username" id="username" type="text" required />
        </div>
  
        <div>
          <label for="email">Электронная почта:</label>
          <input v-model="form.email" id="email" type="email" required />
        </div>
  
        <div>
          <label for="password">Пароль:</label>
          <input v-model="form.password" id="password" type="password" required />
        </div>
  
        <button type="submit">Зарегистрироваться</button>
      </form>
    </div>
  </template>
  
  <script>
  import { ref } from 'vue';
  
  export default {
    setup() {
      const form = ref({
        username: '',
        email: '',
        password: ''
      });
  
      const handleSubmit = () => {
        console.log('Регистрация:', form.value);
        // Здесь можно добавить логику для отправки данных на сервер
      };
  
      return { form, handleSubmit };
    }
  };
  </script>
  
  <style scoped>
  .registration-form {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ddd;
    border-radius: 8px;
  }
  
  h2 {
    text-align: center;
  }
  
  form div {
    margin-bottom: 15px;
  }
  
  label {
    display: block;
    font-weight: bold;
  }
  
  input {
    width: 100%;
    padding: 8px;
    margin-top: 5px;
    border: 1px solid #ddd;
    border-radius: 4px;
  }
  
  button {
    width: 100%;
    padding: 10px;
    background-color: #4CAF50;
    color: white;
    border: none;
    border-radius: 4px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #45a049;
  }
  </style>
  