<script setup lang="ts">
import { defineProps, ref } from 'vue'

defineProps<{
  type: string
  label: string
  placeholder?: string
  minlength?: number
  maxlength?: number
  modelValue?: string
  inputDisasbled?: boolean
}>()

const emit = defineEmits(['update:modelValue'])
const showPassword = ref(false)

function updateValue(event: Event) {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>

<template>
  <div>
    <label>{{ label }}</label>
    <input
      v-if="type !== 'submit'"
      :type="type === 'password' && showPassword ? 'text' : type"
      :placeholder="placeholder"
      :minlength="minlength"
      :maxlength="maxlength"
      :value="modelValue"
      :disabled="inputDisasbled"
      @input="updateValue"
    />
  </div>
</template>

<style scoped>
div {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

input {
  border: 1px solid var(--color-base-gray);
  border-radius: 8px;
  color: var(--color-base-gray);
  font-size: 16px;
  height: 34px;
  outline: none;
  padding: 8px;
  width: 264px;
}
</style>
