export interface ApiError {
  response?: {
    status: number
    data?: {
      message?: string
    }
  }
}

export interface User {
  email: string
  password: string
  userType: number
  accessFlag: number
}

export interface UserDatas {
  atualizado_em: string
  criado_em: string
  email: string | null
  flag_acesso: number
  id_usuario: number
  nome: string | null
  permissao: number
  setor: string | null
  telefone: string | null
}
export interface SessionData {
  link: string
  id_sessao: number
  id_resposta: number
  id_usuario: number
  respondido: number
  criado_em: string
  respondido_em: string
  usuarios_: {
    id: number
    email: string
    tipo: number
    acesso: number
  }
}

export interface Question {
  id_pergunta: number
  pergunta: string
  criado_em: string
  atualizado_em: string
}

export interface DiscCharacteristic {
  fator: string
  caracteristica: string
  id_caracteristica: number
  id_pergunta: number
  criado_em: string
  atualizado_em: string
}

export interface Questionary {
  questions: Array<Question>
  disc_characteristics: Array<DiscCharacteristic>
}

export interface Answers {
  dominancia: number
  influencia: number
  estabilidade: number
  conformidade: number
}

export interface CadasteredAnswer extends Answers {
  motivo: string
  id_resposta: number
  id_usuario: number
  respondido_em: string
}
