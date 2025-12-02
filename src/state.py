from typing import TypedDict, Annotated, List


class base_cliente_state(TypedDict):
    # Identificação
    telefone_cliente: str
    msg_cliente: str
    # Histórico da Conversa (Memória)
    contexto_conversa: List[str]   
    # Controle Interno
    novo_cliente: bool
    # Dados Brutos (Backup de tudo que veio da API)
    dados_brutos: dict
    
    





