import pandas as pd
import os
from src.database import get_connection

BASE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "base de dados", "dados")

def inserir_clientes():
    conn = get_connection()
    df = pd.read_excel(os.path.join(BASE_DIR, "clientes.xlsx"))
    df = df.drop(columns=["id"])
    df.to_sql("clientes", conn, if_exists="append", index=False)
    conn.close()
    print(f"{len(df)} clientes inseridos!")

def inserir_vendedores():
    conn = get_connection()
    df = pd.read_excel(os.path.join(BASE_DIR, "vendedores.xlsx"))
    df = df.drop(columns=["id"]).drop_duplicates(subset=["email_corporativo"])
    df.to_sql("vendedores", conn, if_exists="append", index=False)
    conn.close()
    print(f"{len(df)} vendedores inseridos!")

def inserir_produtos():
    conn = get_connection()
    df = pd.read_excel(os.path.join(BASE_DIR, "produtos.xlsx"))
    df = df.drop(columns=["id"])
    df.to_sql("produtos", conn, if_exists="append", index=False)
    conn.close()
    print(f"{len(df)} produtos inseridos!")

def inserir_pedidos():
    conn = get_connection()
    df = pd.read_excel(os.path.join(BASE_DIR, "pedidos.xlsx"))
    df = df.drop(columns=["id"])
    df["status"] = df["status"].str.lower()
    df.to_sql("pedidos", conn, if_exists="append", index=False)
    conn.close()
    print(f"{len(df)} pedidos inseridos!")

def inserir_itens_pedido():
    conn = get_connection()
    df = pd.read_excel(os.path.join(BASE_DIR, "itens_pedidos.xlsx"))
    df = df.drop(columns=["id"])
    df.to_sql("itens_pedido", conn, if_exists="append", index=False)
    conn.close()
    print(f"{len(df)} itens inseridos!")

def inserir_pagamentos():
    conn = get_connection()
    df = pd.read_excel(os.path.join(BASE_DIR, "pagamentos.xlsx"))
    df = df.drop(columns=["id"])
    df.to_sql("pagamentos", conn, if_exists="append", index=False)
    conn.close()
    print(f"{len(df)} pagamentos inseridos!")

if __name__ == "__main__":
    inserir_clientes()
    inserir_vendedores()
    inserir_produtos()
    inserir_pedidos()
    inserir_itens_pedido()
    inserir_pagamentos()
    print("Ingestão concluída!")