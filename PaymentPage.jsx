import { useState } from 'react'
import { Button } from '@/components/ui/button.jsx'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card.jsx'
import { Badge } from '@/components/ui/badge.jsx'
import { Check, Crown, Zap, Star } from 'lucide-react'
import '../App.css'

function PaymentPage({ user, onPaymentSuccess }) {
  const [loading, setLoading] = useState(false)
  const [selectedPlan, setSelectedPlan] = useState(null)
  const [plans, setPlans] = useState({
    basic: {
      name: 'Básico',
      price: 29.00,
      currency: 'BRL',
      images_limit: 50,
      features: [
        '50 imagens por mês',
        'Resolução até 4K',
        'Suporte por email',
        'Processamento padrão'
      ]
    },
    pro: {
      name: 'Pro',
      price: 79.00,
      currency: 'BRL',
      images_limit: 200,
      features: [
        '200 imagens por mês',
        'Resolução até 8K',
        'Suporte prioritário',
        'Processamento rápido',
        'API de integração'
      ]
    },
    enterprise: {
      name: 'Empresarial',
      price: 199.00,
      currency: 'BRL',
      images_limit: -1,
      features: [
        'Imagens ilimitadas',
        'Resolução até 16K',
        'Suporte 24/7',
        'Processamento ultra-rápido',
        'API completa',
        'Gerenciamento de equipe'
      ]
    }
  })

  const handleSelectPlan = async (planId) => {
    setLoading(true)
    setSelectedPlan(planId)

    try {
      // Simular processo de pagamento
      await new Promise(resolve => setTimeout(resolve, 2000))

      // Simular confirmação de pagamento
      const response = await fetch('http://localhost:5000/api/payment/confirm-payment', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        credentials: 'include',
        body: JSON.stringify({
          payment_intent_id: `pi_${Date.now()}`,
          plan: planId
        })
      })

      if (response.ok) {
        const result = await response.json()
        alert(`Pagamento confirmado! Bem-vindo ao plano ${plans[planId].name}!`)
        if (onPaymentSuccess) {
          onPaymentSuccess(result.subscription)
        }
      } else {
        const error = await response.json()
        alert(`Erro no pagamento: ${error.error}`)
      }
    } catch (error) {
      console.error('Erro no pagamento:', error)
      alert('Erro ao processar pagamento. Tente novamente.')
    } finally {
      setLoading(false)
      setSelectedPlan(null)
    }
  }

  const getPlanIcon = (planId) => {
    switch (planId) {
      case 'basic':
        return <Star className="h-6 w-6 text-blue-600" />
      case 'pro':
        return <Zap className="h-6 w-6 text-purple-600" />
      case 'enterprise':
        return <Crown className="h-6 w-6 text-yellow-600" />
      default:
        return <Star className="h-6 w-6" />
    }
  }

  const getPlanColor = (planId) => {
    switch (planId) {
      case 'basic':
        return 'border-blue-200 hover:border-blue-300'
      case 'pro':
        return 'border-purple-200 hover:border-purple-300 ring-2 ring-purple-200'
      case 'enterprise':
        return 'border-yellow-200 hover:border-yellow-300'
      default:
        return 'border-gray-200'
    }
  }

  return (
    <div className="min-h-screen bg-gray-50 py-12">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="text-center mb-12">
          <h1 className="text-4xl font-bold text-gray-900 mb-4">
            Escolha seu Plano
          </h1>
          <p className="text-xl text-gray-600 max-w-2xl mx-auto">
            Selecione o plano ideal para suas necessidades de processamento de imagens
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 max-w-5xl mx-auto">
          {Object.entries(plans).map(([planId, plan]) => (
            <Card 
              key={planId} 
              className={`relative transition-all duration-200 ${getPlanColor(planId)} ${
                planId === 'pro' ? 'transform scale-105' : ''
              }`}
            >
              {planId === 'pro' && (
                <div className="absolute -top-4 left-1/2 transform -translate-x-1/2">
                  <Badge className="bg-purple-600 text-white px-4 py-1">
                    Mais Popular
                  </Badge>
                </div>
              )}
              
              <CardHeader className="text-center pb-4">
                <div className="flex justify-center mb-4">
                  {getPlanIcon(planId)}
                </div>
                <CardTitle className="text-2xl font-bold">
                  {plan.name}
                </CardTitle>
                <div className="mt-4">
                  <span className="text-4xl font-bold text-gray-900">
                    R$ {plan.price.toFixed(0)}
                  </span>
                  <span className="text-gray-600">/mês</span>
                </div>
                <CardDescription className="mt-2">
                  {planId === 'basic' && 'Perfeito para uso pessoal'}
                  {planId === 'pro' && 'Ideal para profissionais'}
                  {planId === 'enterprise' && 'Para equipes e empresas'}
                </CardDescription>
              </CardHeader>

              <CardContent>
                <ul className="space-y-3 mb-6">
                  {plan.features.map((feature, index) => (
                    <li key={index} className="flex items-center">
                      <Check className="h-5 w-5 text-green-500 mr-3 flex-shrink-0" />
                      <span className="text-gray-700">{feature}</span>
                    </li>
                  ))}
                </ul>

                <Button
                  onClick={() => handleSelectPlan(planId)}
                  disabled={loading}
                  className={`w-full ${
                    planId === 'basic' 
                      ? 'bg-blue-600 hover:bg-blue-700' 
                      : planId === 'pro'
                      ? 'bg-purple-600 hover:bg-purple-700'
                      : 'bg-yellow-600 hover:bg-yellow-700'
                  } text-white`}
                >
                  {loading && selectedPlan === planId ? (
                    <div className="flex items-center">
                      <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-white mr-2"></div>
                      Processando...
                    </div>
                  ) : (
                    `Escolher ${plan.name}`
                  )}
                </Button>
              </CardContent>
            </Card>
          ))}
        </div>

        <div className="mt-12 text-center">
          <div className="bg-white rounded-lg shadow-sm p-6 max-w-2xl mx-auto">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">
              Métodos de Pagamento Aceitos
            </h3>
            <div className="flex justify-center space-x-6 text-sm text-gray-600">
              <div className="flex items-center">
                <div className="w-8 h-5 bg-blue-600 rounded mr-2"></div>
                Cartão de Crédito
              </div>
              <div className="flex items-center">
                <div className="w-8 h-5 bg-green-600 rounded mr-2"></div>
                PIX
              </div>
              <div className="flex items-center">
                <div className="w-8 h-5 bg-yellow-600 rounded mr-2"></div>
                Boleto
              </div>
            </div>
            <p className="text-xs text-gray-500 mt-4">
              Pagamentos processados com segurança. Cancele a qualquer momento.
            </p>
          </div>
        </div>
      </div>
    </div>
  )
}

export default PaymentPage

