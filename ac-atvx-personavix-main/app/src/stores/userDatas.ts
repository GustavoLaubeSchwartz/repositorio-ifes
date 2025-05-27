import { ref } from 'vue'
import { defineStore } from 'pinia'

interface User {
  atualizado_em: string
  criado_em: string
  email: string | null
  flag_acesso: number
  id_usuario: number
  nome: string | null
  permissao: number
  setor: string | null
  telefone: string | null
  isUniqueAccess?: boolean
}

export const useUserDatas = defineStore('userDatas', () => {
  const userDatas = ref<User | null>(null)

  function setUserDatas(data: User) {
    userDatas.value = data
  }

  function clearUserDatas() {
    userDatas.value = null
  }

  return {
    userDatas,
    setUserDatas,
    clearUserDatas,
  }
})
