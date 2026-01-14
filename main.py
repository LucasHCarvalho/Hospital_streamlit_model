import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Carregando a base de dados simulada
df = pd.read_csv('hospital_data.csv', parse_dates=['Data'])

# Título do relatório
st.title('Relatório Financeiro - Hospital')

# Filtro por data (período de análise)
start_date = st.date_input('Data Início', df['Data'].min())
end_date = st.date_input('Data Fim', df['Data'].max())
df_filtered = df[(df['Data'] >= pd.to_datetime(start_date)) & (df['Data'] <= pd.to_datetime(end_date))]

# Gráfico de Linha - Faturamento e Tendência
st.subheader('Faturamento e Tendência')

df_grouped = df_filtered.groupby(df_filtered['Data'].dt.to_period('M')).agg({'Faturamento': 'sum'}).reset_index()
df_grouped['Data'] = df_grouped['Data'].dt.to_timestamp()

# Gráfico de linha
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(df_grouped['Data'], df_grouped['Faturamento'], label='Faturamento', color='b')
ax.set_title('Faturamento Mensal')
ax.set_xlabel('Data')
ax.set_ylabel('Faturamento (R$)')
ax.grid(True)

# Exibindo gráfico
st.pyplot(fig)

# Cálculo da Variação MoM e YoY
df_grouped['Variação MoM'] = df_grouped['Faturamento'].pct_change() * 100
df_grouped['Ano'] = df_grouped['Data'].dt.year
df_grouped['Mês'] = df_grouped['Data'].dt.month

# Variação MoM
st.subheader('Variação MoM')
st.write(df_grouped[['Data', 'Faturamento', 'Variação MoM']].dropna())

# Variação YoY
df_grouped_yoy = df_grouped[df_grouped['Mês'] == 1]
df_grouped_yoy = df_grouped_yoy[['Ano', 'Faturamento']].groupby('Ano').agg({'Faturamento': 'sum'}).reset_index()
df_grouped_yoy['Variação YoY'] = df_grouped_yoy['Faturamento'].pct_change() * 100

st.subheader('Variação YoY')
st.write(df_grouped_yoy[['Ano', 'Faturamento', 'Variação YoY']].dropna())

# Gráfico de Ticket Médio por Procedimento
st.subheader('Rank de Maior Ticket Médio por Procedimento')

df_procedimento = df_filtered.groupby('Procedimento').agg({'Faturamento': 'mean'}).reset_index()
df_procedimento = df_procedimento.sort_values('Faturamento', ascending=False)

# Gráfico de barras
fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(x='Faturamento', y='Procedimento', data=df_procedimento, ax=ax, palette='viridis')
ax.set_title('Rank de Maior Ticket Médio por Procedimento')
ax.set_xlabel('Ticket Médio (R$)')
ax.set_ylabel('Procedimento')

st.pyplot(fig)

# Análise de Pacientes por Idade e CID
st.subheader('Análise de Pacientes - Idade e CID')

df_idade_cid = df_filtered.groupby(['Idade', 'CID']).agg({'Faturamento': 'sum'}).reset_index()

# Gráfico de dispersão
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='Idade', y='Faturamento', hue='CID', data=df_idade_cid, ax=ax, palette='deep')
ax.set_title('Faturamento por Idade e CID')
ax.set_xlabel('Idade')
ax.set_ylabel('Faturamento (R$)')

st.pyplot(fig)
