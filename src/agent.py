from langgraph.graph import StateGraph, END         # monta o grafo e termina o fluxo
from langgraph.prebuilt import ToolNode             # Executa as tools automaticamente
from .schema import State
from .nodes import node_llm
from .tools import buscar_no_banco

"""
    Schema de decisão do banco
"""



def decidir_proximo_passo(state):
    ultima_mensagem = state["messages"][-1]               # Pega a última mensagem do estado
    if hasattr(ultima_mensagem, "tool_calls") and ultima_mensagem.tool_calls:    # Verifica se a LLM pediu para chamar a tool
        return "tools"           # Se sim vai para o nó de tools
    return END

# Cria o grafo
builder = StateGraph(State)

# Adiciona os nós
builder.add_node("llm", node_llm)
builder.add_node("tools", ToolNode([buscar_no_banco]))

# Define a entrada
builder.set_entry_point("llm")

builder.add_conditional_edges("llm", decidir_proximo_passo)
builder.add_edge("tools", "llm")


# Compilando
graph = builder.compile()