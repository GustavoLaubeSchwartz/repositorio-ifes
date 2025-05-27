import api from './api'
import type { User } from '@/types'
import Cookie from 'js-cookie'

export interface LoginResponse {
  access_token: string
  user: User
}

interface UserLoginRequestBody {
  email: string
  senha: string
}

interface UserRequestBody {
  nome: string | null
  email: string
  telefone: string | null
  flag_acesso: number
  permissao: number
  setor: string | null
  senha_hash: string
}

interface LoginResponseBody {
  access_token: string
  user_datas: User
}
class UserService {
  async login(user: UserLoginRequestBody): Promise<LoginResponse> {
    try {
      const response = await api.post<LoginResponse>('/users/login', user)
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  async register(user: User): Promise<User> {
    try {
      const body: UserRequestBody = {
        nome: null,
        email: user.email,
        telefone: null,
        flag_acesso: user.accessFlag,
        permissao: user.userType,
        setor: null,
        senha_hash: user.password,
      }

      const access_token = Cookie.get('access_token')
      const response = await api.post<User>('/users', body, {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  async updateUser(
    userId: number,
    userData: { nome?: string; email?: string; telefone?: string },
  ): Promise<User> {
    try {
      const access_token = Cookie.get('access_token')
      const response = await api.patch<User>(`/users/${userId}`, userData, {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  async loginWithToken(): Promise<LoginResponseBody> {
    try {
      const access_token = Cookie.get('access_token')
      const response = await api.post<LoginResponseBody>(
        '/users/login/with-token',
        {},
        {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        },
      )
      return response.data
    } catch (error) {
      if (error instanceof Error) {
        if (error.message.includes('Email e/ou senha incorretos')) {
          throw error
        }
        throw new Error('Erro ao realizar login com token')
      }
      throw new Error('Erro desconhecido na requisição')
    }
  }

  private handleError(error: unknown): Error {
    if (error instanceof Error) {
      return error
    }
    return new Error('Erro desconhecido na requisição')
  }
}

export default new UserService()
