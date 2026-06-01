from agent import graph
from langchain_core.messages import HumanMessage

pergunta = "Qual vendedor teve mais vendas?"

resultado = graph.invoke({
    "messages": [HumanMessage(content=pergunta)]
})

print(resultado["messages"][-1].content)