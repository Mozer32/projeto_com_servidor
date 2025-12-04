import uvicorn
import sys
import os
from fastapi import FastAPI, Request
from typing import Dict, Any

# --- CONFIGURAÇÃO DE CAMINHOS ---
# Isso aqui é como desenhar um mapa para o Python achar a "Fábrica Principal" (main.py).
# Como este arquivo está numa sub-sala (src/server), precisamos ensinar o caminho de volta.
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

# Tenta chamar o Gerente da Fábrica (main.py)
try:
    from main import app as destino_final
except ImportError as e:
    print(f"⚠️ [PORTARIA] Não achei o Gerente (main.py): {e}")
    destino_final = None

# --- A PORTARIA (Servidor) ---
# Criamos a aplicação FastAPI. Ela é o porteiro que fica ouvindo a campainha (Porta 8000).
app = FastAPI(
    title="Portaria de Recebimento (Webhook)",
    docs_url=None, 
    redoc_url=None
)

@app.post("/webhook")
async def receive_payload(request: Request):
    """
    Esta função é o Porteiro Físico.
    Toda vez que o WhatsApp (Mega API) toca a campainha, esse código roda.
    """
    
    print("\n--- 📥 [PORTARIA] Chegou uma encomenda (Payload) ---")
    payload = {} # Prepara uma caixa vazia
    
    try:
        # O porteiro pega o pacote json que chegou
        payload = await request.json()
        print(payload) # Mostra o pacote no monitor
        
    except Exception as e:
        print(f"⚠️ [PORTARIA] O pacote chegou rasgado ou não é JSON: {e}")
        # Se der erro, mostramos o conteúdo bruto mesmo assim
        body_content = await request.body()
        print(f"Conteúdo Bruto: {body_content}")

    print("--- ✅ [PORTARIA] Pacote recebido e logado ---\n")
    
    # --- ENCAMINHAMENTO PARA A FÁBRICA ---
    # Agora o porteiro precisa levar esse pacote para a esteira de produção (LangGraph)
    if destino_final and payload:
        print("🚀 [PORTARIA] Jogando pacote na esteira do Robô...")
        try:
            # 1. Descobrir o ID do Cliente (Crachá)
            # Precisamos saber de quem é o pacote para buscar o histórico certo (Memória)
            thread_id = "sessao_anonima" 
            try:
                # Tenta ler o remetente na etiqueta do pacote
                key = payload.get("key", {})
                if "remoteJid" in key:
                    thread_id = key["remoteJid"]
            except:
                pass 

            # 2. Configurar a Sessão
            # Avisamos a fábrica: "Esse pacote é do cliente X"
            config = {"configurable": {"thread_id": thread_id}}
            print(f"🆔 Cliente Identificado: {thread_id}")

            # 3. DISPARO! (Invoke)
            # Aqui entregamos a ficha inicial. Note que só preenchemos 'dados_brutos'.
            # O resto da ficha está em branco, os funcionários de dentro vão preencher.
            destino_final.invoke({"dados_brutos": payload}, config=config)
            
            print("✅ [PORTARIA] Robô recebeu e processou.")
        except Exception as e_robo:
            print(f"❌ [PORTARIA] A fábrica devolveu o pacote (Erro): {e_robo}")
    else:
        print("⚠️ [PORTARIA] Fábrica fechada ou pacote vazio.")
    
    # Sempre respondemos "Recebido" para o entregador (Mega API) não ficar buzinando.
    return {"status": "received"}

if __name__ == "__main__":
    # Liga a luz da portaria e abre a porta 8000
    print("🚀 Portaria Aberta! Esperando entregas na porta 8000...")
    uvicorn.run(
        "webhook_server:app", 
        host="0.0.0.0", 
        port=8000, 
        log_level="info", 
        reload=True
    )