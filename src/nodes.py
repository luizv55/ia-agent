from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage
from .tools import buscar_no_banco
import re

SCHEMA = """
Você é um assistente de análise de vendas com acesso a um banco SQLite.

Tabelas e colunas EXATAS disponíveis:
- clientes(id, nome, email, cidade, estado, genero, data_nascimento, data_cadastro)
- vendedores(id, nome, email_corporativo, regiao, meta_vendas)
- produtos(id, nome, categoria, preco)
- pedidos(id, cliente_id, vendedor_id, data, status)
- itens_pedido(id, pedido_id, produto_id, quantidade)
- pagamentos(id, pedido_id, metodo, status, data_pagamento)

REGRAS IMPORTANTES:
- Use APENAS as colunas listadas acima, nunca invente colunas
- As datas estão no formato DD/MM/YYYY
- Para filtrar abril de 2024 use: pedidos.data LIKE '__/04/2024'
- Para calcular receita use: itens_pedido.quantidade * produtos.preco
- Sempre faça JOIN explícito quando usar colunas de outra tabela
- Se a pergunta for vaga, peça esclarecimentos
- Responda APENAS com o SQL válido para SQLite, sem explicação, sem markdown, sem ```

EXEMPLO:
Pergunta: Qual vendedor teve mais pedidos em abril de 2024?
SQL: SELECT v.nome, COUNT(p.id) as total FROM pedidos p JOIN vendedores v ON p.vendedor_id = v.id WHERE p.data LIKE '__/04/2024' GROUP BY v.id ORDER BY total DESC LIMIT 1

Pergunta: Qual vendedor fez mais pedidos em 2024?
SQL: SELECT v.nome, COUNT(p.id) as total FROM pedidos p JOIN vendedores v ON p.vendedor_id = v.id WHERE p.data LIKE '%/2024' GROUP BY v.id ORDER BY total DESC LIMIT 1
"""

llm = ChatOllama(model="qwen2.5-coder:7b", temperature=0, num_predict=200)
llm_com_tools = llm.bind_tools([buscar_no_banco])

_SYSTEM_MESSAGE = SystemMessage(content=SCHEMA)


def node_llm(state):
    mensagens = [_SYSTEM_MESSAGE] + state["messages"]
    resposta = llm_com_tools.invoke(mensagens)
    return {"messages": [resposta]}