# 🚀 UpScale Pro - Plataforma de Aumento de Resolução com IA

![UpScale Pro](https://img.shields.io/badge/UpScale%20Pro-v1.0-blue?style=for-the-badge)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
![Flask](https://img.shields.io/badge/Flask-2.3-000000?style=for-the-badge&logo=flask)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python)

> **Transforme suas imagens de baixa resolução em obras-primas de alta qualidade usando inteligência artificial avançada.**

## 📋 Visão Geral

O **UpScale Pro** é uma plataforma web completa que utiliza o modelo Real-ESRGAN para aumentar a resolução de imagens através de inteligência artificial. O sistema inclui autenticação de usuários, sistema de assinaturas com múltiplos planos e integração com diversos métodos de pagamento.

### ✨ Principais Funcionalidades

- 🖼️ **Aumento de Resolução com IA** - Tecnologia Real-ESRGAN
- 👤 **Sistema de Autenticação** - Login/registro seguro
- 💳 **Múltiplos Planos de Assinatura** - Gratuito, Básico, Pro e Empresarial
- 💰 **Pagamentos Integrados** - PIX, Cartão, Boleto
- 📱 **Design Responsivo** - Funciona em desktop e mobile
- ⚡ **Processamento Rápido** - Resultados em segundos
- 🔒 **Segurança Avançada** - Proteção de dados e privacidade

## 🏗️ Arquitetura

### Frontend
- **React 18** com Vite
- **Tailwind CSS** + shadcn/ui
- **Lucide React** para ícones
- Design responsivo e moderno

### Backend
- **Flask** com Python 3.11
- **SQLAlchemy** ORM
- **SQLite** (desenvolvimento) / **PostgreSQL** (produção)
- APIs RESTful

### Integrações
- **Replicate API** - Processamento de imagens
- **Sistemas de Pagamento** - Stripe, Mercado Pago, etc.

## 🚀 Instalação Rápida

### Pré-requisitos
- Python 3.11+
- Node.js 20+
- npm/pnpm

### 1. Clone o Repositório
```bash
git clone https://github.com/seu-usuario/upscale-pro.git
cd upscale-pro
```

### 2. Configure o Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou venv\Scripts\activate  # Windows

pip install -r requirements.txt
python src/main.py
```

### 3. Configure o Frontend
```bash
cd frontend
pnpm install
pnpm run dev
```

### 4. Acesse a Aplicação
- Frontend: http://localhost:5173
- Backend API: http://localhost:5000

## 📊 Planos e Preços

| Plano | Preço | Imagens/Mês | Resolução | Recursos |
|-------|-------|-------------|-----------|----------|
| **Gratuito** | R$ 0 | 5 | 2x | Básico |
| **Básico** | R$ 29 | 50 | 4x | Email |
| **Pro** | R$ 79 | 200 | 8x | API + Prioritário |
| **Empresarial** | R$ 199 | Ilimitado | 16x | 24/7 + Equipe |

## 🛠️ Configuração para Produção

### Variáveis de Ambiente

#### Backend (.env)
```bash
FLASK_ENV=production
SECRET_KEY=sua_chave_super_secreta
REPLICATE_API_TOKEN=r8_xxx
DATABASE_URL=postgresql://user:pass@host:5432/db
STRIPE_SECRET_KEY=sk_live_xxx
MERCADOPAGO_ACCESS_TOKEN=APP_USR_xxx
```

#### Frontend (.env.production)
```bash
VITE_API_URL=https://api.upscalepro.com
VITE_STRIPE_PUBLIC_KEY=pk_live_xxx
VITE_ENVIRONMENT=production
```

### Deploy Recomendado

#### Opção 1: Vercel + Railway
```bash
# Frontend no Vercel
npm install -g vercel
vercel --prod

# Backend no Railway
railway login
railway new upscale-pro-backend
railway add
railway deploy
```

#### Opção 2: Docker
```bash
# Build das imagens
docker build -t upscale-pro-frontend ./frontend
docker build -t upscale-pro-backend ./backend

# Deploy com docker-compose
docker-compose up -d
```

## 📚 Documentação

- 📖 **[Documentação Técnica](DOCUMENTACAO.md)** - Guia completo para desenvolvedores
- 👥 **[Manual do Usuário](MANUAL_USUARIO.md)** - Guia para usuários finais
- 🔧 **[API Reference](docs/api.md)** - Documentação das APIs
- 🚀 **[Deploy Guide](docs/deploy.md)** - Guia de deploy

## 🧪 Testes

### Executar Testes Backend
```bash
cd backend
python -m pytest tests/
```

### Executar Testes Frontend
```bash
cd frontend
npm run test
```

### Testes de Integração
```bash
npm run test:e2e
```

## 📈 Monitoramento

### Métricas Importantes
- Tempo de processamento por imagem
- Taxa de sucesso do processamento
- Conversões de planos pagos
- Uso de recursos (CPU, memória)

### Logs
```bash
# Visualizar logs em tempo real
tail -f backend/logs/app.log
```

## 🤝 Contribuindo

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo [LICENSE](LICENSE) para detalhes.

## 🆘 Suporte

- 📧 **Email**: suporte@upscalepro.com
- 💬 **Discord**: [Servidor da Comunidade](https://discord.gg/upscalepro)
- 🐛 **Issues**: [GitHub Issues](https://github.com/seu-usuario/upscale-pro/issues)

## 🎯 Roadmap

### v2.0 (Q3 2025)
- [ ] API Pública para desenvolvedores
- [ ] Processamento em lote
- [ ] Modelos customizados
- [ ] Colaboração em projetos

### v2.1 (Q4 2025)
- [ ] Aplicativo mobile
- [ ] Integração com cloud storage
- [ ] Processamento de vídeos
- [ ] Remoção de fundo com IA

## 🏆 Reconhecimentos

- **Real-ESRGAN** - Modelo de IA para super-resolução
- **Replicate** - Plataforma de ML
- **Tailwind CSS** - Framework CSS
- **shadcn/ui** - Componentes UI

---

<div align="center">

**Desenvolvido com ❤️ pela equipe UpScale Pro**

[Website](https://upscalepro.com) • [Documentação](DOCUMENTACAO.md) • [Suporte](mailto:suporte@upscalepro.com)

</div>

