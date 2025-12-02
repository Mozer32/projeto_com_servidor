# 1. Importamos o tipo da nossa ficha (Estado)
from src.state import base_cliente_state
import time

def atendente(state: base_cliente_state) -> dict:

    msg_atual_cliente = state["msg_cliente"]
    telefone_cliente = state["telefone_cliente"]

    print(f"ATENDENTE TRABALHANDO")
    print(f"Aguarde...")
    time.sleep(2)
    print(f"""
    TELEFONE: {telefone_cliente}
    MENSAGEM DO CLIENTE: {msg_atual_cliente}
    """)

    # ---------- ATUALIZAR HISTORICO ----------
    atualizar_contexto = state.get("contexto_conversa", []) + [
        f"Cliente: {msg_atual_cliente}",
        f"Agente_AI: O Atendente fez o seu trabalho e atualizou o State"
    ]

    # --- C. RETORNAR ATUALIZAÇÃO ---
    # Retornamos apenas as chaves que queremos atualizar na ficha.
    return {
        "contexto_conversa": atualizar_contexto,
        "novo_cliente": True
    }
    


