from flask import Blueprint, request, jsonify, session
from src.models.user import User, db
import uuid

user_bp = Blueprint('user', __name__)

@user_bp.route('/users', methods=['GET'])
def get_users():
    """Listar todos os usuários (apenas para admin)"""
    try:
        # Verificar se usuário está autenticado
        user_id = session.get('user_id')
        if not user_id:
            return jsonify({'error': 'Usuário não autenticado'}), 401
        
        # Em produção, adicionar verificação de admin
        users = User.query.all()
        users_data = [user.to_dict() for user in users]
        
        return jsonify({
            'users': users_data,
            'total': len(users_data)
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar usuários: {str(e)}'}), 500

@user_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    """Buscar usuário específico"""
    try:
        # Verificar se usuário está autenticado
        current_user_id = session.get('user_id')
        if not current_user_id:
            return jsonify({'error': 'Usuário não autenticado'}), 401
        
        # Usuário só pode ver seus próprios dados (ou admin pode ver todos)
        if current_user_id != user_id:
            return jsonify({'error': 'Acesso negado'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({'user': user.to_dict()}), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar usuário: {str(e)}'}), 500

@user_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    """Atualizar dados do usuário"""
    try:
        # Verificar se usuário está autenticado
        current_user_id = session.get('user_id')
        if not current_user_id:
            return jsonify({'error': 'Usuário não autenticado'}), 401
        
        # Usuário só pode atualizar seus próprios dados
        if current_user_id != user_id:
            return jsonify({'error': 'Acesso negado'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        # Atualizar campos permitidos
        if 'name' in data:
            name = data['name'].strip()
            if name:
                user.name = name
        
        if 'email' in data:
            email = data['email'].strip().lower()
            if email:
                # Verificar se email já existe
                existing_user = User.query.filter_by(email=email).filter(User.id != user_id).first()
                if existing_user:
                    return jsonify({'error': 'Email já está em uso'}), 409
                user.email = email
                session['user_email'] = email
        
        db.session.commit()
        
        return jsonify({
            'message': 'Usuário atualizado com sucesso',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar usuário: {str(e)}'}), 500

@user_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    """Deletar usuário"""
    try:
        # Verificar se usuário está autenticado
        current_user_id = session.get('user_id')
        if not current_user_id:
            return jsonify({'error': 'Usuário não autenticado'}), 401
        
        # Usuário só pode deletar sua própria conta
        if current_user_id != user_id:
            return jsonify({'error': 'Acesso negado'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Marcar como inativo ao invés de deletar
        user.is_active = False
        db.session.commit()
        
        # Limpar sessão
        session.clear()
        
        return jsonify({'message': 'Conta desativada com sucesso'}), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao desativar conta: {str(e)}'}), 500

@user_bp.route('/users/<user_id>/subscription', methods=['PUT'])
def update_subscription(user_id):
    """Atualizar plano de assinatura do usuário"""
    try:
        # Verificar se usuário está autenticado
        current_user_id = session.get('user_id')
        if not current_user_id:
            return jsonify({'error': 'Usuário não autenticado'}), 401
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        data = request.get_json()
        if not data or 'plan' not in data:
            return jsonify({'error': 'Plano não fornecido'}), 400
        
        plan = data['plan']
        valid_plans = ['free', 'basic', 'pro', 'enterprise']
        
        if plan not in valid_plans:
            return jsonify({'error': f'Plano inválido. Opções: {valid_plans}'}), 400
        
        # Atualizar assinatura
        user.update_subscription(plan)
        db.session.commit()
        
        return jsonify({
            'message': 'Assinatura atualizada com sucesso',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar assinatura: {str(e)}'}), 500

@user_bp.route('/users/<user_id>/usage', methods=['GET'])
def get_usage(user_id):
    """Buscar estatísticas de uso do usuário"""
    try:
        # Verificar se usuário está autenticado
        current_user_id = session.get('user_id')
        if not current_user_id:
            return jsonify({'error': 'Usuário não autenticado'}), 401
        
        # Usuário só pode ver suas próprias estatísticas
        if current_user_id != user_id:
            return jsonify({'error': 'Acesso negado'}), 403
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Calcular estatísticas
        remaining_images = max(0, user.images_limit - user.images_processed) if user.images_limit > 0 else -1
        usage_percentage = (user.images_processed / user.images_limit * 100) if user.images_limit > 0 else 0
        
        return jsonify({
            'user_id': user.id,
            'subscription_plan': user.subscription_plan,
            'images_processed': user.images_processed,
            'images_limit': user.images_limit,
            'remaining_images': remaining_images,
            'usage_percentage': round(usage_percentage, 2),
            'can_process_more': user.can_process_image()
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar estatísticas: {str(e)}'}), 500

@user_bp.route('/users/<user_id>/reset-usage', methods=['POST'])
def reset_usage(user_id):
    """Resetar contador de uso (apenas para admin ou renovação de plano)"""
    try:
        # Verificar se usuário está autenticado
        current_user_id = session.get('user_id')
        if not current_user_id:
            return jsonify({'error': 'Usuário não autenticado'}), 401
        
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        # Resetar contador
        user.images_processed = 0
        db.session.commit()
        
        return jsonify({
            'message': 'Contador de uso resetado com sucesso',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao resetar contador: {str(e)}'}), 500

