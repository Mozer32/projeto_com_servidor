from typing import TypedDict, List

# --- A FICHA DE PEDIDO (State) ---
# Imagine que isso é uma prancheta com um formulário em branco.
# Cada funcionário (Nó) vai receber essa prancheta, ler o que tem nela,
# escrever novas informações e passar para o próximo.

class base_cliente_state(TypedDict):
    # [Identificação]
    # Aqui o funcionário da Triagem vai anotar quem é o cliente
    telefone_cliente: str
    
    # [Entrada]
    # O que o cliente disse? (Ex: "Quero uma pizza")
    msg_cliente: str
    
    # [Memória / Histórico]
    # É como um grampo na prancheta com as folhas das conversas passadas.
    # O Robô lê isso para saber o que já foi conversado antes.
    contexto_conversa: List[str]   
    
    # [Controle]
    # Um check-box para marcar se é a primeira vez do cliente.
    novo_cliente: bool
    
    # [Saída / Resposta]
    # Aqui o "Cérebro" (IA) escreve o que deve ser respondido.
    # O "Carteiro" (Responder) vai ler daqui para enviar.
    msg_resposta: str
    
    # [Arquivo Morto / Backup]
    # Aqui guardamos o pacote fechado que chegou do correio (Mega API).
    # Se precisarmos de algo que não anotamos acima, podemos procurar aqui.
    dados_brutos: dict