<template>
    <div class="corner-banner">
      <div v-if="isLoggedIn" class="account-info">
        <span>{{ username }}</span>
        <button @click="logout">Вийти</button>
      </div>
      <div v-else class="auth-buttons">
        <button @click="goToLogin">Увійти</button>
        <button @click="goToRegister">Зареєструватися</button>
      </div>
    </div>
  </template>
  
  <script setup>
  import { ref, computed } from 'vue';
  import { useRouter } from 'vue-router';
  
  const router = useRouter();
  
  // Проверяем, есть ли токен в localStorage
  const token = localStorage.getItem('token');
  const username = localStorage.getItem('username'); // или имя пользователя, если оно сохранено в localStorage
  
  // Состояние, вошел ли пользователь
  const isLoggedIn = computed(() => !!token);
  
  // Функция для выхода из аккаунта
  const logout = () => {
    localStorage.removeItem('token');
    localStorage.removeItem('username'); // или любое другое, что храните для пользователя
    router.push('/auth'); // Перенаправление на страницу авторизации
  };
  
  // Функции для перехода на страницы регистрации и входа
  const goToLogin = () => {
    router.push('/login');
  };
  
  const goToRegister = () => {
    router.push('/register');
  };
  </script>
  
  <style scoped>
  .corner-banner {
    position: fixed;
    bottom: 10px;
    right: 10px;
    background-color: #333;
    color: white;
    padding: 10px 20px;
    border-radius: 8px;
    box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
    display: flex;
    justify-content: space-between;
    align-items: center;
    z-index: 9999;
  }
  
  .account-info, .auth-buttons {
    display: flex;
    align-items: center;
  }
  
  button {
    background-color: #5c6bc0;
    color: white;
    border: none;
    padding: 5px 10px;
    margin-left: 10px;
    cursor: pointer;
    border-radius: 4px;
  }
  
  button:hover {
    background-color: #3949ab;
  }
  
  span {
    margin-right: 10px;
    font-weight: bold;
  }
  </style>
  