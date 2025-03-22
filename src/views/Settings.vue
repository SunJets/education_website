<template>
    <div class="content">
      <h2>Налаштування</h2>
      <label>
        <input type="checkbox" v-model="darkMode" />
        Темний режим
      </label>
    </div>
</template>
  
<script setup>
    import { ref, watch } from 'vue';

    const darkMode = ref(false);
    watch(darkMode, (val) => {
    document.body.classList.toggle('dark-theme', val);
    });
</script>
  