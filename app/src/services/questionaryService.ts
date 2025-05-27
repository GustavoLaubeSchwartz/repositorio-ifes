import api from './api'
import type { Questionary, CadasteredAnswer } from '@/types'
import Cookie from 'js-cookie'

class QuestionaryService {
  async getQuestionary(): Promise<Questionary> {
    try {
      const access_token = Cookie.get('access_token')
      const response = await api.get<Questionary>('/questionary', {
        headers: {
          Authorization: `Bearer ${access_token}`,
        },
      })
      return response.data
    } catch (error) {
      throw this.handleError(error)
    }
  }

  async submitAnswers(
    userId: number,
    answers: Omit<
      CadasteredAnswer,
      'id_resposta' | 'id_usuario' | 'respondido_em'
    >,
  ): Promise<CadasteredAnswer> {
    try {
      const access_token = Cookie.get('access_token')
      const response = await api.post<CadasteredAnswer>(
        `/answers/${userId}`,
        answers,
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

export default new QuestionaryService()
