<script setup lang="ts">
import { defineProps } from 'vue'

defineProps<{
  text: string
}>()
</script>

<template>
  <button>
    {{ text }}
  </button>
</template>

<style scoped>
button {
  background-color: #ffffff;
  border: none;
  border-radius: 18px;
  color: var(--color-base-blue);
  cursor: pointer;
  font-size: 20px;
  font-weight: 300;
  height: 40px;
  width: 160px;
}
</style>
