<template>
  <div class="app">
    <CornerBanner />
    <Sidebar />
    <div class="main-content">
      <router-view></router-view>
    </div>
  </div>
</template>

<script setup>
import Sidebar from './components/Sidebar.vue';
import CornerBanner from './components/CornerBanner.vue';
</script>

<style scoped>
.app {
  display: flex;
}
.main-content {
  flex: 1;
  padding: 20px;
}
</style>
