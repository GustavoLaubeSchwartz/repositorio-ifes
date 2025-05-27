import api from './api'
import Cookie from 'js-cookie'

interface User {
  atualizado_em: string
  criado_em: string
  email: string
  flag_acesso: number
  id_usuario: number
  nome: string | null
  permissao: number
  setor: string | null
  telefone: string | null
}

interface Answer {
  id_resposta: number
  id_usuario: number
  dominancia: number
  influencia: number
  estabilidade: number
  conformidade: number
  motivo: string
  respondido_em: string
  usuarios_: User
}

class AnswerService {
  async getAllAnswers(): Promise<Answer[]> {
    try {
      const access_token = Cookie.get('access_token')
      const response = await api.get<Answer[]>('/answers', {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  async getAnswerById(id: number): Promise<Answer> {
    try {
      const access_token = Cookie.get('access_token')
      const response = await api.get<Answer>(`/answers/${id}`, {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      })
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

export default new AnswerService()
