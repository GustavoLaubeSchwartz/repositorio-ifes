<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useUserDatas } from '@/stores/userDatas'
import SecondaryButton from '../components/SecondaryButtonComponent.vue'
import LoginInput from '../components/LoginInputComponent.vue'
import PrimaryButton from '../components/PrimaryButtonSubmitComponent.vue'
import LoadingAnimation from '../components/LoadingAnimationComponent.vue'
import loginPasswordValidations from '../utils/loginValidations'
import openWhatsApp from '../utils/openWhatsApp'
import userService from '@/services/userService'
import setLoginCookie from '@/utils/setLoginCookie'

const userDatas = useUserDatas()

// Form fields
const email = ref('')
const password = ref('')

// Messages and flags
const warningMessage = ref('')
const showWarningMessage = ref(false)
const showSuccessMessage = ref(false)
const isLoading = ref(false)
// Router
const router = useRouter()

async function processLogin(event: Event) {
  event.preventDefault()
  const emailValue = email.value
  const passwordValue = password.value

  if (!emailValue || !passwordValue) {
    warningMessage.value = 'Todos os campos devem ser preenchidos.'
    showWarningMessage.value = true
    return
  }

  const validation = loginPasswordValidations(passwordValue)

  if (validation.showWarning) {
    warningMessage.value = validation.message
    showWarningMessage.value = validation.showWarning
    return
  }

  try {
    isLoading.value = true
    const userResponse = await userService.login({
      email: emailValue,
      senha: passwordValue,
    })
    userDatas.setUserDatas({
      ...userResponse.user_datas,
      isUniqueAccess: false,
    })

    setLoginCookie(userResponse.access_token, 24)
    showSuccessMessage.value = true

    setTimeout(() => {
      router.push('/')
    }, 300)
  } catch (error) {
    warningMessage.value = error.message
    showWarningMessage.value = true
  } finally {
    isLoading.value = false
  }
}
</script>

<template>
  <main>
    <div class="banner">
      <div class="banner-content">
        <h2>PersonaVix</h2>
        <h3>Realize o teste DISC e descubra seu perfil comportamental!</h3>
        <SecondaryButton text="Saiba Mais" />
      </div>
    </div>
    <div class="login">
      <img src="../assets/autvix-logo.png" alt="Autvix Logo" />
      <h2>Olá, seja bem-vindo!</h2>
      <p>Entre em sua conta para responder ao teste.</p>
      <form @submit="processLogin($event)">
        <LoginInput
          type="email"
          placeholder="E-mail"
          minlength="6"
          v-model="email"
        />
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
          <PrimaryButton value="Entrar" />
          <LoadingAnimation text="Entrando..." v-if="isLoading" />
        </div>

        <div class="success-message" v-show="showSuccessMessage">
          <p>Logado com sucesso!</p>
        </div>
      </form>

      <p class="login-help">
        Não está conseguindo efetuar o login? Entre em contato com o
        <span @click="openWhatsApp">RH</span>.
      </p>
      <p class="login-footer">© 2024 Autvix Group.</p>
    </div>
  </main>
</template>

<style scoped>
main {
  display: flex;
  color: #ffffff;
  height: 100vh;
  /* overflow: hidden; */
}

h3 {
  margin: 16px 0;
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

.banner {
  align-items: center;
  background: linear-gradient(
    to right,
    var(--color-base-green),
    var(--color-base-blue)
  );
  display: flex;
  height: 100vh;
  justify-content: center;
  width: 50%;
  & h2 {
    font-weight: 600;
  }
}

.banner-content {
  width: 65%;
}

.login {
  align-items: center;
  color: #000000;
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin: 32px;
  width: 50%;
  & h2 {
    margin-bottom: 16px;
  }
  & p {
    padding: 0px 32px;
  }
  & form {
    align-items: center;
    display: flex;
    flex-direction: column;
    gap: 64px;
    justify-content: center;
    margin-top: 64px;
  }
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

@media (max-width: 744px) {
  .banner {
    display: none;
  }

  .login {
    width: 100%;
  }
}

@media (max-width: 480px) {
  img {
    width: 48px;
  }
}
</style>
