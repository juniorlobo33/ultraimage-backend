import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Progress } from '@/components/ui/progress.jsx'
import { User, Settings, LogOut, Image as ImageIcon, Crown, Zap } from 'lucide-react'
import '../App.css'

function Dashboard({ user, onLogout, onNavigate }) {
  const [loading, setLoading] = useState(false)

  const handleLogout = async () => {
    setLoading(true)
    try {
      await fetch('http://localhost:5002/api/auth/logout', {
        method: 'POST',
        credentials: 'include'
      })
      onLogout()
    } catch (err) {
      console.error('Erro no logout:', err)
    } finally {
      setLoading(false)
    }
  }

  const getUsagePercentage = () => {
    if (user.subscription_plan === 'enterprise') return 0 // Ilimitado
    return (user.images_processed / user.images_limit) * 100
  }

  const getPlanColor = (plan) => {
    const colors = {
      free: 'bg-gray-100 text-gray-800',
      basic: 'bg-blue-100 text-blue-800',
      pro: 'bg-purple-100 text-purple-800',
      enterprise: 'bg-gold-100 text-gold-800'
    }
    return colors[plan] || colors.free
  }

  const getPlanName = (plan) => {
    const names = {
      free: 'Gratuito',
      basic: 'Básico',
      pro: 'Pro',
      enterprise: 'Empresarial'
    }
    return names[plan] || 'Gratuito'
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
            <p className="text-gray-600">Bem-vindo, {user.name}!</p>
          </div>
          <Button variant="outline" onClick={handleLogout} disabled={loading}>
            <LogOut className="mr-2 h-4 w-4" />
            {loading ? 'Saindo...' : 'Sair'}
          </Button>
        </div>

        <div className="grid md:grid-cols-2 gap-6 mb-8">
          {/* Informações do Usuário */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <User className="mr-2 h-5 w-5" />
                Perfil
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <p className="text-sm text-gray-600">Nome</p>
                <p className="font-medium">{user.name}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Email</p>
                <p className="font-medium">{user.email}</p>
              </div>
              <div>
                <p className="text-sm text-gray-600">Plano</p>
                <Badge className={getPlanColor(user.subscription_plan)}>
                  {user.subscription_plan === 'enterprise' && <Crown className="mr-1 h-3 w-3" />}
                  {getPlanName(user.subscription_plan)}
                </Badge>
              </div>
            </CardContent>
          </Card>

          {/* Uso da Conta */}
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center">
                <ImageIcon className="mr-2 h-5 w-5" />
                Uso da Conta
              </CardTitle>
            </CardHeader>
            <CardContent className="space-y-4">
              <div>
                <div className="flex justify-between items-center mb-2">
                  <p className="text-sm text-gray-600">Imagens Processadas</p>
                  <p className="text-sm font-medium">
                    {user.images_processed} / {user.subscription_plan === 'enterprise' ? '∞' : user.images_limit}
                  </p>
                </div>
                {user.subscription_plan !== 'enterprise' && (
                  <Progress value={getUsagePercentage()} className="mb-2" />
                )}
              </div>
              
              {user.subscription_plan !== 'enterprise' && getUsagePercentage() > 80 && (
                <div className="bg-yellow-50 border border-yellow-200 rounded-lg p-3">
                  <p className="text-sm text-yellow-800">
                    Você está próximo do limite do seu plano. 
                    <a href="#pricing" className="font-medium underline ml-1">
                      Considere fazer upgrade
                    </a>
                  </p>
                </div>
              )}
            </CardContent>
          </Card>
        </div>

        {/* Ações Rápidas */}
        <div className="grid md:grid-cols-3 gap-6">
          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="bg-blue-100 rounded-full p-3 w-fit mx-auto mb-3">
                  <Zap className="h-6 w-6 text-blue-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Processar Imagem</h3>
                <p className="text-sm text-gray-600 mb-4">
                  Aumente a resolução de suas imagens com IA
                </p>
                <Button 
                  className="w-full"
                  onClick={() => onNavigate && onNavigate('tool')}
                >
                  Ir para Ferramenta
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="bg-green-100 rounded-full p-3 w-fit mx-auto mb-3">
                  <Settings className="h-6 w-6 text-green-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Configurações</h3>
                <p className="text-sm text-gray-600 mb-4">
                  Gerencie suas preferências e dados
                </p>
                <Button variant="outline" className="w-full">
                  Configurar
                </Button>
              </div>
            </CardContent>
          </Card>

          <Card className="hover:shadow-lg transition-shadow cursor-pointer">
            <CardContent className="pt-6">
              <div className="text-center">
                <div className="bg-purple-100 rounded-full p-3 w-fit mx-auto mb-3">
                  <Crown className="h-6 w-6 text-purple-600" />
                </div>
                <h3 className="font-semibold text-gray-900 mb-2">Upgrade</h3>
                <p className="text-sm text-gray-600 mb-4">
                  Desbloqueie recursos premium
                </p>
                <Button 
                  variant="outline" 
                  className="w-full"
                  onClick={() => onNavigate && onNavigate('payment')}
                >
                  Ver Planos
                </Button>
              </div>
            </CardContent>
          </Card>
        </div>
      </div>
    </div>
  )
}

export default Dashboard

