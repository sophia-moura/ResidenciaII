import streamlit as st
import os
import base64

st.set_page_config(
    page_title='Visualizar Calendários',
    page_icon=':eyes:',
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

PASTA_PDFS = "data/calendarios"

st.markdown("""
    <div class="page-header">
        <h1>👁️ Visualizador de Calendários Acadêmicos</h1>
        <p>Selecione um dos documentos institucionais abaixo para abrir o leitor integrado.</p>
    </div>
""", unsafe_allow_html=True)


st.divider()

col_nav1, col_nav2, _ = st.columns([1, 1, 4])
with col_nav1:
    if st.button("📅 Ver Calendário", use_container_width=True):
        st.switch_page("pages/calendario.py")

with col_nav2:
    if st.button("📂 Upload de Arquivos", use_container_width=True):
        st.switch_page("pages/upload.py")

st.write("")

if os.path.exists(PASTA_PDFS):
    pdfs_salvos = [f for f in os.listdir(PASTA_PDFS) if f.endswith('.pdf')]
else:
    pdfs_salvos = []

if pdfs_salvos:
    pdf_selecionado = st.selectbox(
        "📚 Escolha o documento que deseja ler:", 
        options=pdfs_salvos,
        index=0
    )
    
    caminho_arquivo = os.path.join(PASTA_PDFS, pdf_selecionado)
    
    try:
        with open(caminho_arquivo, "rb") as f:
            bytes_pdf = f.read()
            
        base64_pdf = base64.b64encode(bytes_pdf).decode("utf-8")
        
        pdf_display = f"""
        <iframe
            src="data:application/pdf;base64,{base64_pdf}"
            width="100%"
            height="850px"
            type="application/pdf">
         </iframe>
        """
        
       
        st.markdown(f"### 📖 Lendo: {pdf_selecionado}")
        st.markdown(pdf_display, unsafe_allow_html=True)
        
    except Exception as e:
        st.error(f"Erro ao abrir o documento: {e}")
else:
    st.warning("Nenhum calendário acadêmico foi publicado no portal ainda.")