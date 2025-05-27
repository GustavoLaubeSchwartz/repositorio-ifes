import Cookie from 'js-cookie'

export default function setLoginCookie(
  token: string,
  expirationTime: number,
): void {
  const expires = new Date()
  expires.setHours(expires.getHours() + expirationTime)
  Cookie.set('access_token', token, { expires })
}
