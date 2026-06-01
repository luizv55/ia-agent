from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import SystemMessage
from tools import buscar_no_banco
from dotenv import load_dotenv
import os

load_dotenv()

# Promt base

SCHEMA = """
Você é um assistente de análise de vendas. Você tem acesso a um banco de dados SQLite com as seguintes tabelas:

clientes(id, nome, email, cidade, estado, genero, data_nascimento, data_cadastro)
vendedores(id, nome, email_corporativo, regiao, meta_vendas)
produtos(id, nome, categoria, preco)
pedidos(id, cliente_id, vendedor_id, data, status)
itens_pedido(id, pedido_id, produto_id, quantidade)
pagamentos(id, pedido_id, metodo, status, data_pagamento)

Quando o usuário fizer uma pergunta vaga ou sem recorte temporal, peça esclarecimentos.
Quando a pergunta for clara, gere o SQL correto e use a tool buscar_no_banco para executar.
"""

# Conexão da api do LLM do gemini
llm = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-lite",
    google_api_key=os.getenv("GOOGLE_API_KEY")
)

# Busca dentro do banco
llm_com_tools = llm.bind_tools([buscar_no_banco])

def node_llm(state):
    mensagens = [SystemMessage(content=SCHEMA)] + state["messages"]
    resposta = llm_com_tools.invoke(mensagens)
    return {"messages": [resposta]}