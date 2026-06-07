import pandas as pd
import streamlit as st
import sqlite3
import os
import time

st.set_page_config(
    page_title='Upload de Solicitações',
    page_icon=':inbox_tray:',
    layout='wide'
)

DB_NAME = "data/dados.db"

# Garante que a pasta 'data' existe para salvar o banco e o PDF
os.makedirs("data", exist_ok=True)

def iniciar_banco():
    """Cria a conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(DB_NAME)
    return conn


st.title("📂 Central de Upload - Portal Atende")
st.markdown("Use esta página para atualizar a base de dados do sistema e o calendário acadêmico.")


col_nav1, col_nav2, _ = st.columns([1, 1, 4])
with col_nav1:
    if st.button("← Voltar", use_container_width=True):
        st.switch_page("index.py")
with col_nav2:
    if st.button("📅 Ver Calendário", use_container_width=True):
        st.switch_page("pages/calendario.py")

st.divider()

#ABA 1: Upload de Atendimentos em EXCEL / CSV
st.subheader("📊 Atualizar Banco de Dados de Atendimentos")
st.caption("Selecione o novo relatório extraído (.csv ou .xlsx) para atualizar o dashboard.")

arquivo_dados = st.file_uploader(
    label="Arraste ou selecione o arquivo de atendimentos", 
    type=["csv", "xlsx"],
    help="Formatos aceitos pelo sistema: .xlsx e .csv",
    key="uploader_dados"
)

if arquivo_dados is not None:
    try:
        
        if arquivo_dados.name.endswith('.csv'):
            df = pd.read_csv(arquivo_dados, encoding='latin1', sep=';')
        else:
            df = pd.read_excel(arquivo_dados)
            
        st.success(f"Arquivo '{arquivo_dados.name}' carregado com sucesso pelo Pandas!")
        
        # Mostra uma prévia dos dados para o usuário validar visualmente
        st.dataframe(df.head(3), use_container_width=True)
        
        
        if st.button("Confirmar e Salvar no Banco de Dados", type="primary"):
            with st.spinner("Salvando dados no SQLite..."):
                
                # Tratamento de datas antes de salvar no banco
                for col in ['Abertura', 'Fechamento', 'Prazo Limite']:
                    if col in df.columns:
                        df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
                
                
                colunas_datas = [c for c in ['Abertura', 'Fechamento', 'Prazo Limite'] if c in df.columns]
                colunas_texto = df.columns.difference(colunas_datas)
                df[colunas_texto] = df[colunas_texto].fillna('N/A')
                
                
                conn = iniciar_banco()
                
                # 'if_exists="replace"' apaga a tabela antiga e cria a nova com os dados frescos
                df.to_sql("atendimentos", conn, if_exists="replace", index=False)
                conn.close()
                
                time.sleep(2)
                st.toast('Configurações salvas com sucesso!', icon='💾')
                st.success("🔥 Sucesso! O banco de dados SQLite foi atualizado e está pronto para o uso.")
                
    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")

st.divider()

#ABA 2: Upload do Calendário Acadêmico em PDF 
#Em fase de testes
st.subheader("📅 Upload do Calendário Acadêmico")
st.caption("Substitua o arquivo PDF do calendário institucional vigente.")

arquivo_pdf = st.file_uploader(
    "Selecione o calendário acadêmico em formato PDF", 
    type=["pdf"],
    key="uploader_pdf"
)

if arquivo_pdf is not None:
    if st.button("Substituir PDF do Calendário"):
        with st.spinner("Salvando documento..."):

            caminho_salvar = os.path.join("data", "calendario_academico.pdf")
            
            with open(caminho_salvar, "wb") as f:
                f.write(arquivo_pdf.getbuffer())
                
            st.success("📄 Calendário Acadêmico em PDF atualizado com sucesso na pasta do sistema!")