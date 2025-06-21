from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # UUID
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    subscription_plan = db.Column(db.String(20), default='free')  # free, basic, pro, enterprise
    images_processed = db.Column(db.Integer, default=0)
    images_limit = db.Column(db.Integer, default=5)  # Limite baseado no plano
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f'<User {self.email}>'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'subscription_plan': self.subscription_plan,
            'images_processed': self.images_processed,
            'images_limit': self.images_limit,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'is_active': self.is_active
        }
    
    def can_process_image(self):
        """Verifica se o usuário pode processar mais imagens"""
        if self.subscription_plan == 'enterprise':
            return True  # Ilimitado
        return self.images_processed < self.images_limit
    
    def increment_usage(self):
        """Incrementa o contador de imagens processadas"""
        self.images_processed += 1
        self.updated_at = datetime.utcnow()
    
    def update_subscription(self, plan):
        """Atualiza o plano de assinatura e os limites"""
        self.subscription_plan = plan
        
        # Definir limites baseados no plano
        limits = {
            'free': 5,
            'basic': 50,
            'pro': 200,
            'enterprise': -1  # Ilimitado
        }
        
        self.images_limit = limits.get(plan, 5)
        self.updated_at = datetime.utcnow()

class ProcessingJob(db.Model):
    """Modelo para rastrear jobs de processamento"""
    id = db.Column(db.String(36), primary_key=True)  # UUID
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'), nullable=False)
    original_filename = db.Column(db.String(255), nullable=False)
    processed_filename = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pending')  # pending, processing, completed, failed
    scale = db.Column(db.Integer, default=2)
    replicate_prediction_id = db.Column(db.String(255))
    result_url = db.Column(db.Text)
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
    
    # Relacionamento
    user = db.relationship('User', backref=db.backref('processing_jobs', lazy=True))
    
    def __repr__(self):
        return f'<ProcessingJob {self.id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'original_filename': self.original_filename,
            'processed_filename': self.processed_filename,
            'status': self.status,
            'scale': self.scale,
            'result_url': self.result_url,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

