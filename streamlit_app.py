pip install matplotlib
pip install pandas

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


# Título da página e configuração inicial
st.set_page_config(page_title="Análise de vendas", page_icon=":bar_chart:")

# Título
st.title('Análise de vendas')

# URL da planilha
xlsx_url = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vQt8EOEnxeGbcvhHIz_5ubSFJk9G8ids7B-xW8OpsViI3rQVhMdtKFuXl_Lmrnb8h0jWnaoL0cQK2rR/pub?output=xlsx'

# Carregar as abas da planilha
st.subheader("Carregando dados da planilha...")

try:
    xls = pd.ExcelFile(xlsx_url)

    # Carregar os dados da de dados gerais
    df = pd.read_excel(xlsx_url, sheet_name='Cópia de DADOS GERAIS COMERCIAL')

    # Exibir os primeiros registros do DataFrame 
    st.write("Visualizando os primeiros registros da planilha:")
    st.dataframe(df.head(15))

    # Métrica de qualificados e os que assinaram
    atendem = df['Atende aos requisitos']
    assinado = df['Data da assinatura']
    leads = df['Nome']
    respostas = df['Respondeu as msgns']
    aceites = df['Aceitou']
   
    contagem_leads = leads.value_counts() # leads
    contagem_respostas = respostas.value_counts() # Leads que responderam
    contagem_atendem = atendem.value_counts() # Atendem aos requisitos
    contagem_aceites = aceites.value_counts() # Aceites
    contagem_assinado = assinado.value_counts() # Assinaram

    # Exibir contagens de atendem e assinados
    # st.write(f"Total que atendem aos requisitos: {contagem_atendem.sum()}")
    # st.write(f"Total que assinaram: {contagem_assinado.sum()}")

    # Criar listas de dados para gráficos
    dados = {
        'Aptos': contagem_atendem.sum(),
        'Assinaram': contagem_assinado.sum()
    }
    Tabela_dados = {
        'Aptos': [contagem_atendem.sum()],
        'Assinaram': [contagem_assinado.sum()]
    }
    contagem_leads = {
        'Indíce': ['Leads', 'REsponderam', 'Aptos', 'Aceitaram', 'Assinaram'],
        'Colunas':[[contagem_leads.sum()],[contagem_respostas.sum()],[contagem_atendem.sum()],[contagem_aceites.sum()],[contagem_assinado.sum()]]
    } 
 
   
    df_tabela_dados = pd.DataFrame(Tabela_dados)
    st.subheader('Tabela e gráfico de conversão')
    st.table(df_tabela_dados)

     
    # Gerar gráfico de pizza
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.pie(dados.values(), labels=dados.keys(), autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Assegura que o gráfico de pizza será circular

    st.pyplot(fig)  # Exibe o gráfico no Streamlit

    # Carregar os dados da aba específica
    df = pd.read_excel(xlsx_url, sheet_name='PAINEL DE SETEMBRO')

    # Dados gerais
    dados_gerais = {
        'Data':df.iloc[5, 17],
        'Assinados hoje': [df.iloc[5, 18]], 
        'Pré-contratos': [df.iloc[5, 19]],
        'Contratos': [df.iloc[5, 20]],
        'Contratos': [df.iloc[5, 20]]
    }
    
    df_tabela = pd.DataFrame(dados_gerais)
    
    st.subheader('Resumo do dia')
    st.table(df_tabela)

    st.subheader('Funil em resumo')
    st.table(contagem_leads)
    
except Exception as e:
    st.error(f"Erro ao carregar a planilha: {e}")
