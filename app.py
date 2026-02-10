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

# --- 🏆 PMO HUB (VERSIÓN COMPLETA CON 4 PESTAÑAS) ---
elif selected == "🏆 PMO Hub":
    st.title("🏆 PMO Hub LATAM")
    st.markdown("##### **Proyecto:** Reconocimiento Voluntarios y Miembros | **Feb - Dic 2025**")
    
    # SON 4 PESTAÑAS
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Tablero", "👥 Equipo", "✅ Actividades", "📅 Roadmap"])

    # PESTAÑA 1: DASHBOARD
    with tab1:
        df_vol = cargar_datos("PMO_VOLUNTARIOS", 4)
        if df_vol.empty: 
            df_vol = pd.DataFrame(columns=["Nombre", "Rol", "Estado", "Puntos"])
        
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
                    if df_actual.empty: 
                        df_actual = pd.DataFrame(columns=["Nombre", "Rol", "Estado", "Puntos"])
                    guardar_datos("PMO_VOLUNTARIOS", pd.concat([df_actual, nuevo_v], ignore_index=True))

        df_vol = cargar_datos("PMO_VOLUNTARIOS", 4)
        if df_vol.empty: 
            df_vol = pd.DataFrame(columns=["Nombre", "Rol", "Estado", "Puntos"])
            
        edited_vol = st.data_editor(
            df_vol, num_rows="dynamic", use_container_width=True,
            column_config={
                "Estado": st.column_config.SelectboxColumn("Estado", options=["Activo", "Pendiente", "Inactivo"]),
                "Puntos": st.column_config.ProgressColumn("Puntos", min_value=0, max_value=200, format="%d pts")
            }, key="pmo_vol_editor"
        )
        if st.button("💾 Actualizar Equipo"): guardar_datos("PMO_VOLUNTARIOS", edited_vol)

    # PESTAÑA 3: ACTIVIDADES (TABLERO DE TAREAS)
    with tab3:
        st.subheader("📋 Gestión de Tareas y Entregables")
        
        df_volunteers = cargar_datos("PMO_VOLUNTARIOS", 4)
        lista_responsables = df_volunteers['Nombre'].tolist() if not df_volunteers.empty else ["Norma (PM)", "Por definir"]

        with st.expander("➕ Asignar Nueva Actividad", expanded=True):
            with st.form("form_actividades_pmo"):
                c1, c2 = st.columns([2, 1])
                actividad = c1.text_input("Descripción de la Actividad")
                responsable = c2.selectbox("Responsable", lista_responsables)
                
                c3, c4, c5 = st.columns(3)
                fecha_entrega = c3.date_input("Fecha Entrega", date.today())
                prioridad = c4.selectbox("Prioridad", ["Alta 🔥", "Media", "Baja"])
                estado_task = c5.selectbox("Estado Inicial", ["Pendiente", "En Progreso"])
                
                if st.form_submit_button("Asignar Tarea"):
                    nueva_task = pd.DataFrame([{
                        "Actividad": actividad,
                        "Responsable": responsable,
                        "Fecha_Entrega": fecha_entrega,
                        "Estado": estado_task,
                        "Prioridad": prioridad
                    }])
                    df_tasks = cargar_datos("PMO_ACTIVIDADES", 5)
                    if df_tasks.empty: 
                        df_tasks = pd.DataFrame(columns=["Actividad", "Responsable", "Fecha_Entrega", "Estado", "Prioridad"])
                    guardar_datos("PMO_ACTIVIDADES", pd.concat([df_tasks, nueva_task], ignore_index=True))

        st.divider()
        df_tasks_show = cargar_datos("PMO_ACTIVIDADES", 5)
        if df_tasks_show.empty:
            st.info("No hay actividades asignadas. ¡Crea la primera arriba!")
            df_tasks_show = pd.DataFrame(columns=["Actividad", "Responsable", "Fecha_Entrega", "Estado", "Prioridad"])
        
        edited_tasks = st.data_editor(
            df_tasks_show,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Fecha_Entrega": st.column_config.DateColumn("Entrega", format="DD/MM/YYYY"),
                "Estado": st.column_config.SelectboxColumn("Estado", options=["Pendiente", "En Progreso", "Revisión", "Completado"]),
                "Prioridad": st.column_config.SelectboxColumn("Prioridad", options=["Alta 🔥", "Media", "Baja"]),
            }, key="pmo_task_editor"
        )
        if st.button("💾 Actualizar Tareas"): guardar_datos("PMO_ACTIVIDADES", edited_tasks)

    # PESTAÑA 4: ROADMAP
    with tab4:
        st.subheader("📍 Línea de Tiempo 2025")
        st.dataframe(pd.DataFrame([
            {"Mes": "Febrero", "Actividad": "Kick-off y Definición Categorías", "Estado": "✅ Listo"},
            {"Mes": "Marzo", "Actividad": "Convocatoria de Postulados", "Estado": "🔄 En Curso"},
            {"Mes": "Junio", "Actividad": "Primer Corte Evaluación", "Estado": "⏳ Pendiente"},
            {"Mes": "Septiembre", "Actividad": "Gala Semestral", "Estado": "⏳ Pendiente"},
            {"Mes": "Diciembre", "Actividad": "Cierre y Premiación Anual", "Estado": "⏳ Pendiente"}
        ]), use_container_width=True)

