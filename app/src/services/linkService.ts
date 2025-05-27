import api from './api'
import type { UserDatas } from '@/types'
import Cookie from 'js-cookie'

interface LinkGenerationRequest {
  user: string
  link: string
  senha_hash: string
}

interface LinkGenerationResponse {
  link: string
  id_sessao: number
  id_resposta: number | null
  id_usuario: number
  respondido: number
  criado_em: string
  respondido_em: string | null
}

interface UniqueAccessLinkLogin {
  id_sessao: number
  senha: string
}

interface UniqueAccessLinkRequestBody {
  senha: string
}

interface UniqueAccessLinkResponse {
  link: string
  id_sessao: number
  id_resposta: number
  id_usuario: number
  respondido: number
  criado_em: string
  respondido_em: string
  usuarios_: UserDatas
}

interface UniqueAccessLinkResponseBody {
  session_datas: UniqueAccessLinkResponse
  access_token: string
}

class LinkService {
  async generateUniqueAccessLink(
    data: LinkGenerationRequest,
  ): Promise<LinkGenerationResponse> {
    try {
      const access_token = Cookie.get('access_token')
      const response = await api.post<LinkGenerationResponse>(
        '/unique-access-links',
        data,
        {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        },
      )
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  async login(
    loginData: UniqueAccessLinkLogin,
  ): Promise<UniqueAccessLinkResponseBody> {
    try {
      const body: UniqueAccessLinkRequestBody = {
        senha: loginData.senha,
      }

      const response = await api.post<UniqueAccessLinkResponseBody>(
        `/unique-access-links/login/${loginData.id_sessao}`,
        body,
      )
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  async getUniqueAccessLinkDatas(
    session_link: string,
  ): Promise<UniqueAccessLinkResponse> {
    try {
      const access_token = Cookie.get('access_token')
      const response = await api.get<UniqueAccessLinkResponse>(
        `/unique-access-links/${session_link}`,
        {
          headers: {
            Authorization: `Bearer ${access_token}`,
          },
        },
      )
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  private handleError(error: unknown): Error {
    if (error instanceof Error) {
      return error
    }
    return new Error('Erro desconhecido na requisição')
  }
}

export default new LinkService()
