import { useUserDatas } from '@/stores/userDatas'
import { useUniqueAccessLinkDatas } from '@/stores/uniqueAccessLinkDatas'
import linkService from '@/services/linkService'

export default async function checkIfItIsUniqueAccessLogin(
  sessionLink: string,
) {
  if (!sessionLink) {
    return false
  }
  const userStore = useUserDatas()
  const uniqueAccessLinkStore = useUniqueAccessLinkDatas()

  try {
    const sessionData = await linkService.getUniqueAccessLinkDatas(sessionLink)
    if (sessionData) {
      uniqueAccessLinkStore.setSessionData(sessionData)
      userStore.setUserDatas({
        ...sessionData.usuarios_,
        isUniqueAccess: true,
      })
      return true
    } else {
      throw new Error('Sessão inválida')
    }
  } catch (error) {
    console.error(error)
    return false
  }
}
