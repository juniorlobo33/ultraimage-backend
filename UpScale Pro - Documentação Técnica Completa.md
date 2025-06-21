# UpScale Pro - Documentação Técnica Completa

## Visão Geral do Projeto

O **UpScale Pro** é uma plataforma web completa para processamento de imagens usando inteligência artificial, especificamente o modelo Real-ESRGAN para aumento de resolução. O sistema inclui autenticação de usuários, sistema de assinaturas com múltiplos planos e integração com APIs de pagamento.

## Arquitetura do Sistema

### Frontend (React + Vite)
- **Framework**: React 18 com Vite
- **Estilização**: Tailwind CSS + shadcn/ui
- **Ícones**: Lucide React
- **Navegação**: Sistema de navegação customizado (sem React Router)
- **Responsividade**: Design totalmente responsivo para desktop e mobile

### Backend (Flask + Python)
- **Framework**: Flask com Python 3.11
- **Banco de Dados**: SQLite com SQLAlchemy ORM
- **Autenticação**: Sistema de sessões com cookies
- **CORS**: Configurado para comunicação frontend-backend
- **APIs**: RESTful APIs para todas as funcionalidades

### Integração Externa
- **Replicate API**: Para processamento de imagens com Real-ESRGAN
- **Sistemas de Pagamento**: Simulação para Kiwify, Hotmart, Eduzz, Stripe, Mercado Pago

## Estrutura de Arquivos

```
image-upscale-site/
├── frontend/                 # Aplicação React
│   ├── src/
│   │   ├── components/      # Componentes React
│   │   │   ├── AuthPage.jsx
│   │   │   ├── Dashboard.jsx
│   │   │   ├── PaymentPage.jsx
│   │   │   └── UploadTool.jsx
│   │   ├── App.jsx          # Componente principal
│   │   └── App.css          # Estilos globais
│   ├── index.html
│   └── package.json
└── backend/                  # API Flask
    ├── src/
    │   ├── models/          # Modelos de dados
    │   │   └── user.py
    │   ├── routes/          # Rotas da API
    │   │   ├── auth.py
    │   │   ├── image.py
    │   │   ├── payment.py
    │   │   └── user.py
    │   ├── services/        # Serviços externos
    │   │   └── replicate_service.py
    │   └── main.py          # Aplicação principal
    ├── uploads/             # Arquivos temporários
    ├── processed/           # Imagens processadas
    └── requirements.txt
```

## Funcionalidades Implementadas

### 1. Sistema de Autenticação
- **Registro de usuários** com validação de email e senha
- **Login/Logout** com gerenciamento de sessões
- **Verificação automática** de autenticação
- **Proteção de rotas** para áreas restritas

### 2. Processamento de Imagens
- **Upload de imagens** com drag & drop
- **Integração com Replicate API** para Real-ESRGAN
- **Processamento assíncrono** com acompanhamento de status
- **Download de resultados** processados
- **Suporte a múltiplos formatos**: PNG, JPG, JPEG, GIF, WebP

### 3. Sistema de Assinaturas
- **Três planos disponíveis**:
  - **Gratuito**: 5 imagens/mês
  - **Básico**: 50 imagens/mês - R$ 29
  - **Pro**: 200 imagens/mês - R$ 79
  - **Empresarial**: Ilimitado - R$ 199

### 4. Sistema de Pagamentos
- **Múltiplos métodos**: Cartão, PIX, Boleto
- **Simulação de pagamento** para desenvolvimento
- **Webhooks** para confirmação automática
- **Atualização automática** de planos e limites

### 5. Dashboard do Usuário
- **Perfil completo** com informações do usuário
- **Monitoramento de uso** (imagens processadas vs limite)
- **Plano atual** e recursos disponíveis
- **Ações rápidas** para principais funcionalidades

## APIs Implementadas

### Autenticação (`/api/auth/`)
- `POST /register` - Registro de novo usuário
- `POST /login` - Login do usuário
- `POST /logout` - Logout do usuário
- `GET /check-auth` - Verificar autenticação atual

### Processamento de Imagens (`/api/`)
- `POST /upload` - Upload de imagem
- `POST /process` - Iniciar processamento
- `GET /status/<job_id>` - Verificar status do processamento
- `GET /download/<job_id>` - Download da imagem processada

