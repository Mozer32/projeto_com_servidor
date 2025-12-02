from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver # <--- Importar Memória
from src.state import base_cliente_state

# Importação dos Nossos Funcionários (Nós)
from src.nodes.node_base_field import node_base_field
from src.nodes.node_agente_AI import node_agente_ai
from src.nodes.node_responder_cliente import node_responder_cliente

# 1. CRIAR O GRAFO (A Planta da Fábrica)
workflow = StateGraph(base_cliente_state)

# 2. ADICIONAR OS NÓS (Estações de Trabalho)
workflow.add_node("base_field", node_base_field)        # Limpeza
workflow.add_node("agente_ai", node_agente_ai)          # Inteligência
workflow.add_node("responder_cliente", node_responder_cliente) # Envio

# 3. DEFINIR O FLUXO (As Setas)
# A. Começa no Base Field
workflow.set_entry_point("base_field")

# B. Do Base Field vai para o Agente AI
workflow.add_edge("base_field", "agente_ai")

# C. Do Agente AI vai para o Responder Cliente
workflow.add_edge("agente_ai", "responder_cliente")

# D. Do Responder Cliente acaba o processo
workflow.add_edge("responder_cliente", END)

# 4. COMPILAR (Ligar a Máquina com Memória)
checkpointer = MemorySaver() # <--- Criar o gravador
app = workflow.compile(checkpointer=checkpointer) # <--- Ligar o gravador

# --- ÁREA DE TESTE MANUAL (Opcional) ---
if __name__ == "__main__":
    print("Este arquivo é a definição do grafo.")
    print("Para rodar o servidor, use: python src/server/webhook_server.py")