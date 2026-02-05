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

# --- 4. MENÚ ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=100)
    st.write("### Hola, Norma 👋")
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "💰 Finanzas", "🚀 Numbra", " PMO HUB ", "🏛️ Alcaldía", "💪 Bienestar", "✨ Sueños", "📝 Notas", "💙 MIRA", "🧠 Estudio"],
        icons=["grid", "cash-coin", "rocket-takeoff", "bank", "heart-pulse", "stars", "journal-text", "people-fill", "book"],
        default_index=0,
    )

# --- 5. FUNCIONES MAESTRAS (AQUÍ ESTÁ EL ARREGLO) ---
def cargar_datos(hoja, columnas=5):
    try:
        df = conn.read(worksheet=hoja, usecols=list(range(columnas)), ttl=0)
        
        # LIMPIEZA FINANZAS
        if hoja == "FINANZAS" and not df.empty:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            df['Monto'] = pd.to_numeric(df['Monto'], errors='coerce').fillna(0)
            df['Pagado'] = df['Pagado'].astype(str).map({'TRUE': True, 'FALSE': False, 'True': True, 'False': False, '1': True, '0': False}).fillna(False)
        
        # LIMPIEZA ALCALDÍA (¡ESTO ARREGLA EL ERROR ROJO!) 🚨
        if hoja == "ALCALDIA" and not df.empty:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            
        return df
    except:
        return pd.DataFrame()

def guardar_datos(hoja, df):
    try:
        conn.update(worksheet=hoja, data=df)
        st.success("✅ ¡Guardado!")
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")

# ================= MÓDULOS =================

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
        reg = df_h[df_h['Fecha'].astype(str) == str(hoy)]
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
    
    # KANBAN
    if not df_numbra.empty:
        col1, col2, col3 = st.columns(3)
        pendientes = df_numbra[df_numbra['Estado'] == 'Pendiente']
        arya = df_numbra[df_numbra['Estado'] == 'Arya Trabajando']
        listo = df_numbra[df_numbra['Estado'] == 'Listo']
        
        col1.warning(f"📌 Pendientes ({len(pendientes)})")
        col2.info(f"🤖 Arya Trabajando ({len(arya)})")
        col3.success(f"✅ Listas ({len(listo)})")
        st.divider()

    # GESTIÓN
    tab1, tab2 = st.tabs(["📋 Lista de Tareas", "➕ Nueva Tarea"])
    
    with tab1:
        if not df_numbra.empty:
            edited_numbra = st.data_editor(
                df_numbra,
                num_rows="dynamic",
                use_container_width=True,
                column_config={
                    "Prioridad": st.column_config.SelectboxColumn("Prioridad", options=["Alta 🔥", "Media", "Baja"]),
                    "Estado": st.column_config.SelectboxColumn("Estado", options=["Pendiente", "En Proceso", "Arya Trabajando", "Listo"]),
                    "Solicitud_Arya": st.column_config.TextColumn("Instrucción para Arya", width="large")
                }
            )
            if st.button("💾 Actualizar Numbra"):
                guardar_datos("NUMBRA_TAREAS", edited_numbra)
        else:
            st.info("No hay tareas aún. Crea la primera en la otra pestaña.")

    with tab2:
        with st.form("numbra_form"):
            c1, c2 = st.columns(2)
            n_tarea = c1.text_input("Nombre de la Tarea")
            n_prio = c2.selectbox("Prioridad", ["Alta 🔥", "Media", "Baja"])
            n_instruccion = st.text_area("¿Qué debe hacer Arya?", placeholder="Ej: Redactar correo...")
            
            if st.form_submit_button("Crear Tarea"):
                nuevo = pd.DataFrame([{
                    "Fecha": str(date.today()),
                    "Tarea": n_tarea,
                    "Prioridad": n_prio,
                    "Estado": "Pendiente",
                    "Solicitud_Arya": n_instruccion
                }])
                guardar_datos("NUMBRA_TAREAS", pd.concat([df_numbra, nuevo], ignore_index=True))