### Pagamentos (`/api/payment/`)
- `GET /plans` - Listar planos disponíveis
- `POST /create-payment-intent` - Criar intenção de pagamento
- `POST /confirm-payment` - Confirmar pagamento
- `POST /webhook` - Webhook para notificações

### Usuários (`/api/`)
- `GET /users` - Listar usuários (admin)
- `GET /users/<id>` - Obter usuário específico
- `PUT /users/<id>` - Atualizar usuário
- `DELETE /users/<id>` - Deletar usuário

## Modelos de Dados

### User
```python
class User(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # UUID
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    subscription_plan = db.Column(db.String(20), default='free')
    images_processed = db.Column(db.Integer, default=0)
    images_limit = db.Column(db.Integer, default=5)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
```

### ProcessingJob
```python
class ProcessingJob(db.Model):
    id = db.Column(db.String(36), primary_key=True)  # UUID
    user_id = db.Column(db.String(36), db.ForeignKey('user.id'))
    original_filename = db.Column(db.String(255), nullable=False)
    processed_filename = db.Column(db.String(255))
    status = db.Column(db.String(20), default='pending')
    scale = db.Column(db.Integer, default=2)
    replicate_prediction_id = db.Column(db.String(255))
    result_url = db.Column(db.Text)
    error_message = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    completed_at = db.Column(db.DateTime)
```



## Configuração e Instalação

### Pré-requisitos
- Python 3.11+
- Node.js 20+
- npm/pnpm
- Conta no Replicate (para produção)

### Instalação do Backend

1. **Criar ambiente virtual**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
venv\Scripts\activate     # Windows
```

2. **Instalar dependências**:
```bash
pip install -r requirements.txt
```

3. **Configurar variáveis de ambiente**:
```bash
export REPLICATE_API_TOKEN="seu_token_aqui"
export FLASK_SECRET_KEY="sua_chave_secreta"
```

4. **Inicializar banco de dados**:
```bash
python src/main.py
```

### Instalação do Frontend

1. **Instalar dependências**:
```bash
cd frontend
pnpm install
```

2. **Iniciar servidor de desenvolvimento**:
```bash
pnpm run dev
```

### Configuração de Produção

#### Backend (Flask)
```python
# Configurações de produção
app.config['DEBUG'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://...'  # PostgreSQL
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
```

#### Frontend (React)
```bash
# Build para produção
pnpm run build

# Servir arquivos estáticos
pnpm run preview
```

## Integração com Replicate

### Configuração da API
```python
import replicate

# Configurar cliente
replicate_client = replicate.Client(api_token=os.environ.get('REPLICATE_API_TOKEN'))

# Processar imagem
output = replicate_client.run(
    "nightmareai/real-esrgan:42fed1c4974146d4d2414e2be2c5277c7fcf05fcc3a73abf41610695738c1d7b",
    input={
        "image": image_url,
        "scale": 2,  # 2x, 4x, ou 8x
        "face_enhance": False
    }
)
```

### Modelos Disponíveis
- **Real-ESRGAN**: Aumento de resolução geral
- **GFPGAN**: Focado em rostos
- **ESRGAN**: Versão anterior, mais rápida

### Custos Estimados
- **Real-ESRGAN**: ~$0.005-0.015 por imagem
- **Processamento médio**: 10-30 segundos
- **Limite de tamanho**: 25MB por imagem

## Sistema de Pagamentos

### Integração com Gateways

#### Stripe (Internacional)
```javascript
// Frontend
const stripe = Stripe('pk_test_...');

// Criar Payment Intent
const response = await fetch('/api/payment/create-payment-intent', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ plan: 'pro', amount: 7900 })
});
```

#### Mercado Pago (Brasil)
```python
# Backend
import mercadopago

mp = mercadopago.SDK("ACCESS_TOKEN")

preference_data = {
    "items": [{
        "title": "Plano Pro - UpScale Pro",
        "quantity": 1,
        "unit_price": 79.00
    }]
}
```

### Webhooks
```python
@payment_bp.route('/webhook', methods=['POST'])
def handle_webhook():
    payload = request.get_json()
    
    # Verificar assinatura
    if verify_webhook_signature(payload):
        # Processar pagamento
        update_user_subscription(payload['user_id'], payload['plan'])
        return jsonify({'status': 'success'})
    
    return jsonify({'error': 'Invalid signature'}), 400
