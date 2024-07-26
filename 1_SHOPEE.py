import streamlit as st
import pandas as pd
import sqlite3

# Título da aplicação
st.title('Base de Dados de SHOPEE')

st.divider()
preco_venda = st.number_input("PREÇO VENDA(R$)", min_value=0.00, max_value=100000.00, step=0.01, format="%.2f")
st.divider()
preco_custo = st.number_input("PREÇO CUSTO PRODUTO(R$)", min_value=0.00, max_value=100000.00, step=0.01, format="%.2f")
st.divider()
preco_COMISSAO_SHOPEE = st.number_input("COMISSÃO SHOPEE (%)", min_value=20.00, max_value=100.00, step=0.01, format="%.2f")
st.divider()
preco_custo_fixo = st.number_input("CUSTO FIXO(R$)", min_value=0.00, value=4.00, max_value=100000.00, step=0.01, format="%.2f")
st.divider()
preco_custo_frete_mercadoria = st.number_input("FRETE MERCADORIA(R$)", min_value=0.0, value=0.25, max_value=100000.00, step=0.01, format="%.2f")
st.divider()
preco_EMBALAGEM = st.number_input("PREÇO EMBALAGEM(R$)", min_value=0.00, value=0.50, max_value=100000.00, step=0.01, format="%.2f")
st.divider()
imposto_NF = st.number_input("IMPOSTO NOTA FISCAL(%)", min_value=0.00, value=4.00, max_value=100.00, step=0.01, format="%.2f")
st.divider()
OUTROS_IMPOSTOS = st.number_input("OUTROS IMPOSTOS(%)", min_value=0.00, value=0.00, max_value=100.00, step=0.01, format="%.2f")

# Cálculo do custo total do produto em reais
CUSTO_TOTAL_PRODUTO_EM_REAL = (
    preco_custo + 
    preco_custo_fixo + 
    preco_custo_frete_mercadoria + 
    preco_EMBALAGEM + 
    (preco_COMISSAO_SHOPEE / 100) * preco_venda + 
    (imposto_NF / 100) * preco_venda + 
    (OUTROS_IMPOSTOS / 100) * preco_venda
)

# Cálculo dos custos adicionais do produto em porcentagem
if preco_custo != 0:
    CUSTO_ADICIONAIS_PRODUTO_PORCENTAGEM = (CUSTO_TOTAL_PRODUTO_EM_REAL / preco_custo) * 100
else:
    CUSTO_ADICIONAIS_PRODUTO_PORCENTAGEM = 0.0

# Cálculo do lucro total em reais
LUCRO_TOTAL_EM_REAL = preco_venda - CUSTO_TOTAL_PRODUTO_EM_REAL

# Cálculo do lucro total em porcentagem
if preco_venda != 0:
    LUCRO_TOTAL_EM_PORCENTAGEM = (LUCRO_TOTAL_EM_REAL / preco_venda) * 100
else:
    LUCRO_TOTAL_EM_PORCENTAGEM = 0.0

# Determinar cor com base no valor do lucro
lucro_color = "green" if LUCRO_TOTAL_EM_REAL > 0 else "red"
percent_color = "green" if LUCRO_TOTAL_EM_PORCENTAGEM > 0 else "red"

# Template HTML para exibição dos resultados
html_content = f"""
<div style="background-color: yellow; color: black; border: 15px solid black; border-radius: 50px; padding: 20px; margin: 20px 0; box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); animation: slideIn 1s; text-align: center;">
    <h3 style="color: green; font-weight: bold; text-align: center;">Resultados</h3>
    <p style="font-size: 20px; font-weight: bold;"><strong>Custo Total do Produto (R$):</strong> R$ {CUSTO_TOTAL_PRODUTO_EM_REAL:.2f}</p>
    <p style="font-size: 20px; font-weight: bold;"><strong>Custos Adicionais do Produto (%):</strong> {CUSTO_ADICIONAIS_PRODUTO_PORCENTAGEM:.2f}%</p>
    <p style="font-size: 35px; font-weight: bold; color: {lucro_color};"><strong>Lucro Total em Reais:</strong> R$ {LUCRO_TOTAL_EM_REAL:.2f}</p>
    <p style="font-size: 35px; font-weight: bold; color: {percent_color};"><strong>Lucro Total Percentual:</strong> {LUCRO_TOTAL_EM_PORCENTAGEM:.2f}%</p>
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

# Exibir o HTML personalizado
st.markdown(html_content, unsafe_allow_html=True)
