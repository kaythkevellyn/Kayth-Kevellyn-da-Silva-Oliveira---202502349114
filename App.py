import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# CONFIGURAÇÃO
st.set_page_config(
    page_title="Dashboard de Funcionários",
    layout="wide"
)
st.title("Dashboard de Análise de Funcionários")

# FUNÇÃO DE DADOS
@st.cache_data
def carregar_dados():
    dados = {
        "nome": ["Ana", "Bruno", "Carlos", "Daniela", "Eduardo"],
        "idade": [23, 35, 29, np.nan, 40],
        "cidade": ["SP", "RJ", "SP", "MG", "RJ"],
        "salario": [3000, 5000, 4000, 3500, np.nan],
        "data_contratacao": pd.to_datetime([
            "2020-01-10", "2019-03-15", "2021-07-22", "2018-11-30", "2022-05-10"
        ])
    }

    df = pd.DataFrame(dados)

    # Limpeza
    df["idade"] = df["idade"].fillna(df["idade"].mean())
    df["salario"] = df["salario"].fillna(df["salario"].median())

    # Feature engineering
    df["salario_anual"] = df["salario"] * 12
    df["ano_contratacao"] = df["data_contratacao"].dt.year

    df["categoria_salario"] = df["salario"].apply(
        lambda x: "Alto" if x > 4500 else "Médio" if x > 3000 else "Baixo"
    )

    return df

# UPLOAD (SUBSTITUI DADOS)
st.sidebar.subheader("Upload de CSV")

uploaded_file = st.sidebar.file_uploader("Envie um CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)
else:
    df = carregar_dados()

# SIDEBAR (FILTROS)
st.sidebar.header("Filtros")

cidades = st.sidebar.multiselect(
    "Selecione a cidade",
    options=df["cidade"].unique(),
    default=df["cidade"].unique()
)

faixa_salario = st.sidebar.slider(
    "Faixa salarial",
    float(df["salario"].min()),
    float(df["salario"].max()),
    (float(df["salario"].min()), float(df["salario"].max()))
)

# NOVO FILTRO
categoria = st.sidebar.selectbox(
    "Categoria de salário",
    options=["Todas"] + list(df["categoria_salario"].unique())
)

# APLICAR FILTROS
df_filtrado = df[
    (df["cidade"].isin(cidades)) &
    (df["salario"] >= faixa_salario[0]) &
    (df["salario"] <= faixa_salario[1])
]

# APLICAR FILTRO DE CATEGORIA
if categoria != "Todas":
    df_filtrado = df_filtrado[df_filtrado["categoria_salario"] == categoria]

# KPIs
col1, col2, col3 = st.columns(3)

col1.metric("Salário Médio", f"R$ {df_filtrado['salario'].mean():.2f}")
col2.metric("Total Funcionários", df_filtrado.shape[0])
col3.metric("Salário Máximo", f"R$ {df_filtrado['salario'].max():.2f}")

# TABELA
st.subheader("Dados")
st.dataframe(df_filtrado, use_container_width=True)

# GRÁFICOS (PLOTLY)
st.subheader("Análises")

col1, col2 = st.columns(2)

# Gráfico 1
fig1 = px.bar(
    df_filtrado,
    x="cidade",
    y="salario",
    color="categoria_salario",
    title="Salário por Cidade"
)
col1.plotly_chart(fig1, use_container_width=True)

# Gráfico 2
fig2 = px.histogram(
    df_filtrado,
    x="categoria_salario",
    color="categoria_salario",
    title="Distribuição de Categorias"
)
col2.plotly_chart(fig2, use_container_width=True)

# PIVOT TABLE
st.subheader("Tabela Dinâmica")

pivot = pd.pivot_table(
    df_filtrado,
    values="salario",
    index="cidade",
    columns="categoria_salario",
    aggfunc="mean"
)
st.dataframe(pivot)

# DOWNLOAD
st.subheader("Download dos dados")

csv = df_filtrado.to_csv(index=False).encode("utf-8")

st.download_button(
    label="Baixar CSV",
    data=csv,
    file_name="dados_filtrados.csv",
    mime="text/csv"
)