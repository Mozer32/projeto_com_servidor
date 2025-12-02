import os
from src.state import base_cliente_state
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage

# Carrega o .env (Agora renomeado para .env_local por segurança)
load_dotenv(".env_local")

# --- IMPORTAÇÃO CONDICIONAL (Drivers) ---
try:
    from langchain_google_genai import ChatGoogleGenerativeAI
    HAS_GOOGLE = True
except ImportError:
    HAS_GOOGLE = False

try:
    from langchain_openai import ChatOpenAI
    HAS_OPENAI = True
except ImportError:
    HAS_OPENAI = False

def _get_llm():
    """
    FÁBRICA DE CÉREBROS 🏭
    """
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    temp = 0.7

    if provider == "gemini":
        if not HAS_GOOGLE:
            print("❌ ERRO: Biblioteca 'langchain-google-genai' não instalada.")
            return None
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ ERRO: GOOGLE_API_KEY não encontrada no .env")
            return None
        # Modelo específico solicitado pelo usuário (Contexto 2025)
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-09-2025", google_api_key=api_key, temperature=temp)

    elif provider == "openai":
        if not HAS_OPENAI:
            print("❌ ERRO: Biblioteca 'langchain-openai' não instalada.")
            return None
            
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            print("❌ ERRO: OPENAI_API_KEY não encontrada no .env")
            return None
        return ChatOpenAI(model="gpt-4o-mini", api_key=api_key, temperature=temp)
    
    else:
        print(f"❌ ERRO: Provider '{provider}' não suportado.")
        return None

def node_agente_ai(state: base_cliente_state) -> dict:
    """
    O Cérebro: Consulta a IA configurada e gera a resposta.
    """
    print("--- 🧠 NODE AGENTE AI: Pensando (conectando na nuvem)... ---")
    
    mensagem_usuario = state.get("msg_cliente")
    historico = state.get("contexto_conversa", []) or [] # Garante que é lista
    
    # 1. Obtém o cérebro
    llm = _get_llm()
    
    if not llm:
        return {"msg_resposta": "Desculpe, meu cérebro está desligado no momento."}

    # 2. Define a Personalidade (Lendo do arquivo prompt.md)
    try:
        # Caminho relativo ao arquivo atual (node_agente_AI.py)
        base_path = os.path.dirname(__file__)
        prompt_path = os.path.join(base_path, "prompt.md")
        
        with open(prompt_path, "r", encoding="utf-8") as f:
            persona = f.read()
    except Exception as e:
        print(f"⚠️ Erro ao ler prompt.md: {e}")
        persona = "Você é um assistente útil de pizzaria." # Fallback seguro

    # 3. Monta as mensagens (Sistema + Histórico + Atual)
    messages = [SystemMessage(content=persona)]
    
    # Adiciona histórico (se houver)
    # O histórico é uma lista de strings ["Human: oi", "AI: ola"]
    # Vamos converter para objetos de mensagem simples
    for linha in historico:
        if linha.startswith("Cliente: "):
            messages.append(HumanMessage(content=linha.replace("Cliente: ", "")))
        elif linha.startswith("Bot: "):
            # O Gemini às vezes prefere receber como 'model' ou 'assistant'
            # No LangChain, SystemMessage ou AIMessage funcionam
            messages.append(SystemMessage(content=linha.replace("Bot: ", "")))

    # Adiciona a mensagem atual
    messages.append(HumanMessage(content=mensagem_usuario))

    try:
        # 4. Chama a API (Invoca a IA)
        response = llm.invoke(messages)
        resposta_texto = response.content
        
        print(f"💡 IA Respondeu: {resposta_texto}")
        
        # --- LOGGING EM ARQUIVO (Diário de Bordo) ---
        try:
            log_path = "src/nodes/node_historico.log"
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"--- NOVA INTERAÇÃO ---\n")
                f.write(f"Cliente: {mensagem_usuario}\n")
                f.write(f"Bot: {resposta_texto}\n")
                f.write("-" * 30 + "\n")
            print(f"📝 Conversa salva em: {log_path}")
        except Exception as e_log:
            print(f"⚠️ Erro ao salvar log em arquivo: {e_log}")

        # 5. Atualiza o Histórico (Adiciona a nova troca)
        novo_historico = historico + [
            f"Cliente: {mensagem_usuario}",
            f"Bot: {resposta_texto}"
        ]
        
        return {
            "msg_resposta": resposta_texto,
            "contexto_conversa": novo_historico
        }
        
    except Exception as e:
        print(f"❌ Erro na IA: {e}")
        return {"msg_resposta": "Desculpe, tive um erro interno ao processar seu pedido."}