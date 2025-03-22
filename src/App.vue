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

    <button @click="getCourses">Далі  </button>
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

const getCourses = () => {
  const tags = selectedItems.value.map(e => e.text);

  fetch('http://localhost:11434/api/generate', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      "model": "deepseek-r1",
      "prompt": `A person likes these topics: ${tags}. You need to come up with course titles that would be interesting to this person. The course titles should not be too complex, so that you could explain them if needed. Also, each course should have a description of 1-2 sentences. Do not write any text except for the JSON object. The response should contain only a valid JSON string with no extra symbols, spaces, or anything else. The format of the response should be a JSON object like this: {\"courses\":[{\"title\":\"\",\"description\":\"\"}, {\"title\":\"\",\"description\":\"\"}]}.`,
      "stream": false
    }),
  })
  .then(res => res.json())
  .then(data => console.log('Response:', data))
  .catch(error => console.error('Error:', error));
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
