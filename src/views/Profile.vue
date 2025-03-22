<template>
    <div class="content">
        <h2>Профіль</h2>
        <p>Ім'я: {{ user.name }}</p>
        <p>Email: {{ user.email }}</p>
    </div>
</template>

<script setup>
    import { ref } from 'vue';

    const user = ref({ name: 'Ivan Ivanov', email: 'ivan@example.com' });
</script>
  