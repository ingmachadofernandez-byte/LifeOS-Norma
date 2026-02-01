import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import PyPDF2

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Norma LifeOS", page_icon="🧿", layout="wide")

# --- ESTILOS CSS ---
st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    h1, h2, h3, p, div, span, label, li { color: #0f172a !important; }
    div.stMetric {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        padding: 15px; border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    div.stMetric label { color: #64748b !important; }
    .stFileUploader {
        padding: 20px; border: 2px dashed #6366F1; border-radius: 10px; background-color: #EEF2FF;
    }
    .zen-mode { text-align: center; padding: 50px; background-color: #E0F2F1; border-radius: 20px; }
    .zen-mode h1 { color: #2e7d32 !important; }
</style>
""", unsafe_allow_html=True)

# --- MODO ZEN ---
if 'zen_mode' not in st.session_state: st.session_state['zen_mode'] = False
def activar_zen(): st.session_state['zen_mode'] = True
def desactivar_zen(): st.session_state['zen_mode'] = False

if st.session_state['zen_mode']:
    st.markdown('<div class="zen-mode">', unsafe_allow_html=True)
    st.title("🌿 Espacio de Calma")
    st.image("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1000&q=80")
    st.write("Inhala (4)... Retén (7)... Exhala (8)...")
    st.divider()
    if st.button("🔙 Volver al LifeOS"):
        desactivar_zen()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop()

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=80)
    st.write("## Hola, Norma 👋")
    
    selected = option_menu(
        menu_title="Menú Principal",
        options=["Dashboard", "🧠 Inteligencia Doc", "🏛️ Alcaldía", "🚀 Numbra", "💎 Sueños"],
        icons=["grid", "file-earmark-text", "bank", "rocket-takeoff", "gem"],
        default_index=1,  # Hice que arranque directo en Inteligencia
    )
    
    st.divider()
    # CORRECCIÓN AQUÍ: El rerun solo ocurre si se presiona el botón
    if st.button("🚨 PÁNICO / ZEN"): 
        activar_zen()
        st.rerun()

# --- LÓGICA PRINCIPAL ---
if selected == "Dashboard":
    st.title("🧿 Centro de Comando")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pendientes", "2", "Urgentes")
    col2.metric("Numbra", "Fase 2", "En Proceso")
    col3.metric("Docs Leídos", "0", "Hoy")
    col4.metric("Energía", "⚡️ Alta", "Estable")
    st.info("💡 Tip de Arya: Tienes pendiente revisar el contrato de Numbra.")

elif selected == "🧠 Inteligencia Doc":
    st.title("🧠 Analizador de Documentos")
    st.markdown("### Sube tu documento abajo 👇")
    st.markdown("Arya leerá el contenido y buscará lo que necesites.")
    
    uploaded_file = st.file_uploader("Arrastra tu PDF aquí", type="pdf")
    
    if uploaded_file is not None:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages:
            text += page.extract_text()
            
        st.success(f"✅ Documento procesado: {len(reader.pages)} páginas leídas.")
        
        search = st.text_input("🔍 ¿Qué buscas? (Ej: 'presupuesto', 'plazo')")
        if search:
            count = text.lower().count(search.lower())
            if count > 0:
                st.markdown(f"### 🚨 ¡Encontrado!")
                st.write(f"La palabra **'{search}'** aparece **{count} veces**.")
            else:
                st.warning(f"No encontré la palabra '{search}'.")
        
        with st.expander("Ver texto completo"):
            st.write(text)

elif selected == "💎 Sueños":
    st.title("💎 Mapa de Sueños")
    st.write("Aquí van tus metas...")