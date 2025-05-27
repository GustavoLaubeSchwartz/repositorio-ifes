<script setup lang="ts">
import LoadingAnimationComponent from './LoadingAnimationComponent.vue'

defineProps<{
  isLoading: boolean
}>()
</script>

<template>
  <div v-if="isLoading" class="global-loading">
    <div class="loading-overlay">
      <LoadingAnimationComponent text="Carregando..." />
    </div>
  </div>
</template>

<style scoped>
.global-loading {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(255, 255, 255, 0.8);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 9999;
}

.loading-overlay {
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}
</style>
