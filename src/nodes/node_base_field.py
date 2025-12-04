from src.state import base_cliente_state

def node_base_field(state: base_cliente_state) -> dict:
    """
    FUNCIONÁRIO: TRIAGEM (Base Field)
    
    Função: Recebe a caixa bruta, abre, joga fora o papelão e 
    preenche a ficha com os dados importantes (Telefone e Mensagem).
    """
    print("--- 🧹 TRIAGEM: Abrindo o pacote e organizando... ---")
    
    # 1. Pegar a caixa bruta na prancheta (state)
    # O porteiro colocou o pacote aqui em 'dados_brutos'
    dados_brutos = state.get("dados_brutos", {})
    
    # 2. Mineração de Dados (Caçando as informações no JSON)
    
    # --- A. PROCURANDO O TELEFONE ---
    # Geralmente está dentro de uma sub-caixa chamada 'key' -> 'remoteJid'
    key_data = dados_brutos.get("key", {})
    telefone_sujo = key_data.get("remoteJid", "00000000")
    
    # Limpeza: Tira o "@s.whatsapp.net" para ficar só o número bonito
    telefone_limpo = telefone_sujo.replace("@s.whatsapp.net", "").replace("@c.us", "")
    
    # --- B. PROCURANDO A MENSAGEM ---
    # O WhatsApp esconde a mensagem em lugares diferentes dependendo do tipo
    msg_obj = dados_brutos.get("message", {})
    
    # Tentativa 1: É texto simples?
    mensagem_texto = msg_obj.get("conversation")
    
    # Tentativa 2: É resposta ou texto estendido?
    if not mensagem_texto:
        extended = msg_obj.get("extendedTextMessage", {})
        mensagem_texto = extended.get("text", "Mensagem não reconhecida (audio/imagem)")
   
    # --- C. PROCURANDO O NOME ---
    nome = dados_brutos.get("pushName", "Cliente")
    
    print(f"✅ Triagem Concluída: {nome} | Tel: {telefone_limpo} | Msg: {mensagem_texto}")
   
    # 3. Atualizar a Ficha (Return)
    # O funcionário escreve na prancheta e passa adiante.
    # Agora os campos 'telefone_cliente' e 'msg_cliente' têm valor!
    return {
        "telefone_cliente": telefone_limpo,
        "msg_cliente": mensagem_texto,
    }
