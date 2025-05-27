<script setup lang="ts">
import CloseIcon from './icons/CloseIcon.vue'
import TestResultComponent from './TestResultComponent.vue'

interface User {
  atualizado_em: string
  criado_em: string
  email: string
  flag_acesso: number
  id_usuario: number
  nome: string | null
  permissao: number
  setor: string | null
  telefone: string | null
}

interface Answer {
  id_resposta: number
  id_usuario: number
  dominancia: number
  influencia: number
  estabilidade: number
  conformidade: number
  motivo: string
  respondido_em: string
  usuarios_: User
}

defineProps<{
  testResult: Answer
}>()
</script>

<template>
  <div class="dialog-overlay">
    <dialog open>
      <CloseIcon class="dialog-close-icon" @click="$emit('close')" />
      <TestResultComponent :testResult="testResult" />
    </dialog>
  </div>
</template>

<style scoped>
dialog {
  min-width: 1200px;
  padding-top: 32px;
  max-height: 95vh;
  overflow-y: auto;
}

@media screen and (max-width: 1280px) {
  dialog {
    min-width: 80%;
  }
}

@media screen and (max-width: 840px) {
  dialog {
    padding-top: 64px;
  }
}

@media screen and (max-width: 480px) {
  dialog {
    padding-top: 96px;
  }
}
</style>
