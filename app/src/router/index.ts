import { createRouter, createWebHistory } from 'vue-router'
import { useUserDatas } from '@/stores/userDatas'
import { useUniqueAccessLinkDatas } from '@/stores/uniqueAccessLinkDatas'
import linkService from '@/services/linkService'
import verifyIfLoginCookieExists from '@/utils/verifyIfLoginCookieExists'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      beforeEnter: async (to, from, next) => {
        const isAuthenticated = await verifyIfLoginCookieExists()
        void (isAuthenticated ? next() : next({ name: 'login' }))
      },
      component: () => import('../views/InitialPageView.vue'),
    },
    {
      path: '/login',
      name: 'login',
      beforeEnter: (to, from, next) => {
        // Verifies if the 'id_session' query parameter exists
        const idSession = to.query.id_session
        if (idSession) {
          next({ name: 'unique-login', query: { id_session: idSession } })
        } else {
          next()
        }
      },
      component: () => import('../views/PrimaryLoginView.vue'),
    },
    {
      path: '/unique-login',
      name: 'unique-login',
      beforeEnter: async (to, from, next) => {
        const sessionLink = to.query.id_session as string
        if (!sessionLink) {
          return next({ name: 'login' })
        }
        const userStore = useUserDatas()
        const uniqueAccessLinkStore = useUniqueAccessLinkDatas()

        try {
          const sessionData =
            await linkService.getUniqueAccessLinkDatas(sessionLink)
          if (sessionData) {
            uniqueAccessLinkStore.setSessionData(sessionData)
            userStore.setUserDatas({
              ...sessionData.usuarios_,
              isUniqueAccess: true,
            })
            next()
          } else {
            throw new Error('Sessão inválida')
          }
        } catch (error) {
          console.error(error)
          next({ name: 'login', query: { error: 'session_not_found' } })
        }
      },
      component: () => import('../views/SecondaryLoginView.vue'),
    },
    {
      path: '/relatorios',
      name: 'reports',
      beforeEnter: async (to, from, next) => {
        const isAuthenticated = await verifyIfLoginCookieExists()
        void (isAuthenticated ? next() : next({ name: 'login' }))
      },
      component: () => import('../views/ReportsView.vue'),
    },
  ],
})

export default router