```

## Segurança

### Autenticação
- **Senhas**: Hash com bcrypt
- **Sessões**: Cookies seguros com HTTPOnly
- **CSRF**: Proteção contra ataques CSRF
- **Rate Limiting**: Limitação de tentativas de login

### Validação de Dados
```python
# Validação de upload
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
MAX_FILE_SIZE = 25 * 1024 * 1024  # 25MB

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
```

### Sanitização
- **Nomes de arquivo**: Sanitização para evitar path traversal
- **Input do usuário**: Validação e escape de dados
- **SQL Injection**: Uso de ORM (SQLAlchemy)

## Monitoramento e Logs

### Logs do Sistema
```python
import logging

# Configurar logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('app.log'),
        logging.StreamHandler()
    ]
)
```

### Métricas Importantes
- **Tempo de processamento** por imagem
- **Taxa de sucesso** do processamento
- **Uso de recursos** (CPU, memória)
- **Conversões** de planos pagos
- **Erros da API** do Replicate

## Performance

### Otimizações Frontend
- **Code Splitting**: Carregamento sob demanda
- **Lazy Loading**: Componentes carregados quando necessário
- **Compressão**: Gzip/Brotli para assets
- **CDN**: Servir assets estáticos

### Otimizações Backend
- **Cache**: Redis para sessões e dados frequentes
- **Conexão Pool**: Para banco de dados
- **Async Processing**: Celery para tarefas longas
- **Load Balancing**: Múltiplas instâncias

### Banco de Dados
```sql
-- Índices importantes
CREATE INDEX idx_user_email ON user(email);
CREATE INDEX idx_processing_job_user_id ON processing_job(user_id);
CREATE INDEX idx_processing_job_status ON processing_job(status);
```

## Testes

### Testes Unitários (Backend)
```python
import unittest
from src.main import app

class TestAuth(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        
    def test_register(self):
        response = self.app.post('/api/auth/register', json={
            'name': 'Test User',
            'email': 'test@example.com',
            'password': 'Test123!'
        })
        self.assertEqual(response.status_code, 201)
```

### Testes de Integração
```python
def test_image_processing_flow():
    # 1. Login
    login_response = client.post('/api/auth/login', json=login_data)
    
    # 2. Upload
    upload_response = client.post('/api/upload', files={'file': image_file})
    
    # 3. Process
    process_response = client.post('/api/process', json=process_data)
    
    # 4. Check status
    status_response = client.get(f'/api/status/{job_id}')
    
    assert status_response.json['status'] == 'completed'
```

### Testes Frontend (Jest)
```javascript
import { render, screen } from '@testing-library/react';
import AuthPage from './AuthPage';

test('renders login form', () => {
    render(<AuthPage />);
    const emailInput = screen.getByLabelText(/email/i);
    expect(emailInput).toBeInTheDocument();
});
```


## Deploy e Produção

### Opções de Deploy

#### 1. Vercel (Frontend) + Railway (Backend)
```bash
# Frontend no Vercel
npm install -g vercel
vercel --prod

# Backend no Railway
railway login
railway new
railway add
railway deploy
```

#### 2. Docker (Containerização)
```dockerfile
# Dockerfile.backend
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "src/main.py"]

