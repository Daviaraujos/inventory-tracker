import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import requests
from streamlit_autorefresh import st_autorefresh  # Importação do autorefresh

# Configuração da página
st.set_page_config(page_title="Análise de vendas", page_icon=":bar_chart:")

# Atualização automática a cada 15 segundos
st_autorefresh(interval=15000, key="data_refresh")

# Título
st.title('Análise de vendas')

# URL da planilha
try:
    response = requests.get('https://docs.google.com/spreadsheets/d/e/2PACX-1vQt8EOEnxeGbcvhHIz_5ubSFJk9G8ids7B-xW8OpsViI3rQVhMdtKFuXl_Lmrnb8h0jWnaoL0cQK2rR/pub?output=xlsx')
    response.raise_for_status()  # Verifica se a requisição foi bem-sucedida

    # Carregar as abas da planilha
    st.subheader("Carregando dados da planilha...")

    # Ler o conteúdo do arquivo Excel a partir dos bytes recebidos
    xls = pd.ExcelFile(response.content)

    # Carregar os dados gerais
    df = pd.read_excel(xls, sheet_name='Cópia de DADOS GERAIS COMERCIAL')

    # Exibir os primeiros registros do DataFrame 
    st.write("Visualizando os registros mais recentes da planilha:")
    st.dataframe(df.tail(15))

    # Métrica de qualificados e os que assinaram
    atendem = df['Atende aos requisitos']
    assinado = df['Data da assinatura']
    leads = df['Number_leads']
    respostas = df['Respondeu as msgns']
    aceites = df['Aceitou']
   
    # Contagens
    contagem_leads = leads.count()  # Total de leads
    contagem_respostas = respostas.count()  # Leads que responderam
    contagem_atendem = atendem.count()  # Atendem aos requisitos
    contagem_aceites = aceites.count()  # Aceitaram
    contagem_assinado = assinado.count()  # Assinaram

    # Criar DataFrame para exibir na tabela de conversão
    Tabela_dados = {
        'Aptos': [contagem_atendem],
        'Assinaram': [contagem_assinado]
    }
    df_tabela_dados = pd.DataFrame(Tabela_dados)
    st.subheader('Tabela e gráfico de conversão')
    st.table(df_tabela_dados)

    # Gerar gráfico de pizza
    fig, ax = plt.subplots(figsize=(3, 3))
    dados = {
        'Aptos': contagem_atendem,
        'Assinaram': contagem_assinado
    }
    ax.pie(dados.values(), labels=dados.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Assegura que o gráfico de pizza será circular
    st.pyplot(fig)  # Exibe o gráfico no Streamlit

    # Carregar os dados da aba específica
    df_painel = pd.read_excel(xls, sheet_name='PAINEL DE SETEMBRO')

    # Dados gerais
    dados_gerais = {
        'Data': df_painel.iloc[5, 17],
        'Assinados hoje': [df_painel.iloc[5, 18]], 
        'Pré-contratos': [df_painel.iloc[5, 19]],
        'Contratos': [df_painel.iloc[5, 20]]
    }
    
    df_tabela = pd.DataFrame(dados_gerais)
    
    st.subheader('Resumo do dia')
    st.table(df_tabela)

    # Funil em resumo
    st.subheader('Funil em resumo')

    # Criar dados corretos para o gráfico de funil
    data_funel = {
        'Etapas': ['Leads', 'Responderam', 'Aptos', 'Aceitaram', 'Assinaram'],
        'Valores': [contagem_leads, contagem_respostas, contagem_atendem, contagem_aceites, contagem_assinado]
    }

    # Criando o gráfico de funil
    fig_funnel = px.funnel(data_funel, x='Valores', y='Etapas', title='Funil de Vendas')

    # Exibindo no Streamlit
    st.plotly_chart(fig_funnel)

    # Puxar dados das assinaturas
    st.write("Últimas assinaturas")

except Exception as e:
    st.error(f"Erro ao carregar a planilha: {e}")
