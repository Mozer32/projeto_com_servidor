import os
from src.state import base_cliente_state
from dotenv import load_dotenv
from langchain_core.messages import HumanMessage, SystemMessage

# Carrega as senhas do arquivo seguro (.env_local)
load_dotenv(".env_local")

# --- CONFIGURAÇÃO DOS MODELOS (A Ferramenta de Trabalho) ---
# Aqui verificamos se as ferramentas (bibliotecas) estão instaladas
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
    FÁBRICA DE CÉREBROS (Auxiliar)
    Esta função vai no almoxarifado (.env) e pega o cérebro escolhido (Gemini ou GPT).
    """
    provider = os.getenv("LLM_PROVIDER", "gemini").lower()
    temp = 0.7 # Temperatura: Quanto mais alto, mais criativo (e maluco)

    if provider == "gemini":
        if not HAS_GOOGLE:
            print("❌ ERRO: Ferramenta Google não instalada.")
            return None
        
        api_key = os.getenv("GOOGLE_API_KEY")
        if not api_key:
            print("❌ ERRO: Chave do Google não encontrada.")
            return None
        # Retorna o modelo Gemini configurado
        return ChatGoogleGenerativeAI(model="gemini-2.5-flash-preview-09-2025", google_api_key=api_key, temperature=temp)

    elif provider == "openai":
        # (Mesma lógica para OpenAI...)
        if not HAS_OPENAI: return None
        api_key = os.getenv("OPENAI_API_KEY")
        return ChatOpenAI(model="gpt-4o-mini", api_key=api_key, temperature=temp)
    
    else:
        return None

def node_agente_ai(state: base_cliente_state) -> dict:
    """
    FUNCIONÁRIO: O ESPECIALISTA (IA)
    
    Função: Lê a mensagem do cliente, lê o histórico da conversa,
    consulta o manual (Prompt) e gera uma resposta inteligente.
    """
    print("--- 🧠 CÉREBRO: Pensando na resposta... ---")
    
    # 1. Ler o que está na prancheta
    mensagem_usuario = state.get("msg_cliente")
    # Pega o histórico (folhas grampeadas anteriores)
    historico = state.get("contexto_conversa", []) or [] 
    
    # 2. Pegar a ferramenta de trabalho (O Cérebro LLM)
    llm = _get_llm()
    if not llm:
        return {"msg_resposta": "Erro: Cérebro desligado."}

    # 3. Ler o Manual de Instruções (Prompt/Persona)
    try:
        base_path = os.path.dirname(__file__)
        prompt_path = os.path.join(base_path, "prompt.md") # Arquivo externo
        with open(prompt_path, "r", encoding="utf-8") as f:
            persona = f.read()
    except Exception:
        persona = "Você é um bot útil." # Plano B se não achar o arquivo

    # 4. Montar o contexto para a IA
    # Começa com a instrução do chefe (Persona)
    messages = [SystemMessage(content=persona)]
    
    # Adiciona as conversas passadas (Memória)
    for linha in historico:
        if linha.startswith("Cliente: "):
            messages.append(HumanMessage(content=linha.replace("Cliente: ", "")))
        elif linha.startswith("Bot: "):
            messages.append(SystemMessage(content=linha.replace("Bot: ", "")))

    # Adiciona a mensagem nova (A pergunta atual)
    messages.append(HumanMessage(content=mensagem_usuario))

    try:
        # 5. A Mágica (Chama a IA na nuvem)
        response = llm.invoke(messages)
        resposta_texto = response.content
        
        print(f"💡 Ideia: {resposta_texto}")
        
        # 6. Diário de Bordo (Log em arquivo txt)
        try:
            log_path = "src/nodes/node_historico.log"
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"--- NOVA INTERAÇÃO ---\n")
                f.write(f"Cliente: {mensagem_usuario}\n")
                f.write(f"Bot: {resposta_texto}\n")
                f.write("-" * 30 + "\n")
        except: pass

        # 7. Atualizar a Memória (Grampear essa conversa na prancheta)
        novo_historico = historico + [
            f"Cliente: {mensagem_usuario}",
            f"Bot: {resposta_texto}"
        ]
        
        # Retorna a resposta pronta e o histórico atualizado
        return {
            "msg_resposta": resposta_texto,
            "contexto_conversa": novo_historico
        }
        
    except Exception as e:
        print(f"❌ Cérebro falhou: {e}")
        return {"msg_resposta": "Erro interno."}
