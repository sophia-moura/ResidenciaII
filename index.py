import pandas as pd
import streamlit as st

st.set_page_config(page_title='Portal - Atende',
                   page_icon=':bar_chart:',
                   layout='centered')

st.markdown("""
    <style>
        /* Altera o fundo do app para o azul escuro da UCB */
        .stApp {
            background-color: #022A89;
        }
        
        /* Estilização para o texto da universidade */
        .titulo-universidade {
            color: #FFFFFF;
            text-align: center;
            font-size: 32px !important;
            font-weight: bold;
            margin-top: 15px !important;
            margin-bottom: 15px;
            font-family: Arial, sans-serif;
        }
        
        /*Estilização do botão*/ 
        div[data-testid="stPageLink"]{
            display: flex !important;
            justify-content: center !important;
        }
            
        div[data-testid="stPageLink"] a {
            padding: 10px 30px;
            background-color: #FFFFFF;
            color: #022A89;
            font-family: Arial;
            font-size: 30px !important;
            border-radius: 5px;
            transition: transform 0.2s, background-color 0.2s;
        }
                
        div[data-testid="stPageLink"] a:hover {
            transform: scale(1.05);
            background-color: #E0E0E0;
        }
        
    </style>
    """,
unsafe_allow_html=True)

col1, col2, col3 = st.columns([1,2,1], vertical_alignment="center")
with col2:
    st.image('assets/logo.png', width=400)
    st.markdown("<p class='titulo-universidade'>Universidade Catolica de Brasília</p>", unsafe_allow_html=True)
    st.page_link("pages/calendario.py", label="Entrar no Portal - Atende")