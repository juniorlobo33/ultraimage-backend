from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    subscription_plan = db.Column(db.String(50), default='free')
    images_processed = db.Column(db.Integer, default=0)
    images_limit = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relacionamento com jobs de processamento
    processing_jobs = db.relationship('ProcessingJob', backref='user', lazy=True)
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'subscription_plan': self.subscription_plan,
            'images_processed': self.images_processed,
            'images_limit': self.images_limit,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ProcessingJob(db.Model):
    __tablename__ = 'processing_jobs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    status = db.Column(db.String(20), default='pending')  # pending, uploaded, processing, completed, failed
    input_path = db.Column(db.String(255), nullable=True)
    output_path = db.Column(db.String(255), nullable=True)
    original_filename = db.Column(db.String(255), nullable=True)
    file_size = db.Column(db.Integer, nullable=True)
    replicate_prediction_id = db.Column(db.String(255), nullable=True)
    error_message = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime, nullable=True)
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'status': self.status,
            'original_filename': self.original_filename,
            'file_size': self.file_size,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None
        }

