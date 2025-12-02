# Guia do Servidor de Ingestão Universal (Webhook)

Este documento explica o funcionamento e como reutilizar o servidor `webhook_server.py` em qualquer projeto Python.

## 1. O Que Ele Faz? (Conceito "Esponja")

Este servidor foi projetado para ser uma **Camada de Ingestão Agnóstica**.
*   **Agnóstico:** Ele não sabe e não se importa com o formato dos dados (se é WhatsApp, Stripe, GitHub, etc).
*   **Esponja:** Ele absorve qualquer requisição HTTP POST, independente do conteúdo.
*   **Resiliente:** O objetivo principal é **não quebrar**. Ele captura erros de leitura de JSON, loga o problema, mas sempre retorna `200 OK` para a API que enviou a mensagem.

### Fluxo de Trabalho
1.  Escuta na porta `8000` no endpoint `/webhook`.
2.  Recebe o pacote (Payload).
3.  Tenta ler como JSON e imprime no terminal (Log).
4.  Se não for JSON, imprime o texto bruto.
5.  Responde `{"status": "received"}` imediatamente.

---

## 2. Como Reutilizar em OUTRO Projeto

Como este arquivo é modular (não depende de nada do resto do projeto), você pode levá-lo para onde quiser.

### Passo 1: Copie o Arquivo
Copie o arquivo `webhook_server.py` para a pasta do seu novo projeto.

### Passo 2: Instale o Básico
Você só precisa de duas bibliotecas:
*   **FastAPI:** Para criar a rota.
*   **Uvicorn:** Para rodar o servidor.

```bash
pip install fastapi uvicorn
```

### Passo 3: Execute
Rode o arquivo diretamente.

```bash
python3 webhook_server.py
```

### Passo 4: (Opcional) Personalização
Se você quiser conectar este servidor a uma lógica específica (ex: salvar no banco de dados ou chamar uma IA), edite a função `receive_payload`:

```python
@app.post("/webhook")
async def receive_payload(request: Request):
    payload = await request.json() 
    
    # --- SUA LÓGICA AQUI ---
    # ex: salvar_no_banco(payload)
    # ex: chamar_ia(payload)
    # -----------------------
    
    return {"status": "received"}
```

---

## 3. Testando Rapidamente (Curl)
Para testar se ele está funcionando no novo projeto:

```bash
curl -X POST "http://localhost:8000/webhook" \
     -H "Content-Type: application/json" \
     -d '{"projeto": "novo", "status": "sucesso"}'
```
