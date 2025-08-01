# 📊 Sistema de Vendas - Hot-Dog

Este é um projeto de Dashboard de Vendas construído com **Flask** no backend e **Node.js + Vite** para compilar os assets (JavaScript e CSS). O frontend utiliza **Bootstrap 5**, **DataTables**, **jQuery**, **SweetAlert2** e **Choices.js** para uma interface rica e interativa.

---

## 🔧 Tecnologias Utilizadas

### Backend
- Python 3
- Flask
- Jinja2

### Frontend
- Node.js + Vite (para build de JS e CSS)
- Bootstrap 5 (via npm)
- DataTables
- jQuery
- SweetAlert2
- Choices.js

---

## 📁 Estrutura do Projeto

cachorro_quente_social/
```bash
│
├── app/
│ ├── routes/
│ │ └── vendas.py # Rotas do Flask
│ ├── static/
│ │ ├── dist/ # Arquivos compilados pelo Vite (JS e CSS finais)
│ │ ├── images/ # Imagens usadas no frontend
│ └── templates/
│ ├── layouts/
│ │ └── base.html # Layout base do HTML
│ └── dashboard.html # Página principal do dashboard
│
├── frontend/
│ ├── js/
│ │ ├── pages/
│ │ │ └── dashboard.js # Scripts específicos da dashboard
│ │ └── components/
│ │ └── sweet-geral.js # Scripts utilitários
│ ├── scss/
│ │ └── style.scss # SCSS do projeto
│ └── index.js # Entrada para Vite
│
├── relatorio.xlsx # Relatório exemplo enviado por e-mail
├── app.py # Arquivo principal do Flask
├── package.json # Configurações do projeto Node.js
├── vite.config.js # Configurações do Vite
└── requirements.txt # Dependências Python
```

## ▶️ Como rodar o projeto

### 1. Backend (Flask)

```bash
# Crie o ambiente virtual
python -m venv venv
source venv/bin/activate  # ou venv\Scripts\activate no Windows

# Instale as dependências
pip install -r requirements.txt

# Rode o servidor
python app.py
```
### 2. Frontend (Vite + Node.js)

```bash
# Instale as dependências do Node
cd frontend
npm install

# Durante o desenvolvimento:
npm run dev

# Para build de produção:
npm run build

```
Os arquivos gerados por vite vão para app/static/dist/ e são usados no Flask sem depender de CDN.

📦 Bibliotecas Usadas (via NPM)
bootstrap

datatables.net-bs5

jquery

sweetalert2

choices.js



Você pode instalar todas com:

```bash
npm install bootstrap datatables.net-bs5 jquery sweetalert2 choices.js
```
📤 Envio de Relatórios por E-mail

O sistema permite enviar relatórios Excel para múltiplos e-mails através de um modal. Os e-mails são inseridos no campo e separados ao pressionar Enter. O envio é feito via fetch() para a rota Flask /api/send_excel, que envia os anexos via SMTP.

✅ Recursos Prontos
Dashboard com contadores de vendas pagas/pendentes/totais

Filtros por data, status, produto e vendedor

Modal para registrar e editar vendas

Tabela com DataTables interativo

Envio de Excel por e-mail via SMTP

📌 TODO / Melhorias Futuras
Autenticação e login

Geração dinâmica de Excel com filtros aplicados

Exportação CSV/PDF

Dashboard com gráficos (ex: Chart.js)

🧑‍💻 Desenvolvido por
Seu Nome — [@natan33](https://github.com/natan33)



