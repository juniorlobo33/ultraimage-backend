import { useState, useEffect } from 'react'
import AuthPage from './components/AuthPage.jsx'
import Dashboard from './components/Dashboard.jsx'
import UploadTool from './components/UploadTool.jsx'
import PaymentPage from './components/PaymentPage.jsx'
import './App.css'

function App() {
  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)
  const [currentPage, setCurrentPage] = useState('home')

  // Verificar autenticação ao carregar
  useEffect(() => {
    checkAuth()
  }, [])

  const checkAuth = async () => {
    try {
      const response = await fetch('http://localhost:5000/api/auth/check-auth', {
        credentials: 'include'
      })
      
      if (response.ok) {
        const userData = await response.json()
        setUser(userData.user)
      }
    } catch (error) {
      console.error('Erro ao verificar autenticação:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleLogin = (userData) => {
    setUser(userData)
    setCurrentPage('dashboard')
  }

  const handleLogout = async () => {
    try {
      await fetch('http://localhost:5000/api/auth/logout', {
        method: 'POST',
        credentials: 'include'
      })
    } catch (error) {
      console.error('Erro ao fazer logout:', error)
    } finally {
      setUser(null)
      setCurrentPage('home')
    }
  }

  const handlePaymentSuccess = (subscription) => {
    // Atualizar dados do usuário após pagamento bem-sucedido
    setUser(prev => ({
      ...prev,
      subscription_plan: subscription.plan,
      images_limit: subscription.images_limit
    }))
    setCurrentPage('dashboard')
  }

  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-32 w-32 border-b-2 border-blue-600"></div>
      </div>
    )
  }

  // Navegação simples sem React Router para evitar complexidade
  const renderPage = () => {
    if (!user && currentPage !== 'home') {
      return <AuthPage onLogin={handleLogin} />
    }

    switch (currentPage) {
      case 'auth':
        return <AuthPage onLogin={handleLogin} />
      case 'dashboard':
        return user ? <Dashboard user={user} onLogout={handleLogout} onNavigate={setCurrentPage} /> : <AuthPage onLogin={handleLogin} />
      case 'tool':
        return user ? <UploadTool user={user} /> : <AuthPage onLogin={handleLogin} />
      case 'payment':
        return user ? <PaymentPage user={user} onPaymentSuccess={handlePaymentSuccess} /> : <AuthPage onLogin={handleLogin} />
      default:
        return <HomePage />
    }
  }

  const HomePage = () => (
    <div className="min-h-screen bg-white">
      {/* Header */}
      <header className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center py-6">
            <div className="flex items-center">
              <div className="flex-shrink-0 flex items-center">
                <div className="h-8 w-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">✨</span>
                </div>
                <span className="ml-2 text-xl font-bold text-gray-900">UpScale Pro</span>
              </div>
            </div>
            
            <nav className="hidden md:flex space-x-8">
              <button onClick={() => setCurrentPage('home')} className="text-gray-500 hover:text-gray-900">Início</button>
              <button onClick={() => setCurrentPage('tool')} className="text-gray-500 hover:text-gray-900">Ferramenta</button>
              {user && <button onClick={() => setCurrentPage('dashboard')} className="text-gray-500 hover:text-gray-900">Dashboard</button>}
              <a href="#recursos" className="text-gray-500 hover:text-gray-900">Recursos</a>
              <a href="#planos" className="text-gray-500 hover:text-gray-900">Planos</a>
              <a href="#contato" className="text-gray-500 hover:text-gray-900">Contato</a>
            </nav>

            <div className="flex items-center space-x-4">
              {user ? (
                <>
                  <span className="text-sm text-gray-600">Olá, {user.name}</span>
                  <button 
                    onClick={handleLogout}
                    className="bg-red-600 text-white px-4 py-2 rounded-md hover:bg-red-700"
                  >
                    Sair
                  </button>
                </>
              ) : (
                <>
                  <button 
                    onClick={() => setCurrentPage('auth')}
                    className="text-gray-500 hover:text-gray-900"
                  >
                    Entrar
                  </button>
                  <button 
                    onClick={() => setCurrentPage('auth')}
                    className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700"
                  >
                    Começar Agora
                  </button>
                </>
              )}
            </div>
          </div>
        </div>
      </header>

      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-50 to-indigo-100 py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center">
          <p className="text-blue-600 font-semibold mb-4">Powered by Real-ESRGAN AI</p>
          <h1 className="text-5xl font-bold text-gray-900 mb-6">
            Aumente a Resolução de suas{' '}
            <span className="text-blue-600">Imagens com IA</span>
          </h1>
          <p className="text-xl text-gray-600 mb-8 max-w-2xl mx-auto">
            Transforme suas imagens de baixa resolução em obras-primas de alta qualidade 
            usando inteligência artificial avançada. Resultados profissionais em segundos.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <button 
              onClick={() => setCurrentPage('tool')}
              className="bg-gray-900 text-white px-8 py-3 rounded-md hover:bg-gray-800 flex items-center justify-center"
            >
              <span className="mr-2">⬆️</span>
              Fazer Upload Grátis
            </button>
            <button className="border border-gray-300 text-gray-700 px-8 py-3 rounded-md hover:bg-gray-50">
              Ver Demonstração
            </button>
          </div>
        </div>
      </section>

      {/* Features Section */}
      <section id="recursos" className="py-20">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Por que escolher o UpScale Pro?
            </h2>
            <p className="text-xl text-gray-600">
              Nossa tecnologia de ponta oferece os melhores resultados do mercado
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center p-6 rounded-lg border border-gray-200">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="text-blue-600 text-2xl">⚡</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Processamento Rápido</h3>
              <p className="text-gray-600">
                Aumente a resolução de suas imagens em segundos com nossa IA otimizada.
              </p>
            </div>

            <div className="text-center p-6 rounded-lg border border-gray-200">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="text-blue-600 text-2xl">🖼️</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Qualidade Superior</h3>
              <p className="text-gray-600">
                Resultados profissionais com preservação de detalhes e nitidez excepcional.
              </p>
            </div>

            <div className="text-center p-6 rounded-lg border border-gray-200">
              <div className="w-12 h-12 bg-blue-100 rounded-lg flex items-center justify-center mx-auto mb-4">
                <span className="text-blue-600 text-2xl">🛡️</span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">100% Seguro</h3>
              <p className="text-gray-600">
                Suas imagens são processadas com segurança e excluídas após o download.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* Pricing Section */}
      <section id="planos" className="py-20 bg-gray-50">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-3xl font-bold text-gray-900 mb-4">
              Escolha seu plano
            </h2>
            <p className="text-xl text-gray-600">
              Planos flexíveis para todas as necessidades
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            {/* Plano Básico */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Básico</h3>
              <div className="mb-4">
                <span className="text-3xl font-bold text-gray-900">R$ 29</span>
                <span className="text-gray-600">/mês</span>
              </div>
              <p className="text-gray-600 mb-6">Perfeito para uso pessoal</p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  50 imagens por mês
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Resolução até 4K
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Suporte por email
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Processamento padrão
                </li>
              </ul>
              <button 
                onClick={() => setCurrentPage('payment')}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
              >
                Escolher Básico
              </button>
            </div>

            {/* Plano Pro */}
            <div className="bg-white rounded-lg shadow-sm border-2 border-blue-500 p-8 relative">
              <div className="absolute -top-3 left-1/2 transform -translate-x-1/2">
                <span className="bg-blue-500 text-white px-4 py-1 rounded-full text-sm">
                  Mais Popular
                </span>
              </div>
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Pro</h3>
              <div className="mb-4">
                <span className="text-3xl font-bold text-gray-900">R$ 79</span>
                <span className="text-gray-600">/mês</span>
              </div>
              <p className="text-gray-600 mb-6">Ideal para profissionais</p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  200 imagens por mês
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Resolução até 8K
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Suporte prioritário
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Processamento rápido
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  API de integração
                </li>
              </ul>
              <button 
                onClick={() => setCurrentPage('payment')}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
              >
                Escolher Pro
              </button>
            </div>

            {/* Plano Empresarial */}
            <div className="bg-white rounded-lg shadow-sm border border-gray-200 p-8">
              <h3 className="text-xl font-semibold text-gray-900 mb-2">Empresarial</h3>
              <div className="mb-4">
                <span className="text-3xl font-bold text-gray-900">R$ 199</span>
                <span className="text-gray-600">/mês</span>
              </div>
              <p className="text-gray-600 mb-6">Para equipes e empresas</p>
              <ul className="space-y-3 mb-8">
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Imagens ilimitadas
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Resolução até 16K
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Suporte 24/7
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Processamento ultra-rápido
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  API completa
                </li>
                <li className="flex items-center">
                  <span className="text-green-500 mr-2">✓</span>
                  Gerenciamento de equipe
                </li>
              </ul>
              <button 
                onClick={() => setCurrentPage('payment')}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded-md hover:bg-blue-700"
              >
                Escolher Empresarial
              </button>
            </div>
          </div>
        </div>
      </section>

      {/* Footer */}
      <footer id="contato" className="bg-gray-900 text-white py-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
            <div>
              <div className="flex items-center mb-4">
                <div className="h-8 w-8 bg-blue-600 rounded-lg flex items-center justify-center">
                  <span className="text-white font-bold text-lg">✨</span>
                </div>
                <span className="ml-2 text-xl font-bold">UpScale Pro</span>
              </div>
              <p className="text-gray-400">
                Transforme suas imagens com inteligência artificial avançada.
              </p>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">Produto</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Recursos</a></li>
                <li><a href="#" className="hover:text-white">Preços</a></li>
                <li><a href="#" className="hover:text-white">API</a></li>
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">Suporte</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Documentação</a></li>
                <li><a href="#" className="hover:text-white">Contato</a></li>
                <li><a href="#" className="hover:text-white">FAQ</a></li>
              </ul>
            </div>

            <div>
              <h3 className="text-lg font-semibold mb-4">Empresa</h3>
              <ul className="space-y-2 text-gray-400">
                <li><a href="#" className="hover:text-white">Sobre</a></li>
                <li><a href="#" className="hover:text-white">Blog</a></li>
                <li><a href="#" className="hover:text-white">Carreiras</a></li>
              </ul>
            </div>
          </div>

          <div className="border-t border-gray-800 mt-8 pt-8 text-center text-gray-400">
            <p>&copy; 2025 UpScale Pro. Todos os direitos reservados.</p>
          </div>
        </div>
      </footer>
    </div>
  )

  return (
    <div className="App">
      {renderPage()}
    </div>
  )
}

export default App