# --- FINANZAS ---
elif selected == "💰 Finanzas":
    st.title("💰 Finanzas")
    df_fin = cargar_datos("FINANZAS", 5)
    if not df_fin.empty:
        ing = df_fin[df_fin['Tipo']=='Ingreso']['Monto'].sum()
        gas = df_fin[df_fin['Tipo']=='Gasto']['Monto'].sum()
        c1, c2, c3 = st.columns(3)
        c1.metric("Ingresos", f"${ing:,.0f}")
        c2.metric("Gastos", f"${gas:,.0f}")
        c3.metric("Saldo", f"${(ing-gas):,.0f}")
        
    with st.expander("➕ Registrar", expanded=True):
        with st.form("fin"):
            c1, c2, c3, c4 = st.columns(4)
            tipo = c1.selectbox("Tipo", ["Gasto", "Ingreso"])
            f = c2.date_input("Fecha", date.today())
            m = c3.number_input("Monto", step=1000)
            c = c4.text_input("Concepto")
            p = st.checkbox("Pagado", True)
            if st.form_submit_button("Guardar"):
                n = pd.DataFrame([{"Fecha": f, "Concepto": c, "Monto": m, "Tipo": tipo, "Pagado": p}])
                guardar_datos("FINANZAS", pd.concat([df_fin, n], ignore_index=True))
    if not df_fin.empty: st.data_editor(df_fin, num_rows="dynamic", use_container_width=True, column_config={"Fecha": st.column_config.DateColumn("Fecha"), "Monto": st.column_config.NumberColumn("Monto", format="$%d"), "Pagado": st.column_config.CheckboxColumn("Pagado")})

# --- BIENESTAR ---
elif selected == "💪 Bienestar":
    st.title("💪 Salud")
    with st.expander("➕ Registro Diario", expanded=True):
        with st.form("hab"):
            c1, c2 = st.columns(2)
            f = c1.date_input("Fecha", date.today())
            gym = c2.selectbox("Gym", ["Pierna", "Brazo", "Cardio", "Descanso"])
            c3, c4, c5 = st.columns(3)
            lec = c3.number_input("Lectura", step=5)
            bib = c4.number_input("Biblia", step=5)
            ing = c5.number_input("Inglés", step=15)
            ag = st.slider("Agua", 0.0, 4.0, 1.5)
            if st.form_submit_button("Guardar"):
                n = pd.DataFrame([{"Fecha": f, "Enfoque_Gym": gym, "Min_Lectura": lec, "Min_Biblia": bib, "Min_Ingles": ing, "Agua_Litros": ag}])
                guardar_datos("HABITOS", pd.concat([cargar_datos("HABITOS", 6), n], ignore_index=True))
    st.dataframe(cargar_datos("HABITOS", 6), use_container_width=True)

# --- ALCALDÍA (¡AHORA SÍ FUNCIONA!) ---
elif selected == "🏛️ Alcaldía":
    st.title("🏛️ Alcaldía")
    with st.form("alc"):
        c1, c2 = st.columns([1,3])
        f = c1.date_input("Fecha", date.today())
        act = c2.text_input("Actividad")
        if st.form_submit_button("Registrar"):
            n = pd.DataFrame([{"Fecha": f, "Actividad": act, "Evidencia": "-", "Estado": "OK"}])
            guardar_datos("ALCALDIA", pd.concat([cargar_datos("ALCALDIA", 4), n], ignore_index=True))
    
    # Aquí es donde estaba el error, ya está protegido por cargar_datos
    st.data_editor(
        cargar_datos("ALCALDIA", 4), 
        use_container_width=True, 
        column_config={"Fecha": st.column_config.DateColumn("Fecha")}
    )

# --- SUEÑOS ---
elif selected == "✨ Sueños":
    st.title("✨ Sueños")
    df = cargar_datos("SUENOS", 4)
    if not df.empty:
        ed = st.data_editor(df, num_rows="dynamic", use_container_width=True, column_config={"Fecha Meta": st.column_config.DateColumn("Fecha")})
        if st.button("Guardar"): guardar_datos("SUENOS", ed)

# --- NOTAS ---
elif selected == "📝 Notas":
    st.title("📝 Notas")
    with st.form("nt"):
        t = st.text_input("Nota")
        cat = st.selectbox("Categoría", ["General", "Iglesia", "Trabajo"])
        if st.form_submit_button("Guardar"):
            n = pd.DataFrame([{"Fecha": date.today(), "Categoria": cat, "Titulo": t, "Contenido": "-", "Importante": False}])
            guardar_datos("NOTAS", pd.concat([cargar_datos("NOTAS", 5), n], ignore_index=True))
    st.data_editor(cargar_datos("NOTAS", 5), use_container_width=True)

