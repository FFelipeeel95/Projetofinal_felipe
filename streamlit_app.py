import streamlit as st
from google.cloud import firestore
from datetime import datetime

# --- CONFIGURAÇÃO DA PÁGINA ---
st.set_page_config(page_title="Felipe Motors | Gestão de Ativos", page_icon="🏎️", layout="wide")

# --- CONEXÃO COM FIREBASE ---
try:
    if "db" not in st.session_state:
        st.session_state.db = firestore.Client.from_service_account_json("firebase.json")
    db = st.session_state.db
except Exception as e:
    st.error(f"Conexão interrompida: {e}")
    db = None

# --- NAVEGAÇÃO LATERAL ---
st.sidebar.title("Menu de Navegação")
pagina = st.sidebar.radio("Selecione uma seção:", ["Início", "Estoque de Veículos", "Cadastrar Novo Item", "Informações do Projeto"])

# --- ESTILIZAÇÃO E TEMAS POR PÁGINA ---
if pagina == "Início":
    cor_fundo = "#0a0a0a" 
elif pagina == "Estoque de Veículos":
    cor_fundo = "#0f172a" 
elif pagina == "Cadastrar Novo Item":
    cor_fundo = "#1a1a1a" 
else:
    cor_fundo = "#111827" 

st.markdown(f"""
    <style>
    .stApp {{
        background-color: {cor_fundo};
        color: #ffffff;
    }}
    .car-card {{
        background-color: rgba(255, 255, 255, 0.05);
        padding: 25px;
        border-radius: 12px;
        border-left: 4px solid #cc0000;
        margin-bottom: 20px;
    }}
    h1, h2, h3 {{
        color: #f5f5f5;
    }}
    </style>
    """, unsafe_allow_html=True)

# --- PÁGINA: INÍCIO ---
if pagina == "Início":
    st.title("Felipe Motors – Curadoria Automotiva")
    st.image("https://images.unsplash.com/photo-1492144534655-ae79c964c9d7?auto=format&fit=crop&q=80&w=1200")
    st.markdown("""
    ### Excelência em Gestão de Veículos
    Seja bem-vindo à plataforma de controle de inventário de **Felipe**. Este sistema foi desenvolvido para oferecer uma interface técnica e simplificada na organização de veículos de alta performance. 
    
    Navegue pelas seções ao lado para consultar a disponibilidade atual ou registrar novas unidades em nossa base de dados.
    """)

# --- PÁGINA: ESTOQUE DE VEÍCULOS ---
elif pagina == "Estoque de Veículos":
    st.header("🏁 Catálogo de Ativos Disponíveis")
    
    if db:
        docs = db.collection("carros").stream()
        lista_carros = list(docs)
        
        if not lista_carros:
            st.info("No momento, o estoque encontra-se vazio.")
        
        for doc in lista_carros:
            car = doc.to_dict()
            with st.container():
                st.markdown(f"""
                    <div class="car-card">
                        <span style="font-size: 22px; font-weight: bold;">{car['marca']} {car['modelo']}</span><br>
                        <span style="color: #2ecc71; font-size: 18px;">Valor: R$ {car['preco']}</span><br>
                        <p><b>Ano:</b> {car['ano']} | <b>Potência:</b> {car.get('potencia', '---')} cv</p>
                        <p style="color: #bdc3c7;">{car['descricao']}</p>
                    </div>
                """, unsafe_allow_html=True)
                
                # CORREÇÃO DO ERRO AQUI (LINHA 91)
                if st.button(f"Remover Registro: {car['modelo']}", key=doc.id):
                    db.collection("carros").document(doc.id).delete()
                    st.success("Registro removido.")
                    st.rerun()

# --- PÁGINA: CADASTRAR NOVO ITEM ---
elif pagina == "Cadastrar Novo Item":
    st.header("📝 Registro de Patrimônio")
    with st.form("fluxo_cadastro", clear_on_submit=True):
        c1, c2 = st.columns(2)
        with c1:
            marca = st.text_input("Fabricante")
            modelo = st.text_input("Modelo")
            ano = st.number_input("Ano de Fabricação", 1900, 2026, 2025)
        with c2:
            preco = st.text_input("Preço de Avaliação")
            potencia = st.number_input("Potência Estimada (cv)", 0, 2500)
            
        descricao = st.text_area("Observações Técnicas")
        
        if st.form_submit_button("Confirmar Cadastro"):
            if marca and modelo and preco:
                dados = {
                    "marca": marca, "modelo": modelo, "ano": ano,
                    "preco": preco, "potencia": potencia, "descricao": descricao,
                    "registrado_por": "Felipe", "data": datetime.now()
                }
                db.collection("carros").add(dados)
                st.success("O registro foi processado e armazenado com sucesso.")
            else:
                st.error("Campos obrigatórios: Marca, Modelo e Preço.")

# --- PÁGINA: INFORMAÇÕES DO PROJETO ---
elif pagina == "Informações do Projeto":
    st.header("🖥️ Detalhes do Desenvolvimento")
    st.info(f"Desenvolvedor Responsável: **Felipe**")
    st.write("""
    **Instituição:** GRACE ICMC USP  
    **Tecnologias:** Este sistema utiliza Python (Streamlit) e Google Cloud Firestore.
    
    O foco deste projeto é a gestão profissional de inventário automotivo, priorizando a integridade dos dados e uma interface de usuário sóbria e eficiente.
    """)
