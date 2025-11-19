export async function register(username: string, password: string) {
  const res = await fetch('/api/v1/auth/register', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ username, password }),
  })
  if (!res.ok) throw new Error('Registration failed')
  return res.json()
}

export async function login(username: string, password: string) {
  const body = new URLSearchParams()
  body.append('username', username)
  body.append('password', password)

  const res = await fetch('/api/v1/auth/token', {
    method: 'POST',
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
    body: body.toString(),
  })
  if (!res.ok) {
    const txt = await res.text()
    throw new Error(txt || 'Login failed')
  }
  return res.json()
}

export async function me(token: string) {
  const res = await fetch('/api/v1/auth/me', {
    headers: { Authorization: `Bearer ${token}` },
  })
  if (!res.ok) throw new Error('Cannot get user info')
  return res.json()
}
