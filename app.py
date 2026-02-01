import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import PyPDF2
import pandas as pd  # La herramienta para las tablas

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
    /* Estilo para que la tabla se vea profesional */
    .stDataFrame { border: 1px solid #E2E8F0; border-radius: 10px; overflow: hidden; }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=80)
    st.write("## Hola, Norma 👋")
    
    selected = option_menu(
        menu_title="Menú Principal",
        # ¡Agregamos el módulo MIRA!
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

    # 1. BASE DE DATOS TEMPORAL (Para que veas el ejemplo)
    if 'mira_data' not in st.session_state:
        st.session_state['mira_data'] = [
            {"Actividad": "Reunión de Líderes", "Responsable": "Norma", "Estado": "Pendiente", "Avance": 0},
            {"Actividad": "Visita Comuna 12", "Responsable": "Equipo", "Estado": "En Proceso", "Avance": 50},
            {"Actividad": "Capacitación Electoral", "Responsable": "Norma", "Estado": "Listo", "Avance": 100},
        ]

    # Crear la tabla editable
    df = pd.DataFrame(st.session_state['mira_data'])

    st.subheader("📋 Lista de Tareas y Compromisos")
    
    # Aquí configuramos la tabla para que tenga barras de progreso
    edited_df = st.data_editor(
        df,
        num_rows="dynamic", # ¡Permite agregar filas nuevas!
        column_config={
            "Avance": st.column_config.ProgressColumn(
                "Progreso %",
                help="Nivel de cumplimiento",
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

    # Métricas automáticas (calculadas de tu tabla)
    total = len(edited_df)
    completadas = len(edited_df[edited_df["Estado"] == "Listo"])
    progreso_total = (completadas / total) if total > 0 else 0

    st.divider()
    col1, col2 = st.columns([3, 1])
    col1.write("### Progreso General del Partido")
    col1.progress(progreso_total, text=f"Cumplimiento Global: {int(progreso_total*100)}%")
    col2.metric("Tareas Realizadas", f"{completadas}/{total}")

elif selected == "🧠 Inteligencia Doc":
    st.title("🧠 Analizador de Documentos")
    uploaded_file = st.file_uploader("Sube contratos o decretos (PDF)", type="pdf")
    
    if uploaded_file is not None:
        reader = PyPDF2.PdfReader(uploaded_file)
        text = ""
        for page in reader.pages: text += page.extract_text()
        st.success(f"✅ Procesado: {len(reader.pages)} páginas.")
        
        search = st.text_input("🔍 Buscar palabra clave:")
        if search:
            count = text.lower().count(search.lower())
            if count > 0: st.info(f"Encontré '{search}' {count} veces.")
            else: st.warning("No encontrado.")
            
        with st.expander("Ver texto completo"): st.write(text)

elif selected == "💎 Sueños":
    st.title("💎 Mapa de Sueños")
    st.write("Tus metas personales...")