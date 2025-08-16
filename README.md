# Estação Fácil - API (Backend)  

![Python](https://img.shields.io/badge/Python-3670A0?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Oracle](https://img.shields.io/badge/Oracle-F80000?style=for-the-badge&logo=oracle&logoColor=white)
![IBM Watson](https://img.shields.io/badge/IBM%20Watson-052FAD?style=for-the-badge&logo=ibmwatson&logoColor=white)
![API REST](https://img.shields.io/badge/API-REST-blue?style=for-the-badge)
![FIAP](https://img.shields.io/badge/FIAP-ED145B?style=for-the-badge)
![CCR](https://img.shields.io/badge/CCR-FFD700?style=for-the-badge)

---

## 💡 Sobre o Projeto  

O **Estação Fácil** é uma plataforma que permite que passageiros do metrô de São Paulo interajam com a inteligência artificial **Cecilia** para tirar dúvidas e obter informações sobre linhas, estações e rotas.  

Este repositório contém a **API RESTful** consumida pelo frontend. Desenvolvida com **Python (FastAPI)**, integra-se ao **IBM Watson** para processamento de linguagem natural e utiliza **OracleDB** como banco de dados.  

Projeto desenvolvido durante o curso de **Análise e Desenvolvimento de Sistemas (ADS)** da **FIAP**, em parceria com a **CCR**.  

---

## 🛠️ Tecnologias Utilizadas  

- **Python 3.10+**  
- **FastAPI** (framework web)  
- **OracleDB** (banco de dados relacional)  
- **JWT** (autenticação)  
- **IBM Watson Assistant** (chatbot)  

---

## 📌 Endpoints Principais  

### **Autenticação**  
- `POST /auth/token` → Login e obtenção de token JWT  

### **Usuários**  
- `POST /users/` → Criar usuário  
- `GET /users/me` → Obter dados do usuário autenticado  
- `PUT /users/{user_id}` → Atualizar usuário  
- `PUT /users/{user_id}/password` → Alterar senha do usuário  

### **Chats**  
- `GET /chats/` → Listar chats do usuário  
- `POST /chats/` → Criar novo chat  
- `GET /chats/{chat_code}` → Obter detalhes de um chat  
- `PUT /chats/{chat_code}` → Atualizar chat  
- `DELETE /chats/{chat_code}` → Excluir chat  

### **Mensagens**  
- `POST /messages/` → Enviar mensagem (stateless)  
- `POST /messages/{chat_code}` → Enviar mensagem vinculada a um chat (logada)  

### **Rotas de Metrô**  
- `GET /subway-route/` → Calcular melhor rota entre estações  

---

## 🔐 Autenticação  

A API utiliza **JWT (JSON Web Token)** para proteger endpoints sensíveis.  

**Fluxo básico:**  
1. Crie um usuário (`POST /users/`).  
2. Faça login (`POST /auth/token`) e obtenha o token JWT.  
3. Envie o token no header `Authorization: Bearer <token>` para acessar endpoints protegidos.  

---

## 🚀 Como Executar Localmente  

### **Pré-requisitos**  
- Python 3.10+ instalado  
- Banco Oracle configurado  
- Chaves da API do IBM Watson  

### **Configuração do `.env`**  
```properties  
DB_URL=sua_db_url  
DB_USER=seu_usuario  
DB_PASSWORD=sua_senha  

SECRET_KEY=sua_chave_secreta  
ALGORITHM=HS256  
ACCESS_TOKEN_EXPIRE_MINUTES=60  

WATSON_API_KEY=sua_chave_watson  
WATSON_URL=sua_url_watson  
WATSON_ASSISTANT_ID=seu_assistente_id  
```  

### **Instalação**  
```bash  
git clone https://github.com/PauloSergioFB/estacao-facil-api.git  
cd estacao-facil-api  

python3 -m venv .venv  
source .venv/bin/activate  

pip install -r requirements.txt  
```  

### **Execução**  
```bash  
fastapi dev app.py
```  

Documentação Swagger: [http://localhost:8000/docs](http://localhost:8000/docs)  

---

## 📐 Especificações Técnicas  

- **Arquitetura**: FastAPI + OracleDB + integração IBM Watson  
- **Algoritmo de Rotas**: Implementação do Dijkstra para cálculo do menor caminho  
- **Segurança**: Autenticação com JWT e hash de senhas
- **Chatbot**: Integração completa com IBM Watson Assistant  

---

## 👥 Contribuidores  

- [**PauloSergioFB**](https://github.com/PauloSergioFB) — Design do frontend, modelagem do banco de dados e desenvolvimento do backend  
- [**Angelo Recke Ricieri**](https://github.com/AngeloCCR) — Desenvolvimento do fluxo de chatbot  

---

## 📜 Licença  

Este projeto está licenciado sob a [Creative Commons Attribution-NonCommercial 4.0 International](https://creativecommons.org/licenses/by-nc/4.0/).  
Uso livre para fins de estudo e referência, vedado uso comercial.  
