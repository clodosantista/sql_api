import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_option_menu import option_menu
from query import conexao

#*** primeira consulta / atualizacoes de dados

query = "SELECT * FROM tb_carros"

# carregar dados

df = conexao(query)

# botao pra atualizar
if st.button("Atualizar Dados"):
    df = conexao(query)

#**** ESTRUTURA LATERAL DE FILTROS*****
st.sidebar.header("Selecione o Filtro")

marca = st.sidebar.multiselect("Marca Selecionada", options=df["marca"].unique(),default =df["marca"].unique())
modelo = st.sidebar.multiselect("modelo Selecionada", options=df["modelo"].unique(),default =df["modelo"].unique())
ano = st.sidebar.multiselect("ano", options=df["ano"].unique(),default =df["ano"].unique())
cor = st.sidebar.multiselect("cor", options=df["cor"].unique(),default =df["cor"].unique())
valor = st.sidebar.multiselect("valor", options=df["valor"].unique(),default =df["valor"].unique())
numero_vendas = st.sidebar.multiselect("numero_vendas", options=df["numero_vendas"].unique(),default =df["numero_vendas"].unique())

#aplicar os filtros selecionados
df_selecionado = df[
    (df["marca"].isin(marca)) &
    (df["modelo"].isin(modelo)) &
    (df["ano"].isin(ano)) &
    (df["valor"].isin(valor)) &
    (df["cor"].isin(cor)) &
    (df["numero_vendas"].isin(numero_vendas)) 

]

#***EXIBIR VALORES MEDIOS - ESTATISTICA
def Home():
    with st.expander("Valores"):
        mostrarDados = st.multiselect('Filter:', df_selecionado, default=[])

        if mostrarDados:
            st.write(df_selecionado[mostrarDados])

    if not df_selecionado.empty:
        venda_total = df_selecionado["numero_vendas"].sum()
        venda_media = df_selecionado["numero_vendas"].mean()
        venda_mediana = df_selecionado["numero_vendas"].median()

        total1, total2, total3 = st.columns(3, gap="large")

        with total1:
            st.info("valor total de vendas dos carros", icon='🚩')
            st.metric(label="total", value=f"{venda_total:,.0f}")

        with total2:
            st.info("valor medio das vendas", icon='🚩')
            st.metric(label="media", value=f"{venda_media:,.0f}")

        with total3:
            st.info("valor mediano dos carros", icon='🚩')
            st.metric(label="mediana", value=f"{venda_mediana:,.0f}")

    else:
        st.warning("nehum dado disponivel com os filtros selecionados")

    st.markdown(""""--------""")

    #*********graficos***************

def graficos(df_selecionado):
    if df_selecionado.empty:
        st.warning("nehum dados disponivel para gerar graficos")
        return
        
    #criacao dos graficos
    #4 abas > grafico de barras,grafico de linhas,grafico de pizza e dispeesao

    graf1, graf2, graf3, graf4 = st.tabs(["grafico de barras","grafico de linhas","grafico de pizza","grafico de dispersao"])

    with graf1:
        st.write("grafico de barras") # titulo

        investimento = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by="valor", ascending=False)
        #agrupa pela marca e conta o numero de ocorrencias da coluna valor, depois ordena o resultado de forma decrecente.

        fig_valores = px.bar(investimento, x=investimento.index, y="valor",orientation="h", title="<b>valores de carros</b>", color_discrete_sequence=["#0083b3"])
                             
        st.plotly_chart(fig_valores, use_container_width=True)

    with graf2:
        st.write("grafico de linhas") # titulo
        dados = df_selecionado.groupby("marca").count()[["valor"]]

        fig_valores2 = px.line(dados, x=dados.index, y="valor", title="<b>valores por marca</b>", color_discrete_sequence=["#0083b8"])

        st.plotly_chart(fig_valores2, use_container_width=True)

    with graf3:
        st.write("grafico de pizza") # titulo
        dados2 = df_selecionado.groupby("marca").sum()[["valor"]]

        fig_valores3 = px.pie(dados2, values="valor", names=dados2.index, title="<b>distribuicao de valores por marca</b>")

        st.plotly_chart(fig_valores3, use_container_width=True)

    with graf4:
        st.write("grafico de dispersao") # titulo
        dados3 = df_selecionado.melt(id_vars=["marca"], value_vars=["valor"])

        fig_valores4 = px.scatter(dados3, x="marca", y="value", color="variable", title="<b>dispersao de valores por marca</b>")

        st.plotly_chart(fig_valores4, use_container_width=True)

def barraprogresso():
    valorAtual = df_selecionado["numero_vendas"].sum()
    objetivo = 200000
    percentual = round((valorAtual / objetivo * 100))


    if percentual >100:
        st.subheader("valores atingidos!!!")
    else:
        st.write(f"voce tem{percentual}% de {objetivo}. corra atras filhao!")
        mybar = st.progress(0)
        for percentualCompleto in range(percentual):
            mybar.progress(percentualCompleto + 1, text="alvo %")

#*****************************menu lateral*********************
def menulateral():
    with st.sidebar:
        selecionado = option_menu(menu_title="menu", options=["home", "progresso"], icons=["house", "eye"], menu_icon="cast", default_index=0)

    if selecionado == "home":
        st.subheader(f"pagina:{selecionado}")
        Home()
        graficos(df_selecionado)

    if selecionado == "progresso":
        st.subheader(f"pagina:{selecionado}")
        barraprogresso()
        graficos(df_selecionado)

menulateral()







            