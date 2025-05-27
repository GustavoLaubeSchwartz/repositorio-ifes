import { ref } from 'vue'
import { defineStore } from 'pinia'

interface UniqueAccessLinkResponseBody {
  link: string
  id_sessao: number
  id_resposta: number
  id_usuario: number
  respondido: number
  criado_em: string
  respondido_em: string
}

export const useUniqueAccessLinkDatas = defineStore(
  'uniqueAccessLinkDatas',
  () => {
    const sessionData = ref<UniqueAccessLinkResponseBody | null>(null)

    function setSessionData(data: UniqueAccessLinkResponseBody) {
      sessionData.value = data
    }

    function setResponded() {
      if (sessionData.value) {
        sessionData.value.respondido = 1
      }
    }

    function clearSessionData() {
      sessionData.value = null
    }

    return {
      sessionData,
      setSessionData,
      setResponded,
      clearSessionData,
    }
  },
)
