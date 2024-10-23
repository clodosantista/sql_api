import streamlit as st
import pandas as pd
import numpy as np

chart_data = pd.DataFrame(np.random.randn(20, 3), columns=["G", "GG", "GGG"])

st.bar_chart(chart_data)

# with graf1:
#         st.write("grafico de barras") # titulo

#         tamanho = df_selecionado.groupby("marca").count()[["valor"]].sort_values(by="valor", ascending=False)

#         dados1 = df_selecionado.groupby("marca").sum()[["valor"]]

#         fig_valores3 = px.pie(dados1, values="valor", names=dados1.index, title="<b>distribuicao de valores por marca</b>")

#         st.plotly_chart(fig_valores1, use_container_width=True)