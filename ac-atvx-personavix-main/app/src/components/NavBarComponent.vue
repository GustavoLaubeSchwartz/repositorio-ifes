<script setup lang="ts">
import Cookie from 'js-cookie'
import { useRouter } from 'vue-router'
import HomePageIcon from './icons/HomePageIcon.vue'
import AddLinkIcon from './icons/AddLinkIcon.vue'
import AddUserIcon from './icons/AddUserIcon.vue'
import TestResultsIcon from './icons/TestResultsIcon.vue'
import UserIcon from './icons/UserIcon.vue'
import { useUserDatas } from '@/stores/userDatas'
import { useUniqueAccessLinkDatas } from '@/stores/uniqueAccessLinkDatas'
import CadastreUserDatasDialogComponent from './CadastreUserDatasDialogComponent.vue'
import CadastreUserDialogComponent from './CadastreUserDialogComponent.vue'
import GenerateLinkDialogComponent from './GenerateLinkDialogComponent.vue'
import { useShowUpdateUserDatasDialog } from '@/stores/showUpdateUserDatasDialog'
import { useShowCadastreUserDialog } from '@/stores/showCadastreUserDialog'
import { useShowGenerateLinkDialog } from '@/stores/showGenerateLinkDialog'

defineProps<{
  navBarTitle?: string
}>()

const userDatas = useUserDatas()
const uniqueAccessLink = useUniqueAccessLinkDatas()
const userPermission = userDatas.userDatas?.permissao || 1
const isUniqueAccessLink = userDatas.userDatas?.isUniqueAccess

const showCadastreUserDialogStore = useShowCadastreUserDialog()
const showGenerateLinkDialogStore = useShowGenerateLinkDialog()
const showUpdateUserDatasDialogStore = useShowUpdateUserDatasDialog()

const router = useRouter()

async function ProcessLogout() {
  Cookie.remove('access_token')
  if (isUniqueAccessLink) {
    const idSession = uniqueAccessLink.sessionData?.link
    await router.push(`/login?id_session=${idSession}`)
    uniqueAccessLink.clearSessionData()
    userDatas.clearUserDatas()
    return
  }

  await router.push('login')
  userDatas.clearUserDatas()
}
</script>

<template>
  <nav>
    <div class="navbar-logo">
      <img src="../assets/autvix-logo.png" alt="Autvix Logo" />
      <p>Autvix</p>
    </div>
    <h4 v-show="navBarTitle" class="navbar-title">{{ navBarTitle }}</h4>
    <div class="navbar-icons">
      <HomePageIcon class="navbar-icon" @click="router.push('/')" />
      <AddLinkIcon
        v-show="userPermission === 3 && !isUniqueAccessLink"
        class="navbar-icon"
        @click="showGenerateLinkDialogStore.toggleVisibility"
      />
      <AddUserIcon
        v-show="userPermission === 3 && !isUniqueAccessLink"
        class="navbar-icon"
        @click="showCadastreUserDialogStore.toggleVisibility"
      />
      <TestResultsIcon
        v-show="
          userPermission >= 2 && userPermission <= 3 && !isUniqueAccessLink
        "
        class="navbar-icon"
        @click="router.push('relatorios')"
      />
      <UserIcon
        class="navbar-icon"
        @click="showUpdateUserDatasDialogStore.toggleVisibility"
      />
      <p @click="ProcessLogout">Sair</p>
    </div>
  </nav>

  <CadastreUserDialogComponent v-if="showCadastreUserDialogStore.showDialog" />
  <GenerateLinkDialogComponent v-if="showGenerateLinkDialogStore.showDialog" />
  <CadastreUserDatasDialogComponent
    :can-close="true"
    v-if="showUpdateUserDatasDialogStore.showDialog"
  />
</template>

<style scoped>
nav {
  box-shadow: 0px 0px 1px #00000085;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0px 16px;
  height: 48px;
  width: 100%;
}

img {
  width: 30px;
}

h4 {
  color: var(--color-base-blue);
  font-weight: 300;
  left: 50%;
  position: absolute;
  transform: translateX(-50%);
}

p {
  color: var(--color-base-blue);
  font-weight: 400;
}

img,
p,
.navbar-icon {
  cursor: pointer;
}

.navbar-logo,
.navbar-icons {
  display: flex;
  align-items: center;
}

.navbar-icons {
  color: var(--color-base-green);
  gap: 16px;
}

.navbar-icon {
  width: 30px;
}

@media screen and (max-width: 744px) {
  .navbar-title {
    display: none;
  }
}

@media screen and (max-width: 490px) {
  p {
    font-size: 18px;
  }
  .navbar-icons {
    gap: 14px;
  }

  img,
  .navbar-icon {
    width: 26px;
  }
}
</style>