# --- 🏛️ ALCALDÍA ---
elif selected == "🏛️ Alcaldía":
    st.title("🏛️ Gestión Contractual - Alcaldía")
    tab1, tab2 = st.tabs(["📝 Bitácora Diaria", "📄 Generar Informe Mensual"])
    
    with tab1:
        st.info("Registra aquí lo que hiciste hoy.")
        with st.form("alc_diario"):
            c1, c2 = st.columns([1, 3])
            fecha = c1.date_input("Fecha", date.today())
            actividad = c2.text_area("Actividad", placeholder="Ej: Reunión con DATIC...")
            obligacion = st.selectbox("Obligación", [
                "1. Apoyar gestión técnica BOD", "2. Articular con organismos", 
                "3. Informes de seguimiento", "4. Reuniones supervisor", "5. Otras conexas"
            ])
            if st.form_submit_button("Guardar Actividad"):
                nuevo_reg = pd.DataFrame([{"Fecha": fecha, "Actividad": actividad, "Obligacion": obligacion, "Estado": "Realizado"}])
                df_actual = cargar_datos("ALCALDIA", 4)
                if df_actual.empty: df_actual = pd.DataFrame(columns=["Fecha", "Actividad", "Obligacion", "Estado"])
                guardar_datos("ALCALDIA", pd.concat([df_actual, nuevo_reg], ignore_index=True))
        
        st.subheader("📋 Historial")
        st.dataframe(cargar_datos("ALCALDIA", 4).tail(5), use_container_width=True)

    with tab2:
        st.header("📄 Generador de Cuenta de Cobro")
        col_m, col_y = st.columns(2)
        mes = col_m.selectbox("Mes", range(1, 13), index=date.today().month - 1)
        anio = col_y.number_input("Año", value=2026)
        
        if st.button("✨ Generar Informe"):
            df = cargar_datos("ALCALDIA", 4)
            if not df.empty:
                df['Fecha'] = pd.to_datetime(df['Fecha'])
                df_mes = df[(df['Fecha'].dt.month == mes) & (df['Fecha'].dt.year == anio)]
                
                if df_mes.empty: st.warning("No hay actividades en este mes.")
                else:
                    st.success(f"¡{len(df_mes)} actividades encontradas!")
                    texto = f"INFORME DE EJECUCIÓN - {mes}/{anio}\n\nEn cumplimiento del objeto contractual, presento las actividades:\n\n"
                    for obli in sorted(df_mes['Obligacion'].unique()):
                        texto += f"📌 {obli}:\n"
                        for _, row in df_mes[df_mes['Obligacion'] == obli].iterrows():
                            texto += f"   • ({row['Fecha'].strftime('%d/%m')}) {row['Actividad']}.\n"
                        texto += "\n"
                    texto += "Se anexa evidencia digital.\n\nAtentamente,\nNORMA [APELLIDO]\nContratista"
                    st.text_area("Copia tu informe:", value=texto, height=400)
            else: st.error("Hoja ALCALDIA vacía.")

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