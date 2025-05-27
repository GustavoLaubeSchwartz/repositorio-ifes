<script setup lang="ts">
import { ref, watch } from 'vue'
import { useShowUpdateUserDatasDialog } from '@/stores/showUpdateUserDatasDialog'
import { useUserDatas } from '@/stores/userDatas'
import CloseIcon from './icons/CloseIcon.vue'
import CadastreInputComponent from './CadastreInputComponent.vue'
import PrimaryButtonSubmitComponent from './PrimaryButtonSubmitComponent.vue'
import LoadingAnimation from './LoadingAnimationComponent.vue'
import userService from '@/services/userService'

const props = defineProps({
  canClose: Boolean,
})

const dialogStore = useShowUpdateUserDatasDialog()
const userDatasState = useUserDatas()
const isLoading = ref(true)
const isSubmitting = ref(false)

const buttonLabel = ref(props.canClose ? 'Atualizar' : 'Cadastrar')
const dialogTitle = ref(props.canClose ? 'Seus dados' : 'Cadastro de Dados')
const name = ref('')
const email = ref('')
const phone = ref('')
const sector = ref('')

const WarningMessage = ref('')
const showWarningMessage = ref(false)
const showSuccessMessage = ref(false)
const successMessage = ref('')

// Adicionar watcher para os dados do usuário
watch(
  () => userDatasState.userDatas,
  newUserData => {
    if (newUserData) {
      name.value = newUserData.nome ?? ''
      email.value = newUserData.email ?? ''
      phone.value = newUserData.telefone ?? ''
      sector.value = newUserData.setor ?? ''
      isLoading.value = false
    }
  },
  { immediate: true },
)

async function HandleWithUserDatasRegistration(event: Event) {
  event.preventDefault()

  if (!name.value) {
    WarningMessage.value = 'Por favor, preencha o campo de nome.'
    showWarningMessage.value = true
    return
  } else {
    WarningMessage.value = ''
    showWarningMessage.value = false
  }

  if (!userDatasState.userDatas?.id_usuario) {
    WarningMessage.value = 'ID do usuário não encontrado.'
    showWarningMessage.value = true
    return
  }

  const userData = {
    nome: name.value,
    email: email.value,
    telefone: phone.value,
  }

  try {
    isSubmitting.value = true
    showSuccessMessage.value = false
    showWarningMessage.value = false

    const response = await userService.updateUser(
      userDatasState.userDatas.id_usuario,
      userData,
    )
    userDatasState.setUserDatas(response)
    successMessage.value = 'Dados atualizados com sucesso!'
    showSuccessMessage.value = true
  } catch (error) {
    console.error(error)
    WarningMessage.value =
      'Erro ao atualizar os dados. Por favor, tente novamente.'
    showWarningMessage.value = true
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
        v-if="canClose"
        @click="dialogStore.toggleVisibility"
      />

      <h3>{{ dialogTitle }}</h3>
      <p v-if="!canClose">
        Opa, parece que você ainda tem que cadastrar alguns dados para poder
        realizar o teste.
      </p>

      <LoadingAnimation text="Carregando dados..." v-if="isLoading" />

      <form
        v-else
        class="dialog-form"
        @submit="HandleWithUserDatasRegistration($event)"
      >
        <CadastreInputComponent
          type="text"
          label="Nome Completo"
          placeholder="Nome"
          v-model="name"
        />
        <CadastreInputComponent
          type="email"
          label="E-mail"
          placeholder="E-mail"
          v-model="email"
        />
        <CadastreInputComponent
          type="text"
          label="Telefone"
          placeholder="Telefone"
          v-model="phone"
        />
        <CadastreInputComponent
          type="text"
          label="Setor"
          placeholder="Setor"
          :inputDisasbled="true"
          v-model="sector"
        />
        <div class="validation-message" v-show="showWarningMessage">
          <p>{{ WarningMessage }}</p>
        </div>
        <div class="success-message" v-show="showSuccessMessage">
          <p>{{ successMessage }}</p>
        </div>

        <div class="loading-container">
          <PrimaryButtonSubmitComponent
            :value="buttonLabel"
            :disabled="isSubmitting"
            class="form-submit-button"
          />
          <LoadingAnimation text="Atualizando..." v-if="isSubmitting" />
        </div>
      </form>
    </dialog>
  </div>
</template>

<style scoped>
dialog {
  padding: 32px;
}

h3 {
  font-weight: 500;
}
</style>
