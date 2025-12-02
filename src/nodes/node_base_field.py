from src.state import base_cliente_state

def node_base_field(state: base_cliente_state) -> dict:
    """
    Recebe o JSON bruto da API e extrai as informações essenciais.
    Atua como um filtro de entrada.
    """
    print("--- 🧹 NODE BASE FIELD: Limpando e Organizando dados... ---")
    
    # 1. Pegar a caixa de entrada bruta (o JSON que o servidor jogou aqui)
    dados_brutos = state.get("dados_brutos", {})
    
    # 2. Extração Segura (Use .get para não quebrar se o campo faltar)
    # Tente navegar no JSON da Mega API aqui:
    
    # Exemplo de como navegar: dados_brutos.get("chave_principal", {}).get("sub_chave")
    
    # TELEFONE (remoteJid)
    # Dica: Geralmente vem sujo como "55119999@s.whatsapp.net"
    key_data = dados_brutos.get("key", {})
    telefone_sujo = key_data.get("remoteJid", "00000000")
    telefone_limpo = telefone_sujo.replace("@s.whatsapp.net", "").replace("@c.us", "")
    
    # MENSAGEM
    # Dica: Pode vir em 'conversation' ou 'extendedTextMessage' -> 'text'
    msg_obj = dados_brutos.get("message", {})
    mensagem_texto = msg_obj.get("conversation")
    
    # Se não achou em 'conversation', tenta no 'extendedTextMessage'
    if not mensagem_texto:
        extended = msg_obj.get("extendedTextMessage", {})
        mensagem_texto = extended.get("text", "Mensagem não reconhecida (audio/imagem)")
   
    # 3. Nome do Cliente (pushName)
    nome = dados_brutos.get("pushName", "Cliente")
    
    print(f"✅ Extraído: {nome} | Tel: {telefone_limpo} | Msg: {mensagem_texto}")
   
    # 4. Retorno (Atualiza a ficha oficial do LangGraph)
    return {
        "telefone_cliente": telefone_limpo,
        "msg_cliente": mensagem_texto,
    }