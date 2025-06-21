from flask import Blueprint, request, jsonify, session
from src.models.user import User, db
import uuid

payment_bp = Blueprint('payment', __name__)

# Configurações dos planos
PLANS = {
    'basic': {
        'name': 'Básico',
        'price': 29.00,
        'currency': 'BRL',
        'images_limit': 50,
        'features': [
            '50 imagens por mês',
            'Resolução até 4K',
            'Suporte por email',
            'Processamento padrão'
        ]
    },
    'pro': {
        'name': 'Pro',
        'price': 79.00,
        'currency': 'BRL',
        'images_limit': 200,
        'features': [
            '200 imagens por mês',
            'Resolução até 8K',
            'Suporte prioritário',
            'Processamento rápido',
            'API de integração'
        ]
    },
    'enterprise': {
        'name': 'Empresarial',
        'price': 199.00,
        'currency': 'BRL',
        'images_limit': -1,  # Ilimitado
        'features': [
            'Imagens ilimitadas',
            'Resolução até 16K',
            'Suporte 24/7',
            'Processamento ultra-rápido',
            'API completa',
            'Gerenciamento de equipe'
        ]
    }
}

@payment_bp.route('/plans', methods=['GET'])
def get_plans():
    """Retorna todos os planos disponíveis"""
    try:
        return jsonify({
            'plans': PLANS
        }), 200
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar planos: {str(e)}'}), 500

@payment_bp.route('/create-payment-intent', methods=['POST'])
def create_payment_intent():
    """Cria uma intenção de pagamento (simulação)"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'Usuário não autenticado'}), 401
        
        data = request.get_json()
        
        if not data or 'plan' not in data:
            return jsonify({'error': 'Plano não especificado'}), 400
        
        plan_id = data['plan']
        
        if plan_id not in PLANS:
            return jsonify({'error': 'Plano inválido'}), 400
        
        plan = PLANS[plan_id]
        
        # Simulação de criação de payment intent
        # Em produção, aqui você integraria com Stripe, Mercado Pago, etc.
        payment_intent = {
            'id': f'pi_{uuid.uuid4().hex[:24]}',
            'amount': int(plan['price'] * 100),  # Centavos
            'currency': plan['currency'].lower(),
            'status': 'requires_payment_method',
            'client_secret': f'pi_{uuid.uuid4().hex[:24]}_secret_{uuid.uuid4().hex[:16]}'
        }
        
        return jsonify({
            'payment_intent': payment_intent,
            'plan': plan
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao criar intenção de pagamento: {str(e)}'}), 500

@payment_bp.route('/confirm-payment', methods=['POST'])
def confirm_payment():
    """Confirma o pagamento e atualiza a assinatura do usuário"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'Usuário não autenticado'}), 401
        
        data = request.get_json()
        
        if not data or 'payment_intent_id' not in data or 'plan' not in data:
            return jsonify({'error': 'Dados de pagamento incompletos'}), 400
        
        payment_intent_id = data['payment_intent_id']
        plan_id = data['plan']
        
        if plan_id not in PLANS:
            return jsonify({'error': 'Plano inválido'}), 400
        
        # Buscar usuário
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Simular verificação do pagamento
        # Em produção, você verificaria o status real do pagamento
        payment_successful = True  # Simulação
        
        if payment_successful:
            # Atualizar assinatura do usuário
            user.update_subscription(plan_id)
            db.session.commit()
            
            return jsonify({
                'message': 'Pagamento confirmado com sucesso',
                'subscription': {
                    'plan': plan_id,
                    'plan_name': PLANS[plan_id]['name'],
                    'images_limit': user.images_limit,
                    'status': 'active'
                }
            }), 200
        else:
            return jsonify({'error': 'Falha na verificação do pagamento'}), 400
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao confirmar pagamento: {str(e)}'}), 500

@payment_bp.route('/subscription', methods=['GET'])
def get_subscription():
    """Retorna informações da assinatura atual do usuário"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'Usuário não autenticado'}), 401
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        plan_info = PLANS.get(user.subscription_plan, {
            'name': 'Gratuito',
            'price': 0,
            'currency': 'BRL',
            'features': ['5 imagens por mês', 'Resolução até 2K']
        })
        
        return jsonify({
            'subscription': {
                'plan': user.subscription_plan,
                'plan_name': plan_info['name'],
                'images_processed': user.images_processed,
                'images_limit': user.images_limit,
                'status': 'active' if user.subscription_plan != 'free' else 'free'
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar assinatura: {str(e)}'}), 500

@payment_bp.route('/cancel-subscription', methods=['POST'])
def cancel_subscription():
    """Cancela a assinatura do usuário"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'Usuário não autenticado'}), 401
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Reverter para plano gratuito
        user.update_subscription('free')
        db.session.commit()
        
        return jsonify({
            'message': 'Assinatura cancelada com sucesso',
            'subscription': {
                'plan': 'free',
                'plan_name': 'Gratuito',
                'images_limit': user.images_limit,
                'status': 'cancelled'
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao cancelar assinatura: {str(e)}'}), 500

# Simulação de webhooks para diferentes gateways de pagamento
@payment_bp.route('/webhook/stripe', methods=['POST'])
def stripe_webhook():
    """Webhook para processar eventos do Stripe"""
    try:
        # Em produção, você verificaria a assinatura do webhook
        data = request.get_json()
        
        # Processar diferentes tipos de eventos
        event_type = data.get('type')
        
        if event_type == 'payment_intent.succeeded':
            # Pagamento bem-sucedido
            pass
        elif event_type == 'invoice.payment_failed':
            # Falha no pagamento
            pass
        elif event_type == 'customer.subscription.deleted':
            # Assinatura cancelada
            pass
        
        return jsonify({'received': True}), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro no webhook: {str(e)}'}), 500

@payment_bp.route('/webhook/mercadopago', methods=['POST'])
def mercadopago_webhook():
    """Webhook para processar eventos do Mercado Pago"""
    try:
        data = request.get_json()
        
        # Processar notificações do Mercado Pago
        # Em produção, você verificaria a autenticidade da notificação
        
        return jsonify({'received': True}), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro no webhook: {str(e)}'}), 500

