<script setup lang="ts">
import { defineProps, type Component } from 'vue'
defineProps<{
  buttonLabel: string
  iconComponent?: Component
  type?: 'button' | 'submit' | 'reset'
}>()
</script>

<template>
  <button :type="type" class="primary-button">
    {{ buttonLabel }}
    <component :is="iconComponent" v-if="iconComponent" class="icon" />
  </button>
</template>

<style scoped>
.primary-button {
  align-items: center;
  display: flex;
  gap: 4px;
  justify-content: center;
}

.icon {
  height: 20px;
  width: 20px;
}
</style>
