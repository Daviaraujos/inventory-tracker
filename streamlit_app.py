import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import streamlit as st
import requests  # Adicionado aqui
from streamlit_autorefresh import st_autorefresh

# Configuração da página
st.set_page_config(page_title="Análise de Vendas", page_icon=":bar_chart:")

# Atualização automática a cada 15 segundos
st_autorefresh(interval=15000, key="data_refresh")

# Título do dashboard
st.title('Análise de Vendas')

# Carregar dados da planilha Excel (substitua pelo seu arquivo)
# URL da planilha
try:
    response = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vQt8EOEnxeGbcvhHIz_5ubSFJk9G8ids7B-xW8OpsViI3rQVhMdtKFuXl_Lmrnb8h0jWnaoL0cQK2rR/pub?output=xlsx')
    response.raise_for_status()
    xls = pd.ExcelFile(response.content)
    df = pd.read_excel(xls, sheet_name='Cópia de DADOS GERAIS COMERCIAL 1')

    # Converter colunas de datas e limpar dados
    df['Data da assinatura'] = pd.to_datetime(df['Data da assinatura'], errors='coerce')

    # Principais métricas
    total_leads = df['Number_leads'].count()
    leads_qualificados = df[df['Atende aos requisitos'] == 'Sim']['Number_leads'].count()
    leads_respondidos = df[df['Respondeu as msgns'] == 'Sim']['Number_leads'].count()
    propostas_aceitas = df[df['Aceitou'] == 'Sim']['Number_leads'].count()
    assinaturas_finalizadas = df['Data da assinatura'].notnull().sum()
    
    taxa_conversao = (assinaturas_finalizadas / total_leads) * 100 if total_leads else 0
    taxa_resposta = (leads_respondidos / total_leads) * 100 if total_leads else 0

    # Exibição das métricas
    st.metric("Total de Leads", total_leads)
    st.metric("Leads Qualificados", leads_qualificados)
    st.metric("Leads Respondidos", leads_respondidos)
    st.metric("Propostas Aceitas", propostas_aceitas)
    st.metric("Assinaturas Finalizadas", assinaturas_finalizadas)
    st.metric("Taxa de Conversão (%)", f"{taxa_conversao:.2f}")
    st.metric("Taxa de Resposta (%)", f"{taxa_resposta:.2f}")

    # Desempenho por consultor
    vendas_por_consultor = df[df['Aceitou'] == 'Sim'].groupby('Consultor')['Number_leads'].count().reset_index()
    vendas_por_consultor.columns = ['Consultor', 'Total de Vendas']
    vendas_por_consultor = vendas_por_consultor.sort_values(by='Total de Vendas', ascending=False)

    st.subheader("Desempenho por Consultor")
    st.dataframe(vendas_por_consultor)

    # Gráfico de barras de desempenho por consultor
    fig_bar = px.bar(vendas_por_consultor, x='Consultor', y='Total de Vendas', title="Vendas por Consultor")
    st.plotly_chart(fig_bar)

    # Funil de vendas
    funil_dados = {
        'Etapas': ['Leads', 'Leads Qualificados', 'Leads Respondidos', 'Propostas Aceitas', 'Assinaturas Finalizadas'],
        'Valores': [total_leads, leads_qualificados, leads_respondidos, propostas_aceitas, assinaturas_finalizadas]
    }
    fig_funnel = px.funnel(funil_dados, x='Valores', y='Etapas', title="Funil de Vendas")
    st.plotly_chart(fig_funnel)

    # Análise de tempo médio de fechamento
    df['Tempo de Fechamento'] = (df['Data da assinatura'] - df['Data do primeiro contato']).dt.days
    tempo_medio_fechamento = df['Tempo de Fechamento'].mean()
    st.metric("Tempo Médio de Fechamento (dias)", f"{tempo_medio_fechamento:.2f}" if not pd.isna(tempo_medio_fechamento) else "N/A")

    # Gráfico de distribuição de tempo de fechamento
    fig_hist = px.histogram(df, x='Tempo de Fechamento', nbins=30, title="Distribuição do Tempo de Fechamento")
    st.plotly_chart(fig_hist)

except Exception as e:
    st.error(f"Erro ao carregar a planilha: {e}")
