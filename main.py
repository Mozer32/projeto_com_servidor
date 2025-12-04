from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver # Nosso "Arquivo de Memória"
from src.state import base_cliente_state

# --- CONTRATAÇÃO DOS FUNCIONÁRIOS (Importar os nós) ---
from src.nodes.node_base_field import node_base_field       # base_field
from src.nodes.node_agente_AI import node_agente_ai         # Cérebro
from src.nodes.node_responder_cliente import node_responder_cliente # Carteiro

# 1. DESENHAR A PLANTA (O Grafo)
# Dizemos: "Nossa fábrica usa a ficha do tipo 'base_cliente_state'"
workflow = StateGraph(base_cliente_state)

# 2. POSICIONAR AS ESTAÇÕES (Nós)
# Aqui damos nomes para as salas dos funcionários
workflow.add_node("base_field", node_base_field)
workflow.add_node("agente_ai", node_agente_ai)
workflow.add_node("responder_cliente", node_responder_cliente)

# 3. DEFINIR A ESTEIRA (As Setas / Fluxo)
# --- A. Entrada ---
# Todo pedido novo começa na base_field
workflow.set_entry_point("base_field")

# --- B. Fluxo ---
# Da base_field -> vai para o agente_ai
workflow.add_edge("base_field", "agente_ai")

# Do agente_ai -> vai para a responder_cliente
workflow.add_edge("agente_ai", "responder_cliente")

# --- C. Saída ---
# Da responder_cliente -> Acaba o serviço (END)
workflow.add_edge("responder_cliente", END)

# 4. LIGAR A MÁQUINA (Compile)
# Ativamos o 'checkpointer' para que a fábrica tenha memória.
# Sem isso, toda ficha seria tratada como se fosse a primeira vez.
gravador_memoria = MemorySaver()
app = workflow.compile(checkpointer=gravador_memoria)

# --- PONTO DE TESTE MANUAL ---
# Se rodarmos esse arquivo direto, ele só avisa que está pronto.
if __name__ == "__main__":
    print("🏭 Fábrica Montada e Pronta!")
    print("Para começar a trabalhar, inicie a portaria: python src/server/webhook_server.py")
