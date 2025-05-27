<script setup lang="ts">
defineProps<{
  text: string
}>()
</script>

<template>
  <div class="spinner-container">
    <div class="spinner"></div>
    <span>{{ text }}</span>
  </div>
</template>

<style scoped>
.spinner-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  display: flex;
  flex-direction: row;
  gap: 10px;
}

.spinner {
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: conic-gradient(
    transparent,
    var(--color-base-green),
    var(--color-base-blue)
  );
  -webkit-mask: radial-gradient(
    farthest-side,
    transparent calc(100% - 4px),
    #fff 0
  );
  mask: radial-gradient(farthest-side, transparent calc(100% - 4px), #fff 0);
  animation: spin 1s linear infinite;
}

span {
  font-size: 18px;
}

@keyframes spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
