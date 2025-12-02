import os
import requests
from src.state import base_cliente_state
from dotenv import load_dotenv

# Carrega variáveis do .env_local
load_dotenv(".env_local")

def node_responder_cliente(state: base_cliente_state) -> dict:
    """
    O Carteiro: Pega a resposta pronta e envia via Mega API.
    """
    print("--- 📮 NODE RESPONDER: Enviando mensagem... ---")
    
    # 1. Dados para envio
    telefone = state.get("telefone_cliente")
    texto = state.get("msg_resposta")
    
    if not telefone or not texto:
        print("❌ Erro: Telefone ou Texto vazios. Não posso enviar.")
        return {}

    # 2. Configurações da Mega API (Do .env)
    # Formato da URL: https://host/rest/sendMessage/{instance_key}/text
    host = os.getenv("MEGA_API_HOST", "https://api.megaapi.com.br") # Coloque o seu host real no .env
    instance_key = os.getenv("MEGA_INSTANCE_KEY")
    token = os.getenv("MEGA_TOKEN")

    if not instance_key or not token:
        print("❌ Erro: Credenciais da Mega API não encontradas no .env")
        return {}

    url = f"{host}/rest/sendMessage/{instance_key}/text"
    
    # 3. Montagem do Payload (Conforme Documentação OpenAPI)
    payload = {
        "messageData": {
            "to": telefone, # Já deve estar limpo ou com @s.whatsapp.net? A doc diz: "55..@s.whatsapp.net"
            "text": texto
        }
    }
    
    # Ajuste fino: A doc diz que precisa do sufixo @s.whatsapp.net
    if "@" not in str(payload["messageData"]["to"]):
        payload["messageData"]["to"] = f"{telefone}@s.whatsapp.net"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # 4. Disparo
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ Mensagem enviada! Status: {response.json()}")
        else:
            print(f"⚠️ Erro no envio: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Erro de Conexão: {e}")

    # Não precisamos retornar nada para o state, o trabalho acabou.
    return {}