# Dockerfile.frontend
FROM node:20-alpine
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build
EXPOSE 3000
CMD ["npm", "run", "preview"]
```

#### 3. AWS (Escalável)
- **Frontend**: S3 + CloudFront
- **Backend**: EC2 + Load Balancer
- **Banco**: RDS PostgreSQL
- **Storage**: S3 para imagens

### Variáveis de Ambiente

#### Backend (.env)
```bash
FLASK_ENV=production
SECRET_KEY=sua_chave_super_secreta
REPLICATE_API_TOKEN=r8_xxx
DATABASE_URL=postgresql://user:pass@host:5432/db
REDIS_URL=redis://localhost:6379
STRIPE_SECRET_KEY=sk_live_xxx
MERCADOPAGO_ACCESS_TOKEN=APP_USR_xxx
```

#### Frontend (.env.production)
```bash
VITE_API_URL=https://api.upscalepro.com
VITE_STRIPE_PUBLIC_KEY=pk_live_xxx
VITE_ENVIRONMENT=production
```

### Configuração de Domínio
```nginx
# nginx.conf
server {
    listen 80;
    server_name upscalepro.com www.upscalepro.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name upscalepro.com www.upscalepro.com;
    
    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;
    
    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /api/ {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## Manutenção e Monitoramento

### Backup do Banco de Dados
```bash
# PostgreSQL
pg_dump -h localhost -U user -d upscalepro > backup_$(date +%Y%m%d).sql

# Restaurar
psql -h localhost -U user -d upscalepro < backup_20250619.sql
```

### Monitoramento de Logs
```python
# Configuração de logs estruturados
import structlog

logger = structlog.get_logger()

# Log de processamento
logger.info("image_processing_started", 
           user_id=user.id, 
           filename=filename, 
           scale=scale)
```

### Alertas e Notificações
```python
# Integração com Slack/Discord
def send_alert(message, level="info"):
    webhook_url = os.environ.get('SLACK_WEBHOOK_URL')
    payload = {
        "text": f"[{level.upper()}] UpScale Pro: {message}",
        "username": "UpScale Bot"
    }
    requests.post(webhook_url, json=payload)

# Usar em casos de erro
try:
    process_image(image_data)
except Exception as e:
    send_alert(f"Erro no processamento: {str(e)}", "error")
```

## Roadmap e Melhorias Futuras

### Versão 2.0
- [ ] **API Pública**: Endpoints para desenvolvedores
- [ ] **Batch Processing**: Processamento em lote
- [ ] **Modelos Customizados**: Upload de modelos próprios
- [ ] **Colaboração**: Compartilhamento de projetos
- [ ] **Analytics**: Dashboard de métricas detalhadas

### Versão 2.1
- [ ] **Mobile App**: Aplicativo React Native
- [ ] **Integração Dropbox/Google Drive**: Importação direta
- [ ] **Watermark Removal**: Remoção de marcas d'água
- [ ] **Video Upscaling**: Processamento de vídeos
- [ ] **AI Background Removal**: Remoção de fundo

### Versão 2.2
- [ ] **White Label**: Solução para revenda
- [ ] **Multi-tenant**: Suporte a múltiplas empresas
- [ ] **Advanced Analytics**: Machine Learning insights
- [ ] **CDN Global**: Distribuição mundial
- [ ] **Enterprise Features**: SSO, LDAP, etc.

## Troubleshooting

### Problemas Comuns

#### 1. Erro de CORS
```python
# Solução: Configurar CORS corretamente
from flask_cors import CORS
CORS(app, supports_credentials=True, origins=['http://localhost:5173'])
```

#### 2. Timeout no Replicate
```python
# Solução: Implementar retry e timeout
import time
import requests

def process_with_retry(image_url, max_retries=3):
    for attempt in range(max_retries):
        try:
            result = replicate.run(model, input={"image": image_url})
            return result
        except Exception as e:
            if attempt == max_retries - 1:
                raise e
            time.sleep(2 ** attempt)  # Backoff exponencial
```

#### 3. Limite de Upload
```python
# Solução: Configurar limites adequados
app.config['MAX_CONTENT_LENGTH'] = 25 * 1024 * 1024  # 25MB
```

#### 4. Sessão Perdida
```python
# Solução: Configurar cookies corretamente
app.config['SESSION_COOKIE_SECURE'] = True  # HTTPS only
app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
```

### Logs de Debug
```python
# Ativar logs detalhados
import logging
logging.basicConfig(level=logging.DEBUG)

# Log específico para Replicate
replicate_logger = logging.getLogger('replicate')
replicate_logger.setLevel(logging.DEBUG)
```

## Contato e Suporte

### Documentação Adicional
- **API Reference**: `/docs` (Swagger/OpenAPI)
- **Changelog**: `CHANGELOG.md`
- **Contributing**: `CONTRIBUTING.md`

### Suporte Técnico
- **Email**: suporte@upscalepro.com
- **Discord**: [Servidor da Comunidade]
- **GitHub Issues**: [Repositório do Projeto]

### Licença
Este projeto está licenciado sob a MIT License. Veja o arquivo `LICENSE` para mais detalhes.

---

**Desenvolvido com ❤️ pela equipe UpScale Pro**

*Última atualização: 19 de Junho de 2025*

