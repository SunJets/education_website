<template>
    <div class="login-form">
        <h2>Вхід</h2>
        <form @submit.prevent="handleSubmit">
            <label>Ім'я: <input v-model="form.username" required /></label>
            <label>Пароль: <input v-model="form.password" type="password" required /></label>
            <button type="submit">Увійти</button>
        </form>
        <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
        <p v-if="successMessage" style="color: green;">{{ successMessage }}</p>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const form = ref({ username: '', password: '' });

const errorMessage = ref('');
const successMessage = ref('');

const handleSubmit = async () => {
    errorMessage.value = '';
    successMessage.value = '';

    try {
        const response = await fetch('https://ai-education-website.onrender.com/api/login', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: form.value.username,
                password: form.value.password,
            }),
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('token', data.token);
            successMessage.value = 'Вхід успішний!';
            router.push('/profile');
            console.log(data);
        } else {
            const errorData = await response.json();
            errorMessage.value = errorData.message || 'Невірний логін або пароль';
        }
    } catch (error) {
        errorMessage.value = 'Помилка підключення до сервера';
        console.error('Error during login:', error);
    }
};
</script>
