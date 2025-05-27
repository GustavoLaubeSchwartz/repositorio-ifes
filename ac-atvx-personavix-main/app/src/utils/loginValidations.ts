export default function loginPasswordValidations(password: string): {
  message: string
  showWarning: boolean
} {
  let warningMessage = ''
  let showWarningMessage = false

  if (!password) {
    warningMessage = 'O campo senha não pode ser vazio.'
    showWarningMessage = true
  } else if (password.length < 8) {
    warningMessage = 'A senha deve ter no mínimo 8 caracteres.'
    showWarningMessage = true
  } else if (password.length > 30) {
    warningMessage = 'A senha deve ter no máximo 30 caracteres.'
    showWarningMessage = true
  }

  return { message: warningMessage, showWarning: showWarningMessage }
}
