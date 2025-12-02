from langgraph.graph import StateGraph, END
from src.state import base_cliente_state
from src.nodes.node_atendente import atendente

# 1. CRIAR O GRAFO (A Planta da Fábrica)
# Dizemos: "Essa fábrica trabalha com fichas do tipo base_cliente_state"
workflow = StateGraph(base_cliente_state)

# 2. ADICIONAR OS NÓS (Os Funcionários)
# "Contratamos" o atendente e damos o nome de 'atendente' para a estação dele.
workflow.add_node("atendente", atendente)

# 3. DEFINIR O PONTO DE PARTIDA
# "Quando a ficha chegar, mande direto para o atendente."
workflow.set_entry_point("atendente")

# 4. DEFINIR O FIM
# "Depois que o atendente terminar, o processo acaba (END)."
workflow.add_edge("atendente", END)

# 5. COMPILAR (Ligar a Máquina)
app = workflow.compile()


