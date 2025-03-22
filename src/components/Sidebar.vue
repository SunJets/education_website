<template>
    <div class="sidebar">
        <h2>Навігація</h2>
        <nav>
            <router-link to="/dashboard" active-class="active">Головна</router-link>
            <router-link to="/profile" active-class="active">Профіль</router-link>
            <router-link to="/settings" active-class="active">Налаштування</router-link>
        </nav>
        <!-- <br> -->
        <h2>Мої курси</h2>
        <div>
            
        </div>
    </div>
</template>

<style scoped>
    .sidebar {
        width: 200px;
        background: #fff;
        padding: 20px;
    }
    nav a {
        display: block;
        padding: 10px;
        text-decoration: none;
        color: #333;
    }
    nav a.active {
        font-weight: bold;
        color: #2563eb;
    }
</style>
  