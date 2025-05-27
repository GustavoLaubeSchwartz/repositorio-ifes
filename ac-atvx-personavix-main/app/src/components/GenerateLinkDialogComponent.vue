<script setup lang="ts">
import { ref } from 'vue'
import { v4 as uuidv4 } from 'uuid'
import CloseIcon from './icons/CloseIcon.vue'
import CopyIcon from './icons/CopyIcon.vue'
import CadastreInputComponent from './CadastreInputComponent.vue'
import PrimaryButtonComponent from './PrimaryButtonComponent.vue'
import PrimaryButtonSubmitComponent from './PrimaryButtonSubmitComponent.vue'
import LoadingAnimation from './LoadingAnimationComponent.vue'
import { useShowGenerateLinkDialog } from '@/stores/showGenerateLinkDialog'
import linkService from '@/services/linkService'
import type { ApiError } from '@/types'

const dialogStore = useShowGenerateLinkDialog()

const emailOrPhone = ref('')
const warningMessage = ref('')
const showWarningMessage = ref(false)
const successMessage = ref('')
const showSuccessMessage = ref(false)
const uuidGenerated = ref('')
const passwordGenerated = ref('')
const linkGenerated = ref(false)
const datasToCopy = ref('')
const isSubmitting = ref(false)

const copyDatas = () => {
  navigator.clipboard.writeText(datasToCopy.value)
}

function generatePassword(): string {
  const characters =
    'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#'
  let password = ''

  for (let i = 0; i < 8; i++) {
    const randomIndex = Math.floor(Math.random() * characters.length)
    password += characters[randomIndex]
  }

  return password
}

async function HandleWithLinkGeneration(event: Event) {
  event.preventDefault()

  if (!emailOrPhone.value) {
    warningMessage.value = 'O campo E-mail ou telefone é obrigatório!'
    showWarningMessage.value = true
    return
  }

  isSubmitting.value = true
  showWarningMessage.value = false
  linkGenerated.value = false

  uuidGenerated.value = uuidv4()
  passwordGenerated.value = generatePassword()

  const linkData = {
    user: emailOrPhone.value,
    link: uuidGenerated.value,
    senha_hash: passwordGenerated.value,
  }

  try {
    const response = await linkService.generateUniqueAccessLink(linkData)
    successMessage.value = 'Link gerado com sucesso!'
    showSuccessMessage.value = true
    datasToCopy.value = `Link: localhost:5173/login?id_session=${response.link}\nSenha: ${passwordGenerated.value}`
    linkGenerated.value = true

    setTimeout(() => {
      showSuccessMessage.value = false
    }, 2000)
  } catch (error: unknown) {
    const apiError = error as ApiError
    const statusCode = apiError.response?.status
    const errorData = apiError.response?.data as { message?: string }
    warningMessage.value =
      errorData?.message ||
      `Erro ao gerar o link! ${statusCode ? `(Status: ${statusCode})` : ''}`
    showWarningMessage.value = true
    console.error('Error during link generation:', error)
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

      <h3>Gerar Link</h3>

      <form class="dialog-form" @submit="HandleWithLinkGeneration($event)">
        <CadastreInputComponent
          type="text"
          label="E-mail ou Telefone"
          placeholder="E-mail ou Telefone"
          minlength="6"
          v-model="emailOrPhone"
        />
        <div class="validation-message" v-show="showWarningMessage">
          <p>{{ warningMessage }}</p>
        </div>
        <div class="loading-container">
          <PrimaryButtonSubmitComponent
            value="Gerar Link"
            class="form-submit-button"
          />
          <LoadingAnimation text="Gerando link..." v-if="isSubmitting" />
        </div>
      </form>

      <div class="generated-link-informations" v-show="linkGenerated">
        <div>
          <p>Link gerado com sucesso!</p>
          <p>Sessão: {{ uuidGenerated }}</p>
          <p>Senha: {{ passwordGenerated }}</p>
        </div>
        <PrimaryButtonComponent
          buttonLabel="Copiar"
          :iconComponent="CopyIcon"
          v-show="linkGenerated"
          @click="copyDatas"
        />
      </div>
    </dialog>
  </div>
</template>

<style scoped>
h3 {
  font-weight: 500;
}

.generated-link-informations {
  align-items: center;
  display: flex;
  flex-direction: column;
  gap: 32px;
  justify-content: center;
  & div {
    align-items: start;
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin: 0px 54px;
  }
}
</style>
