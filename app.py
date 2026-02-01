import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import PyPDF2
import pandas as pd # Necesitamos esto para las tablas bonitas

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
    .stDataFrame { border: 1px solid #E2E8F0; border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=80)
    st.write("## Hola, Norma 👋")
    
    selected = option_menu(
        menu_title="Menú Principal",
        # ¡Agregamos MIRA a la lista! 💙
        options=["Dashboard", "💙 MIRA", "🧠 Inteligencia Doc", "🏛️ Alcaldía", "🚀 Numbra", "💎 Sueños"],
        icons=["grid", "people-fill", "file-earmark-text", "bank", "rocket-takeoff", "gem"],
        default_index=1, 
    )
    
    st.divider()
    st.info("Versión 3.0 - Módulo Político")

# --- LÓGICA PRINCIPAL ---
if selected == "Dashboard":
    st.title("🧿 Centro de Comando")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pendientes MIRA", "3", "Activos")
    col2.metric("Numbra", "Fase 2", "En Proceso")
    col3.metric("Docs Leídos", "1", "Hoy")
    col4.metric("Energía", "⚡️ Alta", "Estable")

elif selected == "💙 MIRA":
    st.title("💙 Gestión Política - MIRA")
    st.markdown("Control de actividades y compromiso social.")

    # 1. VISIÓN GENERAL (Métricas arriba)
    # Inicializamos las tareas si no existen en la memoria temporal
    if 'mira_data' not in st.session_state:
        st.session_state['mira_data'] = [
            {"Actividad": "Reunión de Líderes", "Responsable": "Norma", "Estado": "Pendiente", "Avance": 0},
            {"Actividad": "Visita Comuna 12", "Responsable": "Equipo", "Estado": "En Proceso", "Avance": 50},
            {"Actividad": "Capacitación Electoral", "Responsable": "Norma", "Estado": "Listo", "Avance": 100},
        ]

    # Convertimos la lista en una tabla (DataFrame)
    df = pd.DataFrame(st.session_state['mira_data'])

    # Editor de Datos (Aquí es donde ocurre la magia)
    st.subheader("📋 Lista de Tareas y Compromisos")
    edited_df = st.data_editor(
        df,
        num_rows="dynamic", # ¡Esto te permite agregar filas nuevas!
        column_config={
            "Avance": st.column_config.ProgressColumn(
                "Progreso %",
                help="¿Cuánto hemos avanzado?",
                min_value=0,
                max_value=100,
                format="%d%%",
            ),
            "Estado": st.column_config.SelectboxColumn(
                "Estado Actual",
                options=["Pendiente", "En Proceso", "Bloqueado", "Listo"],
                required=True,
            )
        },
        use_container_width=True,
        hide_index=True,
    )

    # Cálculo de métricas automáticas
    total_tareas = len(edited_df)
    tareas_listas = len(edited_df[edited_df["Estado"] == "Listo"])
    porcentaje_global = (tareas_listas / total_tareas) if total_tareas > 0 else 0

    st.divider()
    col1, col2 = st.columns([3, 1])
    col1.write("### Progreso General del Partido")
    col1.progress(porcentaje_global, text=f"Cumplimiento: {int(porcentaje_global*100)}%")
    
    col2.metric("Tareas Completadas", f"{tareas_listas}/{total_tareas}")

elif selected == "🧠 Inteligencia Doc":
    st.title("🧠 Analizador de Documentos")
    uploaded_file = st.file_uploader("Sube contratos o decretos (PDF)", type="pdf")
    
    if uploaded_file is not None:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages: text += page.extract_text()
        st.success(f"✅ Documento de {len(reader.pages)} páginas procesado.")
        
        search = st.text_input("🔍 Buscar en el documento:")
        if search:
            count = text.lower().count(search.lower())
            if count > 0: st.info(f"Encontré la palabra '{search}' {count} veces.")
            else: st.warning("No encontré esa palabra.")
        with st.expander("Ver texto completo"): st.write(text)

elif selected == "🏛️ Alcaldía":
    st.title("🏛️ Alcaldía de Cali")
    st.write("Próximamente: Tablero de control de Calidad...")

elif selected == "🚀 Numbra":
    st.title("🚀 Proyecto Numbra")
    st.write("Próximamente: Calculadora financiera...")

elif selected == "💎 Sueños":
    st.title("💎 Mapa de Sueños")
    st.write("Inglés • Viajes • Carro")