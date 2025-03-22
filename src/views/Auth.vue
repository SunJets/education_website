<template>
    <div class="auth-container">
      <h2>Вход или регистрация</h2>
      <div class="buttons">
        <router-link to="/login" class="btn">Войти</router-link>
        <router-link to="/register" class="btn">Зарегистрироваться</router-link>
      </div>
    </div>
  </template>
  
  <style scoped>
  .auth-container {
    text-align: center;
    margin-top: 100px;
  }
  .buttons {
    display: flex;
    justify-content: center;
    gap: 20px;
  }
  .btn {
    padding: 10px 20px;
    background-color: #2563eb;
    color: white;
    text-decoration: none;
    border-radius: 5px;
  }
  </style>
  