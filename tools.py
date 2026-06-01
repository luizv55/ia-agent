import sqlite3
from langchain_core.tools import tool
from database import get_connection

@tool
def buscar_no_banco(sql: str) -> str:  # retorna uma string dps da busca da busca de SQl
    """Executa uma função SQl no banco de vendas"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(sql)
    resultado = cursor.fetchall()
    conn.close()

    # Caso n tenha resultado
    if not resultado:
        return 'Sem resultado'
    
    return str(resultado)