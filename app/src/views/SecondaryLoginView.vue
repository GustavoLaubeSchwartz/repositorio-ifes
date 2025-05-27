<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import LoginInput from '../components/LoginInputComponent.vue'
import PrimaryButton from '../components/PrimaryButtonSubmitComponent.vue'
import LoadingAnimation from '../components/LoadingAnimationComponent.vue'
import { useUserDatas } from '@/stores/userDatas'
import { useUniqueAccessLinkDatas } from '@/stores/uniqueAccessLinkDatas'
import loginPasswordValidations from '../utils/loginValidations'
import openWhatsApp from '../utils/openWhatsApp'
import linkService from '@/services/linkService'
import setLoginCookie from '@/utils/setLoginCookie'

const userDatas = useUserDatas()
const uniqueAccessLinkDatas = useUniqueAccessLinkDatas()

const password = ref('')
const loading = ref(true)

const userData = ref<{
  nome?: string
  email?: string
  telefone?: string
} | null>(null)

const warningMessage = ref('')
const showWarningMessage = ref(false)
const isSubmitting = ref(false)

const router = useRouter()
const user = computed(() => {
  return (
    userData.value?.nome ||
    userData.value?.email ||
    userData.value?.telefone ||
    ''
  )
})

onMounted(async () => {
  try {
    userDatas.clearUserDatas()
    uniqueAccessLinkDatas.clearSessionData()

    const sessionLink = router.currentRoute.value.query.id_session as string
    if (sessionLink) {
      const sessionData =
        await linkService.getUniqueAccessLinkDatas(sessionLink)

      if (sessionData) {
        uniqueAccessLinkDatas.setSessionData(sessionData)
        userData.value = {
          nome: sessionData.usuarios_?.nome || undefined,
          email: sessionData.usuarios_?.email || undefined,
          telefone: sessionData.usuarios_?.telefone || undefined,
        }
        userDatas.setUserDatas({
          ...sessionData.usuarios_,
          isUniqueAccess: true,
        })
      }
    }
  } catch (error) {
    console.error('Erro ao carregar dados da sessão:', error)
    router.push({ name: 'login', query: { error: 'session_not_found' } })
  } finally {
    loading.value = false
  }
})

async function processLogin(event: Event) {
  event.preventDefault()
  isSubmitting.value = true
  const passwordValue = password.value
  const validation = loginPasswordValidations(passwordValue)

  if (validation.showWarning) {
    warningMessage.value = validation.message
    showWarningMessage.value = validation.showWarning
    isSubmitting.value = false
    return
  }

  const loginData = {
    id_sessao: uniqueAccessLinkDatas.sessionData?.id_sessao ?? 0,
    senha: passwordValue,
  }

  try {
    const loginResponse = await linkService.login(loginData)

    userDatas.setUserDatas({
      ...loginResponse.session_datas.usuarios_,
      isUniqueAccess: true,
    })
    uniqueAccessLinkDatas.sessionData = loginResponse.session_datas

    setLoginCookie(loginResponse.access_token, 1)

    router.push('/')
  } catch (error) {
    console.error('Erro durante o login:', error)
    warningMessage.value = `Senha incorreta. ${error.response?.status ? `(Status: ${error.response.status})` : ''}`
    showWarningMessage.value = true
  } finally {
    isSubmitting.value = false
  }
}
</script>

<template>
  <main>
    <LoadingAnimation text="Carregando..." v-if="loading" />
    <template v-else>
      <img src="../assets/autvix-logo.png" alt="Autvix Logo" />
      <h2>Olá, {{ user }}!</h2>
      <h4>Para entrar e responder ao teste, digite a sua senha.</h4>
      <form @submit="processLogin">
        <LoginInput
          type="password"
          placeholder="Senha"
          minlength="8"
          maxlength="30"
          v-model="password"
        />

        <div class="validation-message" v-show="showWarningMessage">
          <p>{{ warningMessage }}</p>
        </div>

        <div class="loading-container">
          <PrimaryButton :disabled="isSubmitting" value="Entrar" />
          <LoadingAnimation text="Entrando..." v-if="isSubmitting" />
        </div>
      </form>
      <p class="login-help">
        Não está conseguindo efetuar o login? Entre em contato com o
        <span @click="openWhatsApp">RH</span>.
      </p>
      <p class="login-footer">© 2024 Autvix Group.</p>
    </template>
  </main>
</template>

<style scoped>
main {
  align-items: center;
  display: flex;
  flex-direction: column;
  height: 100vh;
  justify-content: center;
  padding: 32px;
  position: relative;
}

h4 {
  margin: 16px 0 64px 0;
}

form {
  align-items: center;
  display: flex;
  flex-direction: column;
  gap: 64px;
  justify-content: center;
}

img {
  position: absolute;
  right: 16px;
  top: 16px;
  width: 60px;
}

span {
  color: var(--color-base-blue);
  cursor: pointer;
  text-decoration: underline;
}

.login-help {
  font-size: 16px;
  margin-top: 64px;
  padding: 0 32px;
}

.login-footer {
  position: absolute;
  bottom: 16px;
  font-size: 14px;
}

@media screen and (max-width: 460px) {
  h2 {
    font-size: 20px;
  }

  h4 {
    font-size: 16px;
  }

  img {
    width: 48px;
  }

  .login-help {
    font-size: 14px;
  }
  .login-footer {
    font-size: 12px;
  }
}
</style>
