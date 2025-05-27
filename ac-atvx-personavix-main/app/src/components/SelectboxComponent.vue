<script setup lang="ts">
withDefaults(
  defineProps<{
    label: string
    options: Array<{ id: number; option: string }>
    modelValue: string
    firstOption?: string
    firstOptionDisabled?: boolean
  }>(),
  {
    firstOptionDisabled: false,
  },
)

const emit = defineEmits(['update:modelValue'])

function updateValue(event: Event) {
  const target = event.target as HTMLSelectElement
  emit('update:modelValue', target.value)
}
</script>

<template>
  <div>
    <label>{{ label }}</label>
    <select @change="updateValue" :value="modelValue">
      <option value="" :disabled="firstOptionDisabled" selected>
        {{ firstOption }}
      </option>
      <option
        v-for="option in options"
        :key="option.id"
        :value="option.id.toString()"
      >
        {{ option.option }}
      </option>
    </select>
  </div>
</template>

<style scoped>
div {
  display: flex;
  flex-direction: column;
}

select {
  border: 1px solid var(--color-base-gray);
  border-radius: 8px;
  color: var(--color-base-gray);
  font-size: 16px;
  height: 35px;
  margin-top: 8px;
  outline: none;
  padding-left: 8px;
  width: 264px;
}
</style>
