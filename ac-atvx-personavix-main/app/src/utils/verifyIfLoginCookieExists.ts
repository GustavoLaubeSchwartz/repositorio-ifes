import Cookie from 'js-cookie'
import { useUserDatas } from '@/stores/userDatas'
import { useGlobalLoading } from '@/stores/globalLoading'
import userService from '@/services/userService'
import setLoginCookie from '@/utils/setLoginCookie'

export default async function verifyIfLoginCookieExists(): Promise<boolean> {
  if (Cookie.get('access_token')) {
    const userDatas = useUserDatas()
    const globalLoading = useGlobalLoading()

    if (!userDatas.userDatas) {
      try {
        globalLoading.setLoading(true)
        const response = await getSessionData()
        if (response) {
          userDatas.setUserDatas({
            ...response.user_datas,
            isUniqueAccess: false,
          })
          setLoginCookie(response.access_token, 24)
          return true
        }
        return false
      } catch (error) {
        console.error('Erro ao obter dados da sessão:', error)
        return false
      } finally {
        globalLoading.setLoading(false)
      }
    }
    return true
  }
  return false
}

async function getSessionData() {
  try {
    const response = await userService.loginWithToken()
    return response
  } catch (error) {
    console.error('Erro ao obter dados da sessão:', error)
    Cookie.remove('access_token', { path: '' })
    return null
  }
}
