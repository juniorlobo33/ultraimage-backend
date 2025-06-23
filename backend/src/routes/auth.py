from flask import Blueprint, request, jsonify, session
from werkzeug.security import generate_password_hash, check_password_hash
from src.models.user import User, db
import uuid
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    """Valida formato do email"""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    """Valida força da senha"""
    if len(password) < 8:
        return False, "Senha deve ter pelo menos 8 caracteres"
    if not re.search(r'[A-Z]', password):
        return False, "Senha deve conter pelo menos uma letra maiúscula"
    if not re.search(r'[a-z]', password):
        return False, "Senha deve conter pelo menos uma letra minúscula"
    if not re.search(r'\d', password):
        return False, "Senha deve conter pelo menos um número"
    return True, "Senha válida"

@auth_bp.route('/register', methods=['POST'])
def register():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        name = data.get('name', '').strip()
        
        # Validações
        if not email or not password or not name:
            return jsonify({'error': 'Email, senha e nome são obrigatórios'}), 400
        
        if not validate_email(email):
            return jsonify({'error': 'Email inválido'}), 400
        
        is_valid, message = validate_password(password)
        if not is_valid:
            return jsonify({'error': message}), 400
        
        # Verificar se usuário já existe
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({'error': 'Email já cadastrado'}), 409
        
        # Criar novo usuário
        user = User(
            id=str(uuid.uuid4()),
            email=email,
            name=name,
            password_hash=generate_password_hash(password),
            subscription_plan='free',
            images_processed=0,
            images_limit=5  # Limite gratuito
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuário criado com sucesso',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'subscription_plan': user.subscription_plan,
                'images_limit': user.images_limit,
                'images_processed': user.images_processed
            }
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro no registro: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Dados não fornecidos'}), 400
        
        email = data.get('email', '').strip().lower()
        password = data.get('password', '')
        
        if not email or not password:
            return jsonify({'error': 'Email e senha são obrigatórios'}), 400
        
        # Buscar usuário
        user = User.query.filter_by(email=email).first()
        
        if not user or not check_password_hash(user.password_hash, password):
            return jsonify({'error': 'Email ou senha incorretos'}), 401
        
        # Criar sessão
        session['user_id'] = user.id
        session['user_email'] = user.email
        
        return jsonify({
            'message': 'Login realizado com sucesso',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'subscription_plan': user.subscription_plan,
                'images_limit': user.images_limit,
                'images_processed': user.images_processed
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro no login: {str(e)}'}), 500

@auth_bp.route('/logout', methods=['POST'])
def logout():
    try:
        session.clear()
        return jsonify({'message': 'Logout realizado com sucesso'}), 200
    except Exception as e:
        return jsonify({'error': f'Erro no logout: {str(e)}'}), 500

@auth_bp.route('/profile', methods=['GET'])
def get_profile():
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'Usuário não autenticado'}), 401
        
        user = User.query.get(user_id)
        
        if not user:
            return jsonify({'error': 'Usuário não encontrado'}), 404
        
        return jsonify({
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'subscription_plan': user.subscription_plan,
                'images_limit': user.images_limit,
                'images_processed': user.images_processed,
                'created_at': user.created_at.isoformat() if user.created_at else None
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao buscar perfil: {str(e)}'}), 500

@auth_bp.route('/profile', methods=['PUT'])
def update_profile():
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'error': 'Usuário não autenticado'}), 401
        
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
            if email and validate_email(email):
                # Verificar se email já existe
                existing_user = User.query.filter_by(email=email).filter(User.id != user_id).first()
                if existing_user:
                    return jsonify({'error': 'Email já está em uso'}), 409
                user.email = email
                session['user_email'] = email
        
        db.session.commit()
        
        return jsonify({
            'message': 'Perfil atualizado com sucesso',
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'subscription_plan': user.subscription_plan,
                'images_limit': user.images_limit,
                'images_processed': user.images_processed
            }
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Erro ao atualizar perfil: {str(e)}'}), 500

@auth_bp.route('/check-auth', methods=['GET', 'POST'])
def check_auth():
    """Verifica se o usuário está autenticado"""
    try:
        user_id = session.get('user_id')
        
        if not user_id:
            return jsonify({'authenticated': False}), 200
        
        user = User.query.get(user_id)
        
        if not user:
            session.clear()
            return jsonify({'authenticated': False}), 200
        
        return jsonify({
            'authenticated': True,
            'user': {
                'id': user.id,
                'email': user.email,
                'name': user.name,
                'subscription_plan': user.subscription_plan,
                'images_limit': user.images_limit,
                'images_processed': user.images_processed
            }
        }), 200
        
    except Exception as e:
        return jsonify({'error': f'Erro ao verificar autenticação: {str(e)}'}), 500

