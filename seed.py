import pandas as pd
from database import get_connection

# Ingerindo os dados cliente
def inserir_clientes():
    conn = get_connection()
    df = pd.read_excel("dados/clientes.xlsx")
    df.to_sql("clientes", conn, if_exists="append", index=False)
    conn.close()
    print(f"{len(df)} clientes inseridos!")

# Ingerindo os dados de vendedores
def inserir_vendedores():
    conn = get_connection()
    df = pd.read_excel("dados/vendedores.xlsx")
    df.to_sql("vendedores", conn, if_exists="append", index=False)
    conn.close()
    print(f"{len(df)} vendedores inseridos!")

# Ingerindo os dados de produtos
def inserir_produtos():
    conn = get_connection()
    df = pd.read_excel("dados/produtos.xlsx")
    df.to_sql("produtos", conn, if_exists="append", index=False)
    conn.close()
    print(f"{len(df)} produtos inseridos!")

# Ingerindo os dados de pedidos
def inserir_pedidos():
    conn = get_connection()
    df = pd.read_excel("dados/pedidos.xlsx")
    df.to_sql("pedidos", conn, if_exists="append", index=False)
    conn.close()
    print(f"{len(df)} pedidos inseridos!")

# Ingerindo os dados de itens_pedidos
def inserir_itens_pedido():
    conn = get_connection()
    df = pd.read_excel("dados/itens_pedidos.xlsx")
    df.to_sql("itens_pedido", conn, if_exists="append", index=False)
    conn.close()
    print(f"{len(df)} itens inseridos!")

# Ingerindo os dados de pagamentos
def inserir_pagamentos():
    conn = get_connection()
    df = pd.read_excel("dados/pagamentos.xlsx")
    df.to_sql("pagamentos", conn, if_exists="append", index=False)
    conn.close()
    print(f"{len(df)} pagamentos inseridos!")


# inserindo todas as funções
if __name__ == "__main__":
    inserir_clientes()
    inserir_vendedores()
    inserir_produtos()
    inserir_pedidos()
    inserir_itens_pedido()
    inserir_pagamentos()
    print("Ingestão concluída!")