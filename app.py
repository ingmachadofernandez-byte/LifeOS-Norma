import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import time

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Norma LifeOS", page_icon="🧿", layout="wide")

# --- ESTILOS CSS (DISEÑO BLINDADO & LEGIBLE) ---
st.markdown("""
<style>
    /* Fondo claro para toda la app */
    .stApp { background-color: #F8FAFC; }
    
    /* FORZAR TEXTO NEGRO en todas partes */
    h1, h2, h3, p, div, span, label { color: #0f172a !important; }
    
    /* Estilo de las Tarjetas (Metrics) */
    div.stMetric {
        background-color: #FFFFFF !important;
        border: 1px solid #E2E8F0;
        padding: 15px;
        border-radius: 10px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    div.stMetric label { color: #64748b !important; }
    div.stMetric div { color: #0f172a !important; }
    
    /* Estilo de las Tarjetas de Sueños */
    .dream-card {
        background-color: white !important;
        padding: 20px;
        border-radius: 15px;
        border-left: 5px solid #6366F1;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        margin-bottom: 10px;
    }
    .dream-card h3 { color: #4338ca !important; font-weight: bold; }
    
    /* Estilo del Modo Zen */
    .zen-mode {
        text-align: center; padding: 50px; background-color: #E0F2F1; border-radius: 20px;
    }
    .zen-mode h1 { color: #2e7d32 !important; }
</style>
""", unsafe_allow_html=True)

# --- ESTADO DE PÁNICO (SESSION STATE) ---
if 'zen_mode' not in st.session_state:
    st.session_state['zen_mode'] = False

def activar_zen():
    st.session_state['zen_mode'] = True

def desactivar_zen():
    st.session_state['zen_mode'] = False

# --- LÓGICA DE MODO ZEN (PANTALLA LIMPIA) ---
if st.session_state['zen_mode']:
    st.markdown('<div class="zen-mode">', unsafe_allow_html=True)
    st.title("🌿 Espacio de Calma para Norma")
    st.image("https://images.unsplash.com/photo-1507525428034-b723cf961d3e?auto=format&fit=crop&w=1000&q=80", caption="Respira...")
    
    st.markdown("### 🌬️ Técnica 4-7-8")
    st.write("1. Inhala profundo (4 seg)...")
    st.write("2. Retén el aire (7 seg)...")
    st.write("3. Exhala suavemente (8 seg)...")
    
    st.divider()
    if st.button("🔙 Ya me siento mejor (Volver al LifeOS)"):
        desactivar_zen()
        st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    st.stop() 

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=80)
    st.write("## Hola, Norma 👋")
    st.caption("Gerente de Proyectos | LifeOS v1.0")
    
    selected = option_menu(
        menu_title="Navegación",
        options=["Dashboard Principal", "🏛️ Alcaldía Cali", "🚀 Numbra", "🤝 PMO Hub", "🧘‍♀️ Vida & Sueños"],
        icons=["grid", "bank", "rocket-takeoff", "people", "heart-pulse"],
        menu_icon="cast",
        default_index=0,
    )
    
    st.divider()
    if st.button("🚨 ¡ESTOY ESTRESADA!"):
        activar_zen()
        st.rerun()

# --- PÁGINA: DASHBOARD PRINCIPAL ---
if selected == "Dashboard Principal":
    st.title("🧿 Centro de Comando")
    st.markdown("Bienvenida a tu sistema, Norma.")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("🏛️ Alcaldía", "2 Oficios", "Pendientes")
    col2.metric("🚀 Numbra", "Sprint 4", "En curso")
    col3.metric("🤝 PMO Hub", "Evento", "Logística")
    col4.metric("🧘‍♀️ Energía", "ALTA", "Nivel de Calma")
    
    st.subheader("🐶 Arya (Asistente Virtual)")
    prompt = st.chat_input("Dile a Arya qué necesitas organizar hoy...")
    if prompt:
        st.success(f"✅ Arya anotó: '{prompt}'. Procesando para Norma...")

# --- PÁGINA: VIDA Y SUEÑOS ---
elif selected == "🧘‍♀️ Vida & Sueños":
    st.title("💎 Mapa de Sueños de Norma")
    
    tab1, tab2, tab3 = st.tabs(["🎓 Profesionales", "🚗 Materiales", "🧘‍♀️ Espirituales"])
    
    with tab1:
        st.subheader("Objetivos Profesionales")
        st.markdown('<div class="dream-card"><h3>🇬🇧 Bilingüismo C2</h3><p>Meta: Hablar fluido.</p></div>', unsafe_allow_html=True)
        st.checkbox("¿Practiqué 15 min hoy?", key="english")
        
    with tab2:
        st.subheader("Objetivos Materiales")
        col_a, col_b = st.columns(2)
        with col_a:
            st.markdown('<div class="dream-card"><h3>🚗 Mi Carro</h3></div>', unsafe_allow_html=True)
            st.progress(30)
        with col_b:
            st.metric("Viajes 2026", "0/4", "¡A planear!")

    with tab3:
        st.subheader("Zona de Calma")
        st.info("Si sientes que el estrés sube, usa el botón de pánico en la barra lateral.")
        if st.button("Activar Modo Zen Ahora 🌿"):
            activar_zen()
            st.rerun()