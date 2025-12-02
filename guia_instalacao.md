# Guia de Instalação, Arquitetura e Execução

Este guia documenta a configuração do ambiente, a arquitetura do servidor de webhook e como expor o projeto para a internet.

## 1. Configuração do Ambiente

### Preparação da Pasta
```bash
cd ~/Desktop/projeto_v1
python3 -m venv venv
source venv/bin/activate  # Mac/Linux
# No Windows: venv\Scripts\activate
```

### Instalação de Dependências
```bash
pip install -r requirements.txt
```

---

## 2. Arquitetura do Servidor (Webhook)

O servidor segue o padrão de **Ingestion Layer** (Camada de Ingestão). Ele é agnóstico e desacoplado do resto da lógica de negócios.

*   **Arquivo:** `src/server/webhook_server.py`
*   **Função:** "Esponja". Recebe qualquer JSON, loga no terminal e retorna `200 OK`.
*   **Tecnologia:** FastAPI + Uvicorn.

### Como Rodar o Servidor
Estando na raiz do projeto (`projeto_v1`):

```bash
python3 src/server/webhook_server.py
```
*O servidor iniciará na porta 8000 (`http://0.0.0.0:8000`).*

---

## 3. Expondo para a Internet (Ngrok)

Para que a Mega API (ou qualquer webhook externo) acesse seu servidor local, usamos o **Ngrok**.

### Passo A: Autenticação (Crucial)
Para evitar telas de bloqueio ("Browser Warning"), é necessário autenticar com seu token gratuito.

```bash
# Se instalado via sistema (Homebrew/Global):
ngrok config add-authtoken SEU_TOKEN_AQUI

# Se estiver usando o executável baixado na pasta:
./ngrok config add-authtoken SEU_TOKEN_AQUI
```

### Passo B: Abrir o Túnel
Em um novo terminal (mantenha o servidor Python rodando no outro):

```bash
ngrok http 8000
```

Copie o link HTTPS gerado (ex: `https://xxxx.ngrok-free.app`).

---

## 4. Configurando a API Externa (Mega API)

1.  Acesse o painel da Mega API.
2.  No campo **Webhook**, cole o link do Ngrok **COM O ENDPOINT**:
    
    👉 `https://seu-link-ngrok.ngrok-free.app/webhook`

3.  Certifique-se de marcar os gatilhos de mensagem (ex: `on_message`).
4.  Salve.

## 5. Testando o Fluxo Completo

1.  Envie uma mensagem para o WhatsApp conectado.
2.  Observe o terminal do **Python**: O JSON bruto deve aparecer.
3.  Observe o terminal do **Ngrok**: Deve registrar uma requisição `200 OK`.
