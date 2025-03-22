<template>
    <div class="registration-form">
        <h2>Реєстрація</h2>
        <form @submit.prevent="handleSubmit">
            <label>Ім'я: <input v-model="form.username" required /></label>
            <label>Email: <input v-model="form.email" type="email" required /></label>
            <label>Пароль: <input v-model="form.password" type="password" required /></label>
            <button type="submit">Зареєструватися</button>
        </form>
        <p v-if="errorMessage" style="color: red;">{{ errorMessage }}</p>
        <p v-if="successMessage" style="color: green;">{{ successMessage }}</p>
    </div>
</template>

<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';

const router = useRouter();
const form = ref({ username: '', email: '', password: '' });

const errorMessage = ref('');
const successMessage = ref('');

const handleSubmit = async () => {
    errorMessage.value = '';
    successMessage.value = '';

    try {
        const response = await fetch('https://ai-education-website.onrender.com/api/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                username: form.value.username,
                email: form.value.email,
                password: form.value.password,
            }),
        });

        if (response.ok) {
            const data = await response.json();
            successMessage.value = 'Реєстрація пройшла успішно!';
            router.push('/login');
        } else {
            const errorData = await response.json();
            errorMessage.value = errorData.message || 'Сталася помилка при реєстрації';
        }
    } catch (error) {
        errorMessage.value = 'Помилка підключення до сервера';
        console.error('Error during registration:', error);
    }
};
</script>
