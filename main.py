import streamlit as st
from src.agent import graph
from langchain_core.messages import HumanMessage, AIMessage

st.title("Agente de Análise de Vendas")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Faça uma pergunta sobre as vendas..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    resposta = "Não consegui processar sua pergunta. Tente novamente."

    with st.chat_message("assistant"):
        with st.spinner("Analisando..."):
            try:
                resultado = graph.invoke({
                    "messages": [HumanMessage(content=prompt)]
                })
                for mensagem in reversed(resultado["messages"]):
                    if isinstance(mensagem, AIMessage) and mensagem.content.strip():
                        resposta = mensagem.content.strip()
                        break
            except Exception as e:
                resposta = f"Erro ao processar: {str(e)}"
        st.write(resposta)

    st.session_state.messages.append({"role": "assistant", "content": resposta})