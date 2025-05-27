<script setup lang="ts">
import { defineProps } from 'vue'

defineProps<{
  modelValue?: string
  disabled?: boolean
}>()
</script>

<template>
  <input
    class="primary-button"
    type="submit"
    :value="modelValue"
    :disabled="disabled"
  />
</template>
