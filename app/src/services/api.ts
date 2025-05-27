import axios, {
  type AxiosError,
  type AxiosInstance,
  type AxiosResponse,
} from 'axios'

const api: AxiosInstance = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('token')
  if (token) {
    config.headers.Authorization = `Bearer ${token}`
  }
  return config
})

api.interceptors.response.use(
  (response: AxiosResponse) => response,
  (error: AxiosError) => {
    if (error.response) {
      const status = error.response.status
      const data = error.response.data as { message?: string }

      switch (status) {
        case 401:
          localStorage.removeItem('token')
          window.location.href = '/login'
          break
        case 403:
          console.error('Acesso negado:', data.message)
          break
        case 404:
          console.error('Recurso não encontrado:', data.message)
          break
        case 500:
          console.error('Erro interno do servidor:', data.message)
          break
        default:
          console.error('Erro na requisição:', data.message)
      }
    } else if (error.request) {
      console.error('Erro de rede:', error.request)
    } else {
      console.error('Erro na configuração:', error.message)
    }

    return Promise.reject(error)
  },
)

export default api
