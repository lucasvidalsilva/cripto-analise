import streamlit as st
import pandas as pd
import plotly.express as px
import os
from dotenv import load_dotenv
from sqlalchemy import create_engine
from openai import OpenAI
import time

load_dotenv()

DATABASE_URL = os.getenv('DIRECT_URL')
API_KEY_OPENROUTER = os.getenv('OPENROUTER_API_KEY')

engine = create_engine(DATABASE_URL)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=API_KEY_OPENROUTER,
)

def load_criptosinfo():
    try:
        query = 'SELECT * FROM dw."gold-criptosinfo"'
        return pd.read_sql(query, engine)
    except:
        return None

def load_criptosnews():
    try:
        query = 'SELECT * FROM dw."bronze-criptosnews"'
        return pd.read_sql(query, engine)
    except:
        return None

df_tabelainfo = load_criptosinfo()
df_tabelanews = load_criptosnews()

def processar_pergunta(pergunta, tentativas=3, atraso_inicial=1):
    if df_tabelainfo is None or df_tabelainfo.empty or df_tabelanews is None:
        return "Erro: Não há dados disponíveis para análise."

    criptosinfos = df_tabelainfo.to_string()
    criptosnews = df_tabelanews.to_string()

    prompt = f"""
    Você é um especialista em análise de criptomoedas. Com base nas informações abaixo, responda à pergunta:

    Tabela de informações das criptomoedas:
    {criptosinfos}

    Notícias relacionadas:
    {criptosnews}

    Pergunta: {pergunta}
    """

    for tentativa in range(tentativas):
        try:
            completion = client.chat.completions.create(
                extra_headers={
                    "HTTP-Referer": "https://seusite.com",
                    "X-Title": "Seu Projeto de IA"
                },
                model="google/gemini-2.5-pro-exp-03-25:free",
                messages=[{"role": "user", "content": prompt}]
            )
            if completion and hasattr(completion, "choices") and completion.choices:
                return completion.choices[0].message.content
            return "Erro: A resposta da IA veio vazia."
        except Exception as e:
            if "429" in str(e) and tentativa < tentativas - 1:
                time.sleep(atraso_inicial * (2 ** tentativa))
            else:
                return f"Erro: {e}"

    return "Falha ao processar a pergunta após várias tentativas."

menu = st.sidebar.radio("Menu", ["Dashboard", "Pesquisar", "Sobre"], label_visibility="collapsed")

if menu == "Dashboard":
    st.title("Analise de Criptomoedas")

    if df_tabelainfo is None or df_tabelainfo.empty:
        st.error("Erro ao carregar os dados.")
    else:
        criptos = df_tabelainfo['cripto'].unique()
        selecionadas = st.multiselect("Escolha as criptomoedas:", criptos, default=criptos[:5])
        df_filtrado = df_tabelainfo[df_tabelainfo['cripto'].isin(selecionadas)]

        st.markdown("### Preço Atual")
        st.plotly_chart(
            px.bar(df_filtrado, x='cripto', y='price', color='cripto', text='price', title="Preço das Criptomoedas"),
            use_container_width=True
        )

        st.markdown("### Tendência de Preço")
        st.plotly_chart(
            px.bar(df_filtrado, x='cripto', y='tedencia_preco', color='cripto', text='tedencia_preco', title="Tendência de Preço"),
            use_container_width=True
        )

        st.markdown("### RSI (Índice de Força Relativa - 14)")
        st.plotly_chart(
            px.line(df_filtrado, x='cripto', y='rsi_14', markers=True, title='RSI 14'),
            use_container_width=True
        )

        st.markdown("### MACD")
        st.plotly_chart(
            px.line(df_filtrado, x='cripto', y='macd', markers=True, title='MACD'),
            use_container_width=True
        )

        st.markdown("### Média Móvel (MA 7)")
        st.plotly_chart(
            px.line(df_filtrado, x='cripto', y='ma_7', markers=True, title='Média Móvel 7 Dias'),
            use_container_width=True
        )

        st.markdown("### Spread (Diferença Ask - Bid)")
        st.plotly_chart(
            px.bar(df_filtrado, x='cripto', y='spread', color='cripto', text='spread', title='Spread (Ask - Bid)'),
            use_container_width=True
        )

        st.markdown("### Sinal do Livro de Ordens")
        st.dataframe(df_filtrado[['cripto', 'ordem_livro_sinal']], use_container_width=True)

        st.markdown("### Recomendação de Ação")
        st.dataframe(df_filtrado[['cripto', 'recomendacao']], use_container_width=True)

        st.markdown("### Dominância do BTC")
        if 'BTC/USDT' in df_filtrado['cripto'].values:
            btc_row = df_filtrado[df_filtrado['cripto'] == 'BTC/USDT'].iloc[0]
            st.metric("Dominância do BTC", f"{btc_row['dominancia_btc']}%")

        st.markdown("### Última Atualização")
        data_extracao = df_filtrado['data_extracao'].max()
        st.info(f"Dados atualizados em: **{data_extracao}**")

elif menu == "Pesquisar":
    st.header("Pesquisar com IA")
    pergunta = st.text_area("Escreva sua pergunta:")
    if st.button("Enviar"):
        resposta = processar_pergunta(pergunta)
        st.markdown(f"**Você:** {pergunta}")
        st.markdown(f"**IA:** {resposta}")

elif menu == "Sobre":
    st.title("Sobre o Projeto")
    st.write("Análise visual e assistida por IA do mercado de criptomoedas.")
