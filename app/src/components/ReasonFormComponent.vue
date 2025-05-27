<script setup lang="ts">
import { ref } from 'vue'
import { useQuestionaryAnswers } from '@/stores/questionaryAnswers'
import PrimaryButtonSubmitComponent from '@/components/PrimaryButtonSubmitComponent.vue'

const questionaryAnswers = useQuestionaryAnswers()

const selectedReason = ref(null)

const showWarningMessage = ref(false)
const warningMessage = ref('')

const reasons = [
  {
    idReason: 1,
    reason: 'Processo Seletivo',
  },
  {
    idReason: 2,
    reason: 'Autoconhecimento',
  },
  {
    idReason: 3,
    reason: 'Desenvolvimento de carreira',
  },
  {
    idReason: 4,
    reason: 'Facilitar a adaptação',
  },
]

function handleWithFirstQuestion(event: Event) {
  event.preventDefault()

  if (!selectedReason.value) {
    showWarningMessage.value = true
    warningMessage.value = 'Selecione um motivo para responder o teste.'
    return
  } else {
    showWarningMessage.value = false
    warningMessage.value = ''
  }

  const selectedReasonObject = reasons.find(
    reason => reason.idReason === selectedReason.value,
  )

  if (selectedReasonObject) {
    questionaryAnswers.setReason(selectedReasonObject?.reason)
  }
}
</script>

<template>
  <h4>Antes de Iniciar, por que você está respondendo este teste?</h4>

  <form @submit="handleWithFirstQuestion($event)">
    <div
      v-for="reason in reasons"
      :key="reason.idReason"
      class="radio-container"
    >
      <input
        type="radio"
        :id="'reason-' + reason.idReason"
        :value="reason.idReason"
        v-model="selectedReason"
      />
      <label :for="'reason-' + reason.idReason">{{ reason.reason }}</label>
    </div>
    <div class="validation-message" v-show="showWarningMessage">
      <p>{{ warningMessage }}</p>
    </div>
    <PrimaryButtonSubmitComponent value="Iniciar" class="form-submit-button" />
  </form>
</template>

<style scoped>
form {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
  gap: 16px 0;
  margin: 32px 64px 0px 64px;
  width: 780px;
}

h4 {
  margin-top: 32px;
  width: 780px;
}

.radio-container {
  align-items: center;
  display: flex;
  flex-basis: calc(50% - 16px);
  gap: 16px;
  justify-content: flex-start;
  & input[type='radio'] {
    appearance: none;
    border: 4px solid #ccc;
    border-radius: 50%;
    cursor: pointer;
    display: inline-block;
    height: 20px;
    outline: none;
    position: relative;
    transition: border-color 0.1s ease-in-out;
    width: 20px;
  }
  & input[type='radio']:checked {
    border-color: var(--color-base-blue);
  }
  & label {
    font-size: 18px;
    margin-right: 32px;
  }
}

.form-submit-button {
  margin-top: 32px;
}

.validation-message {
  margin-top: 32px;
}

@media (max-width: 860px) {
  h4 {
    font-size: 24px;
  }

  form,
  h4 {
    width: 680px;
  }
}

@media (max-width: 480px) {
  h4 {
    font-size: 18px;
  }

  form {
    align-items: center;
    flex-direction: column;
    justify-content: center;
    width: 100%;
  }

  label {
    font-size: 16px;
  }

  form,
  h4 {
    width: 100%;
  }
}
</style>
