import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
from datetime import date, datetime
from streamlit_gsheets import GSheetsConnection
import PyPDF2

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Norma LifeOS", page_icon="🧿", layout="wide")

# --- ESTILOS VISUALES (CSS) ---
st.markdown("""
<style>
    .stApp { background-color: #F8FAFC; }
    div.stMetric {
        background-color: #FFFFFF;
        border: 1px solid #E2E8F0;
        border-radius: 10px;
        padding: 15px;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
    }
    .alerta-roja {
        padding: 15px; background-color: #FEE2E2; color: #991B1B;
        border: 1px solid #F87171; border-radius: 10px; margin-bottom: 20px;
        font-weight: bold; text-align: center;
    }
    .agenda-card {
        padding: 15px; background-color: #E0F2FE; color: #075985;
        border-radius: 10px; border-left: 5px solid #0284C7; margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- CONEXIÓN A LA NUBE ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- MENÚ LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=80)
    st.write("## Hola, Norma 👋")
    
    selected = option_menu(
        menu_title="LifeOS v10.0",
        options=["Dashboard", "💪 Bienestar", "🧠 Estudio", "✨ Sueños", "🏛️ Alcaldía", "💰 Finanzas", "📝 Notas", "💙 MIRA"],
        icons=["grid", "heart-pulse", "book", "stars", "bank", "cash-coin", "journal-text", "people-fill"],
        default_index=0,
    )
    st.divider()
    st.caption("Asistente Integral IA ☁️")

# --- FUNCIONES MAESTRAS ---
def cargar_datos(hoja, columnas=5):
    try:
        return conn.read(worksheet=hoja, usecols=list(range(columnas)), ttl=0)
    except:
        return pd.DataFrame()

def guardar_datos(hoja, df):
    try:
        conn.update(worksheet=hoja, data=df)
        st.success("✅ ¡Guardado en la nube!")
        st.balloons()
    except Exception as e:
        st.error(f"Error al guardar: {e}")

# --- 1. DASHBOARD (TU AGENDA DIARIA) ---
if selected == "Dashboard":
    st.title("🧿 Tu Día Hoy")
    fecha_hoy = date.today()
    dia_semana = fecha_hoy.strftime("%A") # Obtenemos el día (Monday, Tuesday...)
    
    # TRADUCTOR DE DÍAS (Para que Arya hable español)
    dias_esp = {"Monday":"Lunes", "Tuesday":"Martes", "Wednesday":"Miércoles", "Thursday":"Jueves", "Friday":"Viernes", "Saturday":"Sábado", "Sunday":"Domingo"}
    hoy_es = dias_esp.get(dia_semana, "Hoy")
    
    st.markdown(f"### 📅 {hoy_es}, {fecha_hoy.day} de {fecha_hoy.strftime('%B')}")

    # --- ZONA DE ALERTAS (EL PEPE GRILLO) ---
    df_habitos = cargar_datos("HABITOS", 6)
    ingles_hecho = False
    
    if not df_habitos.empty:
        # Buscamos si hay registro de HOY
        registro_hoy = df_habitos[df_habitos['Fecha'] == str(fecha_hoy)]
        if not registro_hoy.empty:
            minutos = registro_hoy.iloc[0]['Min_Ingles']
            if minutos > 0:
                ingles_hecho = True
    
    if not ingles_hecho:
        st.markdown("""
        <div class="alerta-roja">
            🚨 ALERTA: ¡No has estudiado Inglés hoy! 🇬🇧<br>
            Ve al módulo de 'Bienestar' y registra tus minutos.
        </div>
        """, unsafe_allow_html=True)
    else:
        st.success("✅ ¡Bien hecho! Ya cumpliste con tu inglés de hoy.")

    # --- TU AGENDA AUTOMÁTICA ---
    col1, col2, col3 = st.columns(3)
    
    # 1. GYM (Lógica simple: Un músculo por día)
    rutina_gym = {
        "Lunes": "Pierna y Glúteo 🍑", "Martes": "Cardio y Abdomen 🔥",
        "Miércoles": "Espalda y Brazos 💪", "Jueves": "Pierna (Enfoque Femoral)",
        "Viernes": "Cuerpo Completo (Full Body)", "Sábado": "Cardio Larga Duración 🏃‍♀️", "Domingo": "Descanso Activo / Estiramiento 🧘‍♀️"
    }
    toca_gym = rutina_gym.get(hoy_es, "Descanso")
    col1.info(f"💪 **Gym Hoy:**\n\n{toca_gym}")

    # 2. MENÚ DEL DÍA (Desde Excel)
    df_menu = cargar_datos("MENU", 4)
    plato_hoy = "No hay menú registrado"
    if not df_menu.empty:
        # Busca la fila donde dice 'Lunes' (o el día de hoy)
        menu_hoy = df_menu[df_menu['Dia_Semana'] == hoy_es]
        if not menu_hoy.empty:
            # Muestra lo que haya en la columna 'Plato'
            plato_hoy = "\n".join([f"- {r['Comida']}: {r['Plato']}" for i, r in menu_hoy.iterrows()])
    
    col2.warning(f"🥗 **Menú Hoy:**\n\n{plato_hoy}")

    # 3. SIGUIENTE CLASE DE INGLÉS
    df_plan = cargar_datos("PLAN_INGLES", 4)
    prox_clase = "¡Plan completado o vacío!"
    if not df_plan.empty:
        # Busca la primera que NO esté lista
        pendientes = df_plan[df_plan['Estado'] != 'Listo']
        if not pendientes.empty:
            prox = pendientes.iloc[0]
            prox_clase = f"**{prox['Dia']}:** {prox['Tema']}\n\n📝 *{prox['Actividad']}*"
    
    col3.success(f"🇬🇧 **Misión Inglés:**\n\n{prox_clase}")


# --- 2. BIENESTAR (HÁBITOS) ---
elif selected == "💪 Bienestar":
    st.title("💪 Registro Diario")
    
    with st.form("form_habitos"):
        st.write("¿Qué lograste hoy?")
        c1, c2, c3, c4 = st.columns(4)
        h_gym = c1.selectbox("Enfoque Gym", ["Pierna", "Brazo", "Cardio", "Descanso", "Otro"])
        h_leer = c2.number_input("Min. Lectura", step=5)
        h_biblia = c3.number_input("Min. Biblia", step=5)
        h_ingles = c4.number_input("Min. Inglés", step=15)
        h_agua = st.slider("Litros de Agua 💧", 0.0, 4.0, 1.5)
        
        if st.form_submit_button("💾 Guardar Mi Progreso"):
            nuevo = pd.DataFrame([{
                "Fecha": str(date.today()), 
                "Enfoque_Gym": h_gym, 
                "Min_Lectura": h_leer, 
                "Min_Biblia": h_biblia,
                "Min_Ingles": h_ingles,
                "Agua_Litros": h_agua
            }])
            # Guardado inteligente: agrega al historial
            df_old = cargar_datos("HABITOS", 6)
            guardar_datos("HABITOS", pd.concat([df_old, nuevo], ignore_index=True))

    st.divider()
    st.write("📊 **Tu Historial de Disciplina**")
    df_ver = cargar_datos("HABITOS", 6)
    if not df_ver.empty:
        st.dataframe(df_ver, use_container_width=True)

# --- 3. ESTUDIO (BIBLIOTECA) ---
elif selected == "🧠 Estudio":
    st.title("🧠 Biblioteca & Plan de Inglés")
    
    tab1, tab2 = st.tabs(["🇬🇧 Plan de Inglés", "📚 Mis Libros"])
    
    with tab1:
        st.subheader("Ruta de Aprendizaje (3 Meses)")
        df_plan = cargar_datos("PLAN_INGLES", 4)
        if not df_plan.empty:
            edited_plan = st.data_editor(
                df_plan, 
                num_rows="dynamic", 
                use_container_width=True,
                column_config={"Estado": st.column_config.SelectboxColumn("Estado", options=["Pendiente", "Listo"])}
            )
            if st.button("Actualizar Plan"):
                guardar_datos("PLAN_INGLES", edited_plan)
        else:
            st.info("Tu plan está vacío. Agrega días en el Excel o aquí mismo.")
            if st.button("Crear Plantilla Base"):
                base = pd.DataFrame([
                    {"Dia": "Dia 1", "Tema": "Verbo To Be", "Actividad": "Ver video en YT", "Estado": "Pendiente"},
                    {"Dia": "Dia 2", "Tema": "Presente Simple", "Actividad": "Escribir 10 frases", "Estado": "Pendiente"}
                ])
                guardar_datos("PLAN_INGLES", base)

    with tab2:
        st.write("Próximamente: Lista de libros leídos...")

# --- 4. SUEÑOS ---
elif selected == "✨ Sueños":
    st.title("✨ Mapa de Sueños & Viajes")
    df_suenos = cargar_datos("SUENOS", 4)
    if not df_suenos.empty:
        ed_suenos = st.data_editor(df_suenos, num_rows="dynamic", use_container_width=True)
        if st.button("💾 Guardar Sueños"): guardar_datos("SUENOS", ed_suenos)

# --- 5. NOTAS (INBOX) ---
elif selected == "📝 Notas":
    st.title("📝 Inbox & Notas Iglesia")
    with st.expander("➕ Nueva Nota Rápida", expanded=True):
        with st.form("notas"):
            cat = st.selectbox("Categoría", ["Iglesia", "Trabajo", "Idea Brillante", "Jefe", "Inbox"])
            tit = st.text_input("Título")
            cont = st.text_area("Contenido")
            imp = st.checkbox("¡Importante!")
            if st.form_submit_button("Guardar Nota"):
                nueva = pd.DataFrame([{"Fecha": str(date.today()), "Categoria": cat, "Titulo": tit, "Contenido": cont, "Importante": imp}])
                guardar_datos("NOTAS", pd.concat([cargar_datos("NOTAS", 5), nueva], ignore_index=True))
    
    st.divider()
    df_notas = cargar_datos("NOTAS", 5)
    if not df_notas.empty:
        st.data_editor(df_notas, use_container_width=True)

# --- 6. ALCALDÍA ---
elif selected == "🏛️ Alcaldía":
    st.title("🏛️ Bitácora Alcaldía")
    # (Código resumido igual al anterior)
    with st.form("alc"):
        act = st.text_input("Actividad de hoy")
        if st.form_submit_button("Registrar"):
            n = pd.DataFrame([{"Fecha": str(date.today()), "Actividad": act, "Evidencia": "-", "Estado": "OK"}])
            guardar_datos("ALCALDIA", pd.concat([cargar_datos("ALCALDIA", 4), n], ignore_index=True))
    st.data_editor(cargar_datos("ALCALDIA", 4), use_container_width=True)

# --- 7. FINANZAS ---
elif selected == "💰 Finanzas":
    st.title("💰 Finanzas")
    st.info("Registra tus movimientos aquí.")
    # (Lógica resumida para ahorrar espacio, funciona igual leyendo la hoja FINANZAS)
    df_fin = cargar_datos("FINANZAS", 5)
    st.data_editor(df_fin, num_rows="dynamic", use_container_width=True)

# --- 8. MIRA ---
elif selected == "💙 MIRA":
    st.title("💙 MIRA")
    st.data_editor(cargar_datos("MIRA", 4), num_rows="dynamic", use_container_width=True)