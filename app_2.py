import streamlit as st
import pandas as pd
import sqlite3

# Função para conectar ao banco de dados e obter os dados
def get_data():
    conn = sqlite3.connect('base_taxas.db')
    df = pd.read_sql_query("SELECT * FROM taxas", conn)
    conn.close()
    return df



# Caminho para a imagem
caminho_imagem = 'img_ML.png'


# Exibir a imagem
st.image(caminho_imagem, caption='Mercado Livre', use_column_width=True)

# Título da aplicação
st.title('Base de Dados de Taxas')

# Obter os dados do banco de dados
df = get_data()

# Exibir o DataFrame na aplicação
st.write('Tabela de Taxas:', df)

# Seções de entrada
st.divider()
preco_venda = st.number_input("PREÇO VENDA (R$)", min_value=0.00, max_value=100000.00, step=0.01, format="%.2f")
st.divider()
preco_custo = st.number_input("PREÇO CUSTO PRODUTO (R$)", min_value=0.00, max_value=100000.00, step=0.01, format="%.2f")
st.divider()
preco_frete_gratis = st.number_input("PREÇO FRETE GRÁTIS (CLIENTE) (R$)", min_value=0.00, max_value=100000.00, step=0.01, format="%.2f")
st.divider()
preco_custo_fixo = st.number_input("CUSTO FIXO (R$)", min_value=0.00, value=6.00, max_value=100000.00, step=0.01, format="%.2f")
st.divider()
preco_custo_frete_mercadoria = st.number_input("FRETE MERCADORIA (R$)", min_value=0.00, value=0.50, max_value=100000.00, step=0.01, format="%.2f")
st.divider()
preco_embalagem = st.number_input("PREÇO EMBALAGEM (R$)", min_value=0.00, value=0.25, max_value=100000.00, step=0.01, format="%.2f")

# Taxas de cartão
opcoes_taxa_cartao = [
    'CARTÃO DEBITO', 'DÉBITO VIRTUAL CAIXA', 'PIX', 
    'CREDITO A VISTA- RECEBER NA HORA', 'CREDITO A VISTA - RECEBER EM 14 DIAS', 
    'CREDITO A VISTA- RECEBER EM 30 DIAS', 'CREDITO PARCELADO CLIENTE ATE 12 VEZES - RECEBER 30 DIAS', 
    'CREDITO PARCELADO CLIENTE ATE 12 VEZES - RECEBER 14 DIAS'
]
taxas_cartao = [0.0199, 0.0399, 0.0, 0.0498, 0.0379, 0.0303, 0.0360, 0.0460]

# Convertendo taxas para porcentagem
taxas_cartao_percent = [f"{taxa * 100:.2f}%" for taxa in taxas_cartao]

# Criando o DataFrame com taxas de cartão
df_taxas = pd.DataFrame({
    'Tipo': opcoes_taxa_cartao,
    'Valor': taxas_cartao_percent
})

st.divider()
st.subheader("TAXAS CARTÃO")
# Exibindo o DataFrame no Streamlit
st.write('DataFrame com taxas de cartão:')
st.dataframe(df_taxas)

# Entrada de taxa de cartão pelo usuário
taxa_cartao_percent = st.number_input("TAXA CARTÃO (%)", min_value=0.00, value=3.79, max_value=100.00, step=0.01, format="%.2f")
# Convertendo a taxa percentual para decimal
taxa_cartao_div_100 = taxa_cartao_percent / 100

st.divider()
st.subheader("CATEGORIA DE PRODUTOS")
# Selecionar a categoria
if 'CATEGORIA' in df.columns:
    categoria = st.selectbox('Selecione a Categoria', df['CATEGORIA'].unique())

    st.divider()
    st.subheader("TIPO DE ANÚNCIO")
    # Selecionar o tipo de taxa
    tipo_taxa = st.radio('Selecione o Tipo de Taxa', ['Anúncio Clássico', 'Anúncio Premium'])

    # Obter a taxa correspondente
    if tipo_taxa == 'Anúncio Clássico':
        if 'CLASSICO' in df.columns:
            taxa_comissao_ML = df.loc[df['CATEGORIA'] == categoria, 'CLASSICO'].values[0]
            st.write(f'A taxa para a categoria {categoria} ({tipo_taxa}) é: {taxa_comissao_ML * 100:.2f}%')
        else:
            st.write("A coluna 'CLASSICO' não está presente no DataFrame.")
    else:
        if 'PREMIUM' in df.columns:
            taxa_comissao_ML = df.loc[df['CATEGORIA'] == categoria, 'PREMIUM'].values[0]
            st.write(f'A taxa para a categoria {categoria} ({tipo_taxa}) é: {taxa_comissao_ML * 100:.2f}%')
        else:
            st.write("A coluna 'PREMIUM' não está presente no DataFrame.")
else:
    st.write("A coluna 'CATEGORIA' não está presente no DataFrame.")


# calculando taxas
custo_taxas_sem_cartao=preco_custo_fixo+taxa_comissao_ML*preco_venda+preco_embalagem+preco_frete_gratis+preco_custo_frete_mercadoria
custo_taxas_com_cartao=preco_custo_fixo+taxa_comissao_ML*preco_venda+preco_embalagem+preco_frete_gratis+preco_custo_frete_mercadoria+taxa_cartao_div_100*preco_venda

#sem taxa cartao lucro
lucro_reais_sem_cartao=preco_venda-custo_taxas_sem_cartao-preco_custo
lucro_reais_sem_cartao_percentual_=lucro_reais_sem_cartao/preco_venda

#calculando lucro
lucro_reais_total=preco_venda-custo_taxas_com_cartao-preco_custo
lucro_reais_total_percentual=lucro_reais_total/preco_venda


# Criando o DataFrame com os resultados
df_resultados = pd.DataFrame({
    'Descrição': [
        'Custo Sem Taxa Cartão',
        'Custo Com Taxa Cartão',
        'Lucro Sem Taxa Cartão (R$)',
        'Lucro Sem Taxa Cartão (%)',
        'Lucro Total (R$)',
        'Lucro Total (%)'
    ],
    'Valor': [
        custo_taxas_sem_cartao,
        custo_taxas_com_cartao,
        lucro_reais_sem_cartao,
        f"{lucro_reais_sem_cartao_percentual_ * 100:.2f}%",
        lucro_reais_total,
        f"{lucro_reais_total_percentual * 100:.2f}%"
    ]
})

st.divider()
# Exibindo o DataFrame com os resultados no Streamlit
st.write('Resultados Calculados:')
st.dataframe(df_resultados)

# Área de destaque com bordas arredondadas, efeito de animação e estilo atualizado
html_content = f"""
<div style="background-color: yellow; color: black; border: 10px solid black; border-radius: 30px; padding: 20px; margin: 20px 0; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); animation: slideIn 1s; text-align: center;">
    <h3 style="color: green; font-weight: bold; text-align: center;">Lucro Total</h3>
    <p style="font-size: 20px; font-weight: bold;"><strong>Lucro Total em Reais:</strong> R$ {lucro_reais_total:.2f}</p>
    <p style="font-size: 20px; font-weight: bold;"><strong>Lucro Total Percentual:</strong> {lucro_reais_total_percentual * 100:.2f}%</p>
</div>

<style>
@keyframes slideIn {{
    from {{
        transform: translateY(-50%);
        opacity: 0;
    }}
    to {{
        transform: translateY(0);
        opacity: 1;
    }}
}}
</style>
"""

st.markdown(html_content, unsafe_allow_html=True)



