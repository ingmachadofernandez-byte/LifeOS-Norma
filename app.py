import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
from datetime import date, datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURACIÓN ---
st.set_page_config(page_title="Norma OS", page_icon="🧿", layout="wide")

# --- 2. ESTILOS ---
st.markdown("""
<style>
    .stApp { background-color: #F0F9FF; }
    h1, h2, h3, h4, h5, p, span, label, div { color: #1E3A8A !important; font-family: 'Helvetica Neue', sans-serif; }
    div.stMetric, div.stDataFrame, .css-1r6slb0 {
        background-color: #FFFFFF !important; border: 1px solid #DBEAFE;
        border-radius: 15px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    section[data-testid="stSidebar"] { background-color: #EFF6FF; border-right: 1px solid #BFDBFE; }
    .stButton>button { background-color: #3B82F6; color: white !important; border-radius: 10px; border: none; font-weight: bold; padding: 10px 20px; }
    .stButton>button:hover { background-color: #2563EB; }
    .alerta-roja {
        padding: 15px; background-color: #FEF2F2; color: #991B1B !important;
        border: 1px solid #FCA5A5; border-radius: 12px; margin-bottom: 20px; font-weight: bold; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CONEXIÓN ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 4. FUNCIONES MAESTRAS ---
def cargar_datos(hoja, columnas=5):
    try:
        df = conn.read(worksheet=hoja, usecols=list(range(columnas)), ttl=0)
        # Limpieza General de Fechas
        if 'Fecha' in df.columns:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
        if 'Fecha_Entrega' in df.columns:
            df['Fecha_Entrega'] = pd.to_datetime(df['Fecha_Entrega'], errors='coerce')
        
        # Limpieza Específica Finanzas
        if hoja == "FINANZAS" and not df.empty:
            df['Monto'] = pd.to_numeric(df['Monto'], errors='coerce').fillna(0)
            df['Pagado'] = df['Pagado'].astype(str).map({'TRUE': True, 'FALSE': False, 'True': True, 'False': False, '1': True, '0': False}).fillna(False)
            
        return df
    except Exception:
        return pd.DataFrame()

def guardar_datos(hoja, df):
    try:
        conn.update(worksheet=hoja, data=df)
        st.success("✅ ¡Guardado exitosamente!")
        st.rerun()
    except Exception as e:
        st.error(f"Error al guardar: {e}")

# --- 5. MENÚ LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=100)
    st.write("### Hola, Norma 👋")
    
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "💰 Finanzas", "🚀 Numbra", "🏆 PMO Hub", "🏛️ Alcaldía", "💪 Bienestar", "✨ Sueños", "📝 Notas", "💙 MIRA", "🧠 Estudio"],
        icons=["grid", "cash-coin", "rocket-takeoff", "trophy", "bank", "heart-pulse", "stars", "journal-text", "people-fill", "book"],
        default_index=0,
    )

# ================= MÓDULOS DEL SISTEMA =================

# --- DASHBOARD ---
if selected == "Dashboard":
    st.title("🧿 Tu Día Brillante")
    hoy = date.today()
    dias_esp = {"Monday":"Lunes", "Tuesday":"Martes", "Wednesday":"Miércoles", "Thursday":"Jueves", "Friday":"Viernes", "Saturday":"Sábado", "Sunday":"Domingo"}
    hoy_es = dias_esp.get(hoy.strftime("%A"), "Hoy")
    st.markdown(f"#### 📅 {hoy_es}, {hoy.day}")

    # Alerta Inglés
    df_h = cargar_datos("HABITOS", 6)
    hecho = False
    if not df_h.empty:
        reg = df_h[df_h['Fecha'].dt.date == hoy]
        if not reg.empty and reg.iloc[0]['Min_Ingles'] > 0: hecho = True
    if not hecho: st.markdown('<div class="alerta-roja">🚨 ¡Alerta! Inglés pendiente 🇬🇧</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    rutina = {"Lunes": "Pierna 🍑", "Martes": "Cardio 🔥", "Miércoles": "Espalda 💪", "Jueves": "Pierna", "Viernes": "Full Body", "Domingo": "Relax"}
    c1.metric("🏋️‍♀️ Gym", rutina.get(hoy_es, "Descanso"))
    
    df_fin = cargar_datos("FINANZAS", 5)
    saldo = 0
    if not df_fin.empty:
        saldo = df_fin[df_fin['Tipo']=='Ingreso']['Monto'].sum() - df_fin[df_fin['Tipo']=='Gasto']['Monto'].sum()
    c2.metric("💰 Disponible", f"${saldo:,.0f}")
    
    # Contador Numbra
    df_numbra = cargar_datos("NUMBRA_TAREAS", 5)
    tareas_pend = len(df_numbra[df_numbra['Estado'] != 'Listo']) if not df_numbra.empty else 0
    c3.metric("🚀 Numbra Pendientes", f"{tareas_pend} Tareas")

# --- 🚀 NUMBRA (GESTOR DE TAREAS) ---
elif selected == "🚀 Numbra":
    st.title("🚀 Gestor de Proyectos Numbra")
    df_numbra = cargar_datos("NUMBRA_TAREAS", 5)
    
    if not df_numbra.empty:
        col1, col2, col3 = st.columns(3)
        pendientes = df_numbra[df_numbra['Estado'] == 'Pendiente']
        arya = df_numbra[df_numbra['Estado'] == 'Arya Trabajando']
        listo = df_numbra[df_numbra['Estado'] == 'Listo']
        col1.warning(f"📌 Pendientes ({len(pendientes)})")
        col2.info(f"🤖 Arya Trabajando ({len(arya)})")
        col3.success(f"✅ Listas ({len(listo)})")
        st.divider()

    tab1, tab2 = st.tabs(["📋 Lista de Tareas", "➕ Nueva Tarea"])
    with tab1:
        if not df_numbra.empty:
            edited_numbra = st.data_editor(
                df_numbra, num_rows="dynamic", use_container_width=True,
                column_config={
                    "Prioridad": st.column_config.SelectboxColumn("Prioridad", options=["Alta 🔥", "Media", "Baja"]),
                    "Estado": st.column_config.SelectboxColumn("Estado", options=["Pendiente", "En Proceso", "Arya Trabajando", "Listo"]),
                    "Solicitud_Arya": st.column_config.TextColumn("Instrucción para Arya", width="large")
                }
            )
            if st.button("💾 Actualizar Numbra"): guardar_datos("NUMBRA_TAREAS", edited_numbra)
        else: st.info("No hay tareas aún.")

    with tab2:
        with st.form("numbra_form"):
            c1, c2 = st.columns(2)
            n_tarea = c1.text_input("Nombre de la Tarea")
            n_prio = c2.selectbox("Prioridad", ["Alta 🔥", "Media", "Baja"])
            n_instruccion = st.text_area("¿Qué debe hacer Arya?", placeholder="Ej: Redactar correo...")
            if st.form_submit_button("Crear Tarea"):
                nuevo = pd.DataFrame([{"Fecha": str(date.today()), "Tarea": n_tarea, "Prioridad": n_prio, "Estado": "Pendiente", "Solicitud_Arya": n_instruccion}])
                guardar_datos("NUMBRA_TAREAS", pd.concat([df_numbra, nuevo], ignore_index=True))

# --- 🏆 PMO HUB (ACTUALIZADO CON TAREAS) ---
elif selected == "🏆 PMO Hub":
    st.title("🏆 PMO Hub LATAM")
    st.markdown("##### **Proyecto:** Reconocimiento Voluntarios y Miembros | **Feb - Dic 2025**")
    
    # AHORA SON 4 PESTAÑAS
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Tablero", "👥 Equipo", "✅ Actividades", "📅 Roadmap"])

    # PESTAÑA 1: DASHBOARD
    with tab1:
        df_vol = cargar_datos("PMO_VOLUNTARIOS", 4)
        if df_vol.empty: df_vol = pd.DataFrame(columns=["Nombre", "Rol", "Estado", "Puntos"])
        
        # Cargamos tareas para las métricas
        df_tareas = cargar_datos("PMO_ACTIVIDADES", 5)

        total_v = len(df_vol)
        tareas_pendientes = len(df_tareas[df_tareas['Estado'] != 'Completado']) if not df_tareas.empty else 0
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Total Voluntarios", total_v)
        c2.metric("Tareas Pendientes", tareas_pendientes, delta_color="inverse")
        c3.metric("Próximo Hito", "Marzo (Convocatoria)")
        
        st.divider()
        st.info("🤖 **Arya PMO:** Hola Norma. Si asignas tareas hoy, recuerda poner fechas realistas.")

    # PESTAÑA 2: GESTIÓN VOLUNTARIOS
    with tab2:
        st.subheader("👥 Base de Datos del Equipo")
        with st.expander("➕ Agregar Nuevo Voluntario"):
            with st.form("nuevo_voluntario"):
                col_a, col_b = st.columns(2)
                nombre = col_a.text_input("Nombre Completo")
                rol = col_b.selectbox("Rol", ["Logística", "Comunicaciones", "Jurado", "Patrocinio", "General"])
                col_c, col_d = st.columns(2)
                estado = col_c.selectbox("Estado", ["Activo", "Pendiente", "Inactivo"])
                puntos = col_d.number_input("Puntos Iniciales", value=0)
                if st.form_submit_button("Guardar Voluntario"):
                    nuevo_v = pd.DataFrame([{"Nombre": nombre, "Rol": rol, "Estado": estado, "Puntos": puntos}])
                    df_actual = cargar_datos("PMO_VOLUNTARIOS", 4)
                    if df_actual.empty: df_actual = pd.DataFrame(columns=["Nombre", "Rol", "Estado", "Puntos"])
                    guardar_datos("PMO_VOLUNTARIOS", pd.concat([df_actual, nuevo_v], ignore_index=True))

        df_vol = cargar_datos("PMO_VOLUNTARIOS", 4)
        if df_vol.empty: df_vol = pd.DataFrame(columns=["Nombre", "Rol", "Estado",