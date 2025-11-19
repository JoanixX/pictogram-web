import './App.css'
import { useEffect, useState } from 'react'
import Chat from './components/Chat'
import Sidebar from './components/Sidebar'
import UploadPredict from "./components/UploadPredict";
import Login from './components/Login'
import { me as apiMe } from './api/auth'


function App() {
  const [token, setToken] = useState<string | null>(localStorage.getItem('token'))
  const [showLogin, setShowLogin] = useState(false)
  const [user, setUser] = useState<{ id: number; username: string } | null>(null)
  const [selectedConversationId, setSelectedConversationId] = useState<number | null>(null)

  useEffect(() => {
    if (!token) return
    ;(async () => {
      try {
        const u = await apiMe(token)
        setUser(u)
        // conversations will be fetched by Sidebar when token present
      } catch (err) {
        console.error('failed to fetch user', err)
        setToken(null)
        localStorage.removeItem('token')
      }
    })()
  }, [token])

  const handleLogin = (newToken: string) => {
    localStorage.setItem('token', newToken)
    setToken(newToken)
    setShowLogin(false)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    setToken(null)
    setUser(null)
    setSelectedConversationId(null)
  }

  return (
    <div id="root">
      <header className="app-header">
        <h1>Pictogram Chat</h1>
        <div className="header-actions">
          <button className="user-btn" onClick={() => setShowLogin((s) => !s)} title="Cuenta">
            👤
          </button>
          {token && <button className="user-logout" onClick={handleLogout}>Salir</button>}
        </div>
      </header>

      <div className="app-layout">
        <aside className="app-sidebar">
          <Sidebar token={token ?? undefined} user={user ?? undefined} onSelectConversation={(id?: number) => setSelectedConversationId(id ?? null)} />
        </aside>

        <main className="app-main">
          <div className="app-card">
            <Chat token={token ?? undefined} user={user ?? undefined} conversationId={selectedConversationId ?? undefined} onConversationCreated={(id: number) => setSelectedConversationId(id)} />
              <UploadPredict />
          </div>
        </main>
      </div>

      {showLogin && (
        <div className="login-panel">
          <Login onLogin={handleLogin} />
        </div>
      )}
    </div>
  )
}

export default App
