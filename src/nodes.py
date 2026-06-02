from langchain_ollama import ChatOllama
from langchain_core.messages import SystemMessage, AIMessage
from .database import get_connection
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

llm = ChatOllama(model="mistral:7b")


def corrigir_formato_data(sql: str) -> str:
    sql = re.sub(r"LIKE '(\d{4})-(\d{2})-%'", lambda m: f"LIKE '__{m.group(2)}/{m.group(1)}'", sql)
    sql = re.sub(r"LIKE '__/(\d{4})'", r"LIKE '%/\1'", sql)
    return sql

def executar_sql(sql: str) -> str:
    sql = corrigir_formato_data(sql)
    print("SQL CORRIGIDO:", sql)
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    conn.close()
    if not resultado:
        return "Nenhum resultado encontrado."
    return str(resultado)

def node_llm(state):
    mensagens = [SystemMessage(content=SCHEMA)] + state["messages"]
    resposta = llm.invoke(mensagens)
    
    sql = resposta.content.strip()
    sql = re.sub(r"```sql\s*|\s*```", "", sql).strip()
    sql = re.sub(r"^SQL:\s*", "", sql).strip()
    sql = sql.split("\n")[0].strip()
    sql = sql.strip('"')
    print("SQL GERADO:", repr(sql))
    
    if sql.upper().startswith("SELECT"):
        resultado = executar_sql(sql)
        print("RESULTADO SQL:", resultado)
        if resultado == "Nenhum resultado encontrado.":
            return {"messages": [AIMessage(content=resultado)]}
        
        linhas = "\n".join([", ".join(str(v) for v in linha) for linha in eval(resultado)])
        return {"messages": [AIMessage(content=linhas)]}
        