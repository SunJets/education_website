<template>
  <div class="box">
    <h1>Вибір навичок</h1>
    <h2>Твої скіли</h2>
    <div class="selected-list" v-if="selectedItems.length">
      <div
        v-for="(item, index) in selectedItems"
        :key="item.id"
        class="item selected"
        @click="removeFromSelected(index)"
      >
        {{ item.text }}
      </div>
    </div>
    <p v-else class="placeholder">
      Натисніть на елемент, щоб додати до списку скілів
    </p>

    <h2>Список елементів</h2>
    <div class="list">
      <div
        v-for="(item, index) in items"
        :key="item.id"
        class="item"
        @click="moveToSelected(index)"
      >
        {{ item.text }}
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const items = ref([
  { id: 1, text: "Айті" },
  { id: 2, text: "Дизайн" },
  { id: 3, text: "SMM" },
  { id: 4, text: "Інше" },
]);

const selectedItems = ref([]);

const moveToSelected = (index) => {
  selectedItems.value.push(items.value[index]);
  items.value.splice(index, 1);
};

const removeFromSelected = (index) => {
  items.value.push(selectedItems.value[index]);
  selectedItems.value.splice(index, 1);
};
</script>

<style scoped>
.box {
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.2);
  border-radius: 10px;
  text-align: center;
  width: 400px;
  margin: 50px auto;
  padding: 20px;
  background-color: #f8f9fa;
}

h1 {
  color: #333;
  font-size: 22px;
  margin-bottom: 15px;
}

h2 {
  font-size: 18px;
  color: #555;
  margin-bottom: 10px;
}

.placeholder {
  font-size: 14px;
  color: gray;
  font-style: italic;
}

.selected-list,
.list {
  display: flex;
  flex-direction: column;
  gap: 8px;
  margin-bottom: 20px;
}

.item {
  padding: 12px;
  border-radius: 5px;
  border: 1px solid #ccc;
  cursor: pointer;
  background: white;
  transition: 0.3s;
}

.item:hover {
  background: #e9ecef;
}

.item.selected {
  background: #007bff;
  color: white;
  border-color: #007bff;
}

.item.selected:hover {
  background: #0056b3;
}
</style>
