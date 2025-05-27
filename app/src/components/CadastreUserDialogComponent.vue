<script setup lang="ts">
import { ref } from 'vue'
import CloseIcon from './icons/CloseIcon.vue'
import CadastreInputComponent from './CadastreInputComponent.vue'
import PrimaryButtonSubmitComponent from './PrimaryButtonSubmitComponent.vue'
import SelectboxComponent from './SelectboxComponent.vue'
import LoadingAnimation from './LoadingAnimationComponent.vue'
import { useShowCadastreUserDialog } from '@/stores/showCadastreUserDialog'
import userService from '@/services/userService'
import type { ApiError, User } from '@/types'

const dialogStore = useShowCadastreUserDialog()

// Form fields
const email = ref('')
const password = ref('')
const userType = ref('0')
const access = ref('0')

// Messages and flags
const warningMessage = ref('')
const successMessage = ref('')
const showWarningMessage = ref(false)
const showSuccessMessage = ref(false)
const isSubmitting = ref(false)
const lastOperation = ref<'register'>('register')

// Validate form inputs
function validateForm() {
  if (!email.value || !password.value || !userType.value || !access.value) {
    warningMessage.value = 'Preencha todos os campos!'
    showWarningMessage.value = true
    return false
  }
  showWarningMessage.value = false
  return true
}

// Clear form fields
function clearForm() {
  email.value = ''
  password.value = ''
  userType.value = '0'
  access.value = '0'
}

// Retry operation
async function retryOperation() {
  showWarningMessage.value = false
  if (lastOperation.value === 'register') {
    await HandleUserRegister(new Event('submit'))
  }
}

// Handle user registration
async function HandleUserRegister(event: Event) {
  event.preventDefault()

  if (!validateForm()) return

  isSubmitting.value = true
  lastOperation.value = 'register'

  const user: User = {
    email: email.value,
    password: password.value,
    userType: parseInt(userType.value, 10),
    accessFlag: parseInt(access.value, 10),
  }

  try {
    const response = await userService.register(user)
    successMessage.value = response.message || 'Usuário cadastrado com sucesso!'
    showSuccessMessage.value = true

    setTimeout(() => {
      clearForm()
      showSuccessMessage.value = false
      dialogStore.toggleVisibility()
    }, 2000)
  } catch (error) {
    const apiError = error as ApiError
    const statusCode = apiError.response?.status
    const errorData = apiError.response?.data as { message?: string }

    warningMessage.value =
      errorData?.message ||
      `Erro ao cadastrar o usuário! ${statusCode ? `(Status: ${statusCode})` : ''}`
    showWarningMessage.value = true
    console.error('Erro durante o cadastro:', apiError)
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <div class="dialog-overlay">
    <dialog open>
      <CloseIcon
        class="dialog-close-icon"
        @click="dialogStore.toggleVisibility"
      />
      <h3>Cadastrar Usuário</h3>
      <form class="dialog-form" @submit="HandleUserRegister($event)">
        <CadastreInputComponent
          type="email"
          label="E-mail"
          placeholder="E-mail"
          :minlength="6"
          v-model="email"
        />
        <CadastreInputComponent
          type="password"
          label="Senha"
          placeholder="Senha"
          :minlength="8"
          :maxlength="30"
          v-model="password"
        />
        <SelectboxComponent
          label="Tipo de Usuário"
          :options="[
            { id: 1, option: 'Usuário' },
            { id: 2, option: 'Gestor' },
            { id: 3, option: 'Administrador' },
          ]"
          v-model="userType"
          firstOption="Tipo de Usuário"
        />
        <SelectboxComponent
          label="Acesso"
          :options="[
            { id: 0, option: 'Não' },
            { id: 1, option: 'Sim' },
          ]"
          v-model="access"
          firstOption="Acesso"
        />
        <div class="success-message" v-show="showSuccessMessage">
          <p>{{ successMessage }}</p>
        </div>
        <div class="validation-message" v-show="showWarningMessage">
          <p>{{ warningMessage }}</p>
          <button class="retry-button" @click="retryOperation">
            Tentar Novamente
          </button>
        </div>

        <div class="loading-container">
          <PrimaryButtonSubmitComponent
            :disabled="isSubmitting"
            value="Cadastrar"
            class="form-submit-button"
          />
          <LoadingAnimation text="Cadastrando..." v-if="isSubmitting" />
        </div>
      </form>
    </dialog>
  </div>
</template>

<style scoped>
.dialog-form {
  align-items: center;
  display: flex;
  flex-direction: column;
  gap: 32px;
  justify-content: center;
}

h3 {
  font-weight: 500;
}

.validation-message {
  align-items: center;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.retry-button {
  background-color: var(--color-base-blue);
  border: none;
  border-radius: 4px;
  color: white;
  cursor: pointer;
  font-size: 14px;
  padding: 8px 16px;
  transition: background-color 0.3s;
}

.retry-button:hover {
  background-color: #1976d2;
}

@media screen and (max-width: 860px) {
  dialog {
    max-width: 70%;
  }
}

@media screen and (max-width: 480px) {
  dialog {
    max-width: 320px;
  }
}
</style>
