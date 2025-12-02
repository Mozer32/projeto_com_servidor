import uvicorn
import sys
import os
from fastapi import FastAPI, Request
from typing import Dict, Any

# --- SETUP DE IMPORTAÇÃO ---
# Adiciona a raiz do projeto (projeto_v1) ao path para conseguir importar o main.py
# Isso garante que funcione mesmo rodando de dentro da pasta server
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

try:
    from main import app as destino_final
except ImportError as e:
    print(f"⚠️ [SERVER] Erro ao importar main.py: {e}")
    destino_final = None

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
    payload = {} # Inicializa vazio para segurança
    
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
    
    # --- INTEGRAÇÃO: Disparo para o Robô (LangGraph) ---
    if destino_final and payload:
        print("🚀 [SERVER] Encaminhando pacote para o Robô...")
        try:
            # 1. Tenta descobrir QUEM é o cliente para manter a memória (Thread ID)
            # O padrão do Whats é payload['key']['remoteJid']
            thread_id = "sessao_anonima" # Fallback
            try:
                key = payload.get("key", {})
                if "remoteJid" in key:
                    thread_id = key["remoteJid"]
            except:
                pass # Se falhar, usa anonimo

            # 2. Configuração de Execução (Com Memória)
            config = {"configurable": {"thread_id": thread_id}}
            
            print(f"🆔 Thread ID: {thread_id}")

            # 3. Chama o Robô passando a config
            destino_final.invoke({"dados_brutos": payload}, config=config)
            
            print("✅ [SERVER] Robô recebeu o pacote.")
        except Exception as e_robo:
            print(f"❌ [SERVER] Erro ao chamar o Robô: {e_robo}")
    else:
        print("⚠️ [SERVER] Pulei o envio (Robô desconectado ou Payload vazio).")
    
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
