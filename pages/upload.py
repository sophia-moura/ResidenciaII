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

st.markdown(
    """<style>
    .page-header {
            background: linear-gradient(135deg, #011E6B 0%, #0A4FD4 100%);
            border-radius: 14px;
            padding: 22px 30px;
            margin-bottom: 18px;
            box-shadow: 0 4px 18px rgba(1,30,107,0.18);
        }
        .page-header h1 {
            color: #FFFFFF;
            font-size: 25px;
            font-weight: 700;
            margin: 0 0 3px 0;
            font-family: Arial, sans-serif;
            letter-spacing: 0.2px;
        }
        .page-header p {
            color: #A8C8F8;
            font-size: 15px;
            margin: 0;
            font-family: Arial, sans-serif;
        }
    """, unsafe_allow_html=True)

DB_NAME = "data/dados.db"
PASTA_PDFS = "data/calendarios"

# Garante que a pasta 'data' existe para salvar o banco e o PDF
os.makedirs("data", exist_ok=True)
os.makedirs("data/calendarios", exist_ok=True)

def iniciar_banco():
    """Cria a conexão com o banco de dados SQLite."""
    conn = sqlite3.connect(DB_NAME)
    return conn

def criar_tabela_se_nao_existir(df_exemplo, conn):
    """Cria a estrutura da tabela com base no DataFrame caso seja a primeira execução."""
    df_exemplo.head(0).to_sql("atendimentos", conn, if_exists="append", index=False)
    
    # try:
    #     cursor = conn.cursor()
    #     cursor.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_atendimento ON atendimentos (Atendimento);")
    #     conn.commit()
    # except Exception:
    #     pass

st.markdown("""
            <div class="page-header">
                <h1>📂 Central de Upload - Portal Atende</h1>
                <p>Use esta página para atualizar a base de dados do sistema e o calendário acadêmico.</p>
            </div>
""", unsafe_allow_html=True)


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
            
        st.success(f"Arquivo '{arquivo_dados.name}' carregado. Total de linhas para análise: {len(df)}")
        
        # Mostra uma prévia dos dados para o usuário validar visualmente
        st.dataframe(df.head(3), use_container_width=True)
        
        
        if st.button("🔄 Iniciar Análise e Integração de Dados", type="primary"):
            with st.spinner("Analisando e atualizando a base de dados... Por favor, aguarde..."):
                
                # Tratamento de datas antes de salvar no banco
                for col in ['Abertura', 'Fechamento', 'Prazo limite final']:
                    if col in df.columns:
                        df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
                        df[col] = df[col].dt.strftime('%Y-%m-%d %H:%M:%S').fillna('N/A')
                
                colunas_datas = [c for c in ['Abertura', 'Fechamento', 'Prazo limite final'] if c in df.columns]
                colunas_texto = df.columns.difference(colunas_datas)
                df[colunas_texto] = df[colunas_texto].fillna('N/A')
                
                df['Atendimento'] = df['Atendimento'].astype(str)

                conn = iniciar_banco()
                criar_tabela_se_nao_existir(df, conn)
                cursor = conn.cursor()
                
                cont_novos = 0
                cont_atualizados = 0

                for _, row in df.iterrows():
                    num_atendimento = row['Atendimento']
                    
                    # Verifica se esse número de atendimento já existe no SQLite
                    cursor.execute("SELECT COUNT(*) FROM atendimentos WHERE Atendimento = ?;", (num_atendimento,))
                    existe = cursor.fetchone()[0] > 0
                    
                    colunas = list(row.index)
                    valores = [str(v) for v in row.values]
                    
                    if not existe:
                        colunas_com_escape = [f'"{col}"' for col in colunas]
                        placeholders = ", ".join(["?"] * len(colunas))
                        sql_insert = f"INSERT INTO atendimentos ({', '.join(colunas_com_escape)}) VALUES ({placeholders});"
                        cursor.execute(sql_insert, valores)
                        cont_novos += 1
                    else:
                        set_clause = ", ".join([f'"{col}" = ?' for col in colunas if col != 'Atendimento'])
                        valores_update = [str(row[col]) for col in colunas if col != 'Atendimento']
                        valores_update.append(num_atendimento)
                        
                        sql_update = f"UPDATE atendimentos SET {set_clause} WHERE Atendimento = ?;"
                        cursor.execute(sql_update, valores_update)
                        cont_atualizados += 1
                
                conn.commit()
                conn.close()
                
                time.sleep(2)
                st.toast('Configurações salvas com sucesso!', icon='💾')
                st.success("🔥 Processamento Concluído!")
                st.write(f"✨ **Novos chamados cadastrados:** {cont_novos}")
                st.write(f"🔄 **Chamados atualizados com novos dados:** {cont_atualizados}")

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")

st.divider()

#ABA 2: Upload do Calendário Acadêmico em PDF 
#Em fase de testes
st.subheader("📅 Upload do Calendário Acadêmico")

pdfs_salvos = [f for f in os.listdir(PASTA_PDFS) if f.endswith('.pdf')]

if "pdf_visualizado" not in st.session_state:
    st.session_state.pdf_visualizado = None

if pdfs_salvos:
    st.caption("📂 Calendários atualmente cadastrados no sistema:")
    for pdf in pdfs_salvos:
        caminho_arquivo = os.path.join(PASTA_PDFS, pdf)
        with open(caminho_arquivo, "rb") as f:
            bytes_pdf = f.read()
            
        col_nome,  col_download = st.columns([4, 1], vertical_alignment="center")
        col_nome.markdown(f"📄 **{pdf}**")

        col_download.download_button(
            label="⬇️ Baixar",
            data=bytes_pdf,
            file_name=pdf,
            mime="application/pdf",
            key=f"btn_upload_{pdf}"
        )
        
else:
    st.warning("Nenhum calendário acadêmico cadastrado até o momento.")

st.caption("---")
st.caption("🔹 Fazer upload de um novo calendário institucional:")

arquivo_pdf = st.file_uploader(
    label="Selecione o calendário acadêmico em formato PDF", 
    type=["pdf"],
    key="uploader_pdf"
)

if arquivo_pdf is not None:
    if st.button("📁 Salvar PDF de Calendário Acadêmico", type="primary"):
        with st.spinner("Salvando documento..."):

            caminho_salvar = os.path.join(PASTA_PDFS, arquivo_pdf.name)
            
            with open(caminho_salvar, "wb") as f:
                f.write(arquivo_pdf.getbuffer())
                
            st.success(f"📄 O Calendário '{arquivo_pdf.name}' foi adicionado com sucesso!")
            st.rerun()
