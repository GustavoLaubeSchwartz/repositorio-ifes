<script setup lang="ts">
import { defineProps, ref } from 'vue'
import ClosedEyeIcon from './icons/ClosedEyeIcon.vue'
import OpenEyeIcon from './icons/OpenEyeIcon.vue'

defineProps<{
  type: string
  placeholder?: string
  minlength?: number
  maxlength?: number
  modelValue?: string
}>()

const emit = defineEmits(['update:modelValue'])
const showPassword = ref(false)

function togglePasswordVisibility() {
  showPassword.value = !showPassword.value
}

function updateValue(event: Event) {
  const target = event.target as HTMLInputElement
  emit('update:modelValue', target.value)
}
</script>

<template>
  <div class="relative">
    <input
      v-if="type !== 'submit'"
      :type="type === 'password' && showPassword ? 'text' : type"
      :placeholder="placeholder"
      :minlength="minlength"
      :maxlength="maxlength"
      :value="modelValue"
      @input="updateValue"
    />
    <input v-else :type="type" :value="modelValue" />
    <button
      v-show="type === 'password'"
      @click="togglePasswordVisibility"
      type="button"
      aria-label="Toggle password visibility"
    >
      <OpenEyeIcon v-if="showPassword" />
      <ClosedEyeIcon v-else />
    </button>
  </div>
</template>

<style scoped>
input {
  border: none;
  border-bottom: 1px solid #000000;
  font-size: 18px;
  height: 32px;
  width: 320px;
  padding-right: 32px;
}

input:focus {
  outline: none;
}

button {
  background: none;
  border: none;
  cursor: pointer;
  height: 24px;
  position: absolute;
  right: 8px;
  top: 4px;
  width: 24px;
  padding: 0;
}

.relative {
  position: relative;
}

@media screen and (max-width: 390px) {
  input {
    width: 280px;
  }
}
</style>