# --- MIRA ---
elif selected == "💙 MIRA":
    st.title("💙 MIRA")
    df = cargar_datos("MIRA", 4)
    if not df.empty:
        ed = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("Guardar"): guardar_datos("MIRA", ed)

# --- ESTUDIO ---
elif selected == "🧠 Estudio":
    st.title("🧠 Estudio")
    df = cargar_datos("PLAN_INGLES", 4)
    if not df.empty:
        ed = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("Actualizar"): guardar_datos("PLAN_INGLES", ed)

        # --- 🏆 PMO HUB (NUEVO MÓDULO) ---
elif selected == "🏆 PMO Hub":
    st.title("🏆 PMO Hub LATAM")
    st.markdown("##### **Proyecto:** Reconocimiento Voluntarios y Miembros | **Feb - Dic 2025**")
    
    # Pestañas del Módulo
    tab1, tab2, tab3 = st.tabs(["📊 Tablero", "👥 Equipo Voluntarios", "📅 Roadmap 2025"])

    # --- Pestaña 1: Tablero ---
    with tab1:
        # Cargamos datos para las métricas
        df_vol = cargar_datos("PMO_VOLUNTARIOS", 4)
        
        c1, c2, c3 = st.columns(3)
        total_vol = len(df_vol) if not df_vol.empty else 0
        activos = len(df_vol[df_vol['Estado'] == 'Activo']) if not df_vol.empty else 0
        
        c1.metric("Total Voluntarios", total_vol)
        c2.metric("Activos Ahora", activos)
        c3.metric("Próximo Hito", "Marzo (Convocatoria)")
        
        st.divider()
        st.info("🤖 **Arya PMO:** Hola Norma. Recuerda que en Febrero estamos definiendo las categorías de reconocimiento.")

    # --- Pestaña 2: Gestión de Voluntarios ---
    with tab2:
        st.subheader("Base de Datos del Equipo")
        
        # Formulario para agregar nuevo voluntario
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
                    # Si no existe df_vol, lo crea
                    df_actual = cargar_datos("PMO_VOLUNTARIOS", 4)
                    guardar_datos("PMO_VOLUNTARIOS", pd.concat([df_actual, nuevo_v], ignore_index=True))

        # Mostrar y Editar la Tabla
        df_vol = cargar_datos("PMO_VOLUNTARIOS", 4)
        if not df_vol.empty:
            edited_vol = st.data_editor(
                df_vol, 
                num_rows="dynamic", 
                use_container_width=True,
                column_config={
                    "Estado": st.column_config.SelectboxColumn("Estado", options=["Activo", "Pendiente", "Inactivo"]),
                    "Puntos": st.column_config.ProgressColumn("Puntos", min_value=0, max_value=200, format="%d pts")
                }
            )
            if st.button("💾 Actualizar Equipo"):
                guardar_datos("PMO_VOLUNTARIOS", edited_vol)
        else:
            st.warning("Aún no tienes voluntarios registrados. ¡Agrega el primero arriba!")

    # --- Pestaña 3: Roadmap (Cronograma) ---
    with tab3:
        st.subheader("📍 Línea de Tiempo del Proyecto")
        # Esto es visual, no necesita base de datos por ahora
        timeline_data = [
            {"Mes": "Febrero", "Actividad": "Kick-off y Definición Categorías", "Estado": "✅ Listo"},
            {"Mes": "Marzo", "Actividad": "Convocatoria de Postulados", "Estado": "🔄 En Curso"},
            {"Mes": "Junio", "Actividad": "Primer Corte Evaluación", "Estado": "⏳ Pendiente"},
            {"Mes": "Septiembre", "Actividad": "Gala Semestral", "Estado": "⏳ Pendiente"},
            {"Mes": "Diciembre", "Actividad": "Cierre y Premiación Anual", "Estado": "⏳ Pendiente"},
        ]
        st.dataframe(pd.DataFrame(timeline_data), use_container_width=True)