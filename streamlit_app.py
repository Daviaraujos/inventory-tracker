import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import requests
from streamlit_autorefresh import st_autorefresh

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

    # Ler o conteúdo do arquivo Excel a partir dos bytes recebidos
    xls = pd.ExcelFile(response.content)

    # Carregar os dados gerais
    df = pd.read_excel(xls, sheet_name='Cópia de DADOS GERAIS COMERCIAL')

    # Verificar as colunas disponíveis no DataFrame
    st.write("Colunas disponíveis no DataFrame:", df.columns.tolist())

    # Certificar-se de que 'Data da assinatura' está no formato datetime
    df['Data da assinatura'] = pd.to_datetime(df['Data da assinatura'], errors='coerce')

    # Barra de pesquisa para buscar por nome do consultor
    search_term = st.text_input('Digite o nome do consultor para buscar:')

    # Verifica se o usuário digitou algo na barra de pesquisa
    if search_term:
        df_filtered = df[df['Consultor'].str.contains(search_term, case=False, na=False)]
        st.write(f"Resultados da busca para '{search_term}':")
        st.dataframe(df_filtered)

        if df_filtered.empty:
            st.warning(f"Nenhum resultado encontrado para '{search_term}'.")

    # Exibir os primeiros registros do DataFrame 
    st.write("Visualizando os registros mais recentes da planilha:")
    st.dataframe(df.tail(30))

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

    # Funil de vendas
    st.subheader('Funil em resumo')
    data_funel = {
        'Etapas': ['Leads', 'Responderam', 'Aptos', 'Aceitaram', 'Assinaram'],
        'Valores': [contagem_leads, contagem_respostas, contagem_atendem, contagem_aceites, contagem_assinado]
    }

    fig_funnel = px.funnel(data_funel, x='Valores', y='Etapas', title='Funil de Vendas')
    st.plotly_chart(fig_funnel)

    # Converter a coluna 'Aceitou' para valores numéricos: 1 para 'Sim', 0 para 'Não'
    df['Aceitaram'] = df['Aceitou'].apply(lambda x: 1 if x == 'sim' or 'SIM' else 0)

    # Agrupar por consultor e somar as assinaturas
    vendas_por_consultor = df.groupby('Consultor')['Aceitaram'].sum().reset_index()

    # Renomear a coluna para melhor clareza
    vendas_por_consultor.rename(columns={'Aceitaram': 'Total de Assinaturas'}, inplace=True)

    # Exibir tabela de consultores e suas respectivas vendas
    st.subheader('Total de assinaturas por consultor')
    st.table(vendas_por_consultor)

except Exception as e:
    st.error(f"Erro ao carregar a planilha: {e}")
