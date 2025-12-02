import uvicorn
from fastapi import FastAPI, Request
from typing import Dict, Any

# Definição da Aplicação
# Docs URL desativado para manter o servidor leve e focado apenas em ingestão
app = FastAPI(
    title="Ingestion Layer (Agnostic Webhook)",
    docs_url=None, 
    redoc_url=None
)

@app.post("/webhook")
async def receive_payload(request: Request):
    """
    Ponto de entrada agnóstico (Esponja).
    
    Comportamento:
    1. Aceita a requisição HTTP bruta.
    2. Tenta decodificar o JSON para log.
    3. Retorna 200 OK incondicionalmente.
    """
    
    print("\n--- 📥 [INGESTION] Payload Recebido ---")
    
    try:
        # Tentamos extrair o JSON para visualização, mas sem schema estrito.
        payload = await request.json()
        print(payload)
        
    except Exception as e:
        # Se não for JSON (ex: form-data ou texto puro), logamos o erro de parse
        # mas NÃO falhamos a requisição. A ingestão deve confirmar o recebimento.
        print(f"⚠️ [AVISO] Payload não é um JSON válido ou está vazio: {e}")
        body_content = await request.body()
        print(f"Conteúdo Bruto: {body_content}")

    print("--- ✅ [INGESTION] Fim do Log ---\n")
    
    # Contrato simples de resposta
    return {"status": "received"}

if __name__ == "__main__":
    # Configuração de produção-ready para desenvolvimento local
    print("🚀 Servidor de Ingestão Iniciado na porta 8000...")
    uvicorn.run(
        "webhook_server:app", 
        host="0.0.0.0", 
        port=8000, 
        log_level="info", 
        reload=True
    )
