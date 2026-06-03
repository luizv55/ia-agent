from langchain_core.tools import tool
from .database import get_connection

@tool
def buscar_no_banco(sql: str) -> str:
    """Executa uma query SQL no banco de vendas e retorna os resultados."""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(sql)
            resultado = cursor.fetchall()
        if not resultado:
            return "Nenhum resultado encontrado."
        return str(resultado)
    except Exception as e:
        return f"Erro ao executar SQL: {e}"