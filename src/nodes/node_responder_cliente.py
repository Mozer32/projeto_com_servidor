import os
import requests
from src.state import base_cliente_state
from dotenv import load_dotenv

# Carrega o arquivo de endereços (.env_local)
load_dotenv(".env_local")

def node_responder_cliente(state: base_cliente_state) -> dict:
    """
    FUNCIONÁRIO: CARTEIRO (Mega API Sender)
    
    Função: Pega a carta escrita pelo Cérebro (msg_resposta)
    e entrega para o motoboy da Mega API levar até o cliente.
    """
    print("--- 📮 EXPEDIÇÃO: Preparando envio... ---")
    
    # 1. Pegar os dados na prancheta
    telefone = state.get("telefone_cliente")
    texto = state.get("msg_resposta")
    
    # Verificação básica (O endereço existe? A carta tem texto?)
    if not telefone or not texto:
        print("❌ Erro: Endereço ou Mensagem faltando.")
        return {}

    # 2. Pegar as chaves do caminhão (Credenciais da API)
    host = os.getenv("MEGA_API_HOST", "https://api.megaapi.com.br")
    instance_key = os.getenv("MEGA_INSTANCE_KEY")
    token = os.getenv("MEGA_TOKEN")

    if not instance_key or not token:
        print("❌ Erro: Chaves da Mega API não configuradas.")
        return {}

    # Monta o endereço de entrega (URL)
    url = f"{host}/rest/sendMessage/{instance_key}/text"
    
    # 3. Empacotar a mensagem (Payload JSON)
    # Precisamos seguir a regra da transportadora (Documentação Mega API)
    payload = {
        "messageData": {
            "to": telefone, 
            "text": texto
        }
    }
    
    # Regra da transportadora: O destino tem que ter @s.whatsapp.net
    if "@" not in str(payload["messageData"]["to"]):
        payload["messageData"]["to"] = f"{telefone}@s.whatsapp.net"

    # Selo de Autenticação (Header)
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {token}"
    }

    # 4. Entregar para o motoboy (Request POST)
    try:
        response = requests.post(url, json=payload, headers=headers)
        
        if response.status_code == 200:
            print(f"✅ Entrega realizada! Protocolo: {response.json()}")
        else:
            print(f"⚠️ Entrega falhou: {response.status_code} - {response.text}")
            
    except Exception as e:
        print(f"❌ Caminhão quebrou (Erro de Conexão): {e}")

    # Fim do trabalho. Não precisamos atualizar a ficha.
    return {}