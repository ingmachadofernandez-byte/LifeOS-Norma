import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
from datetime import date, datetime
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Norma LifeOS", page_icon="🧿", layout="wide")

# --- 🎨 DISEÑO "FRIENDLY" (MODO CLARO) ---
st.markdown("""
<style>
    .stApp { background-color: #F0F9FF; }
    h1, h2, h3, h4, h5, p, span, label, div { color: #1E3A8A !important; font-family: 'Helvetica Neue', sans-serif; }
    div.stMetric, div.stDataFrame, .css-1r6slb0 {
        background-color: #FFFFFF !important; border: 1px solid #DBEAFE;
        border-radius: 15px; padding: 20px; box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    section[data-testid="stSidebar"] { background-color: #EFF6FF; border-right: 1px solid #BFDBFE; }
    .stButton>button { background-color: #3B82F6; color: white !important; border-radius: 10px; border: none; font-weight: bold; }
    .stButton>button:hover { background-color: #2563EB; }
    .alerta-roja {
        padding: 15px; background-color: #FEF2F2; color: #991B1B !important;
        border: 1px solid #FCA5A5; border-radius: 12px; margin-bottom: 20px; font-weight: bold;
    }
    .aviso-pago {
        padding: 10px; background-color: #FEF9C3; color: #854D0E !important;
        border: 1px solid #FDE047; border-radius: 8px; margin-bottom: 5px;
    }
</style>
""", unsafe_allow_html=True)

# --- CONEXIÓN ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- MENÚ LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=100)
    st.write("### Hola, Norma 👋")
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "💰 Finanzas", "🏛️ Alcaldía", "💪 Bienestar", "✨ Sueños", "📝 Notas", "💙 MIRA", "🧠 Estudio"],
        icons=["grid", "cash-coin", "bank", "heart-pulse", "stars", "journal-text", "people-fill", "book"],
        default_index=0,
        styles={
            "container": {"padding": "0!important", "background-color": "transparent"},
            "icon": {"color": "#2563EB", "font-size": "18px"}, 
            "nav-link": {"font-size": "16px", "text-align": "left", "margin":"5px", "--hover-color": "#DBEAFE", "color": "#1E3A8A"},
            "nav-link-selected": {"background-color": "#3B82F6", "color": "white"},
        }
    )

# --- FUNCIONES ---
def cargar_datos(hoja, columnas=5):
    try:
        return conn.read(worksheet=hoja, usecols=list(range(columnas)), ttl=0)
    except:
        return pd.DataFrame()

def guardar_datos(hoja, df):
    try:
        conn.update(worksheet=hoja, data=df)
        st.success("✅ ¡Guardado!")
        st.balloons()
    except Exception as e:
        st.error(f"Error: {e}")

# --- 1. DASHBOARD ---
if selected == "Dashboard":
    st.title("🧿 Tu Día Brillante")
    fecha_hoy = date.today()
    dias_esp = {"Monday":"Lunes", "Tuesday":"Martes", "Wednesday":"Miércoles", "Thursday":"Jueves", "Friday":"Viernes", "Saturday":"Sábado", "Sunday":"Domingo"}
    hoy_es = dias_esp.get(fecha_hoy.strftime("%A"), "Hoy")
    
    st.markdown(f"#### 📅 {hoy_es}, {fecha_hoy.day} de {fecha_hoy.strftime('%B')}")
    
    # Alerta Inglés
    df_habitos = cargar_datos("HABITOS", 6)
    ingles_hecho = False
    if not df_habitos.empty:
        reg = df_habitos[df_habitos['Fecha'] == str(fecha_hoy)]
        if not reg.empty and reg.iloc[0]['Min_Ingles'] > 0: ingles_hecho = True
    if not ingles_hecho:
        st.markdown('<div class="alerta-roja">🚨 ¡Recuerda tu Inglés hoy! 🇬🇧</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    rutina_gym = {"Lunes": "Pierna 🍑", "Martes": "Cardio 🔥", "Miércoles": "Espalda 💪", "Jueves": "Pierna", "Viernes": "Full Body", "Sábado": "Cardio", "Domingo": "Relax 🧘‍♀️"}
    c1.metric("🏋️‍♀️ Gym Hoy", rutina_gym.get(hoy_es, "Descanso"))

    df_fin = cargar_datos("FINANZAS", 5)
    saldo = 0
    if not df_fin.empty:
        ing = df_fin[df_fin['Tipo']=='Ingreso']['Monto'].sum()
        gas = df_fin[df_fin['Tipo']=='Gasto']['Monto'].sum()
        saldo = ing - gas
    c2.metric("💰 Disponible", f"${saldo:,.0f}")
    c3.metric("🏛️ Alcaldía", "Activa")

# --- 2. FINANZAS (VERSIÓN PRO RECUPERADA) ---
elif selected == "💰 Finanzas":
    st.title("💰 Control Financiero Total")
    
    # Cargar datos
    df_fin = cargar_datos("FINANZAS", 5)
    
    # 1. ALERTAS DE PAGO (Lógica inteligente)
    if not df_fin.empty:
        # Filtramos gastos no pagados
        pendientes = df_fin[(df_fin['Tipo'] == 'Gasto') & (df_fin['Pagado'] == False)]
        if not pendientes.empty:
            st.write("#### 🔔 Alertas de Vencimiento")
            hoy = date.today()
            hay_alertas = False
            for index, row in pendientes.iterrows():
                try:
                    # Intentamos convertir la fecha
                    f_limite = datetime.strptime(str(row['Fecha']), "%Y-%m-%d").date()
                    dias = (f_limite - hoy).days
                    
                    if dias < 0:
                        st.markdown(f'<div class="alerta-roja">🚨 VENCIDO: {row["Concepto"]} hace {abs(dias)} días</div>', unsafe_allow_html=True)
                        hay_alertas = True
                    elif 0 <= dias <= 5:
                        st.markdown(f'<div class="aviso-pago">⚠️ ATENCIÓN: {row["Concepto"]} vence en {dias} días</div>', unsafe_allow_html=True)
                        hay_alertas = True
                except:
                    pass # Si la fecha está mal escrita, la ignora
            
            if not hay_alertas: st.success("✅ Todo al día para esta semana.")
            st.divider()

    # 2. MÉTRICAS
    if not df_fin.empty:
        ing = df_fin[df_fin['Tipo']=='Ingreso']['Monto'].sum()
        gas = df_fin[df_fin['Tipo']=='Gasto']['Monto'].sum()
        disp = ing - gas
        col1, col2, col3 = st.columns(3)
        col1.metric("Ingresos", f"${ing:,.0f}")
        col2.metric("Gastos", f"${gas:,.0f}", delta_color="inverse")
        col3.metric("Disponible Real", f"${disp:,.0f}")

    # 3. REGISTRO NUEVO
    with st.expander("➕ Registrar Nuevo Movimiento", expanded=True):
        with st.form("fin"):
            c1, c2, c3, c4 = st.columns(4)
            tipo = c1.selectbox("Tipo", ["Gasto", "Ingreso"])
            # AQUÍ ESTÁ LA MAGIA DEL CALENDARIO
            f_mov = c2.date_input("Fecha", date.today()) 
            monto = c3.number_input("Monto", step=1000)
            conc = c4.text_input("Concepto (Ej: Arriendo)")
            pagado = st.checkbox("¿Ya lo pagué?", value=True)
            
            if st.form_submit_button("💾 Registrar"):
                n = pd.DataFrame([{
                    "Fecha": f_mov.strftime("%Y-%m-%d"), 
                    "Concepto": conc, 
                    "Monto": monto, 
                    "Tipo": tipo, 
                    "Pagado": pagado
                }])
                guardar_datos("FINANZAS", pd.concat([df_fin, n], ignore_index=True))

    # 4. TABLA EDITABLE (CON CALENDARIO)
    st.subheader("📝 Historial Detallado")
    if not df_fin.empty:
        st.data_editor(
            df_fin,
            num_rows="dynamic",
            use_container_width=True,
            column_config={
                "Fecha": st.column_config.DateColumn("Fecha", format="YYYY-MM-DD"), # Calendario en la tabla
                "Monto": st.column_config.NumberColumn("Monto", format="$%d"),
                "Pagado": st.column_config.CheckboxColumn("Pagado")
            }
        )

# --- 3. ALCALDÍA (CON CALENDARIO) ---
elif selected == "🏛️ Alcaldía":
    st.title("🏛️ Alcaldía")
    with st.form("alc"):
        c1, c2 = st.columns([1,3])
        f_act = c1.date_input("Fecha", date.today()) # Calendario
        act = c2.text_input("Actividad")
        if st.form_submit_button("Registrar"):
            n = pd.DataFrame([{"Fecha": f_act.strftime("%Y-%m-%d"), "Actividad": act, "Evidencia": "-", "Estado": "OK"}])
            guardar_datos("ALCALDIA", pd.concat([cargar_datos("ALCALDIA", 4), n], ignore_index=True))
    
    st.data_editor(
        cargar_datos("ALCALDIA", 4), 
        use_container_width=True,
        column_config={
            "Fecha": st.column_config.DateColumn("Fecha", format="YYYY-MM-DD") # Calendario
        }
    )

# --- 4. BIENESTAR (CON CALENDARIO) ---
elif selected == "💪 Bienestar":
    st.title("💪 Registro Diario")
    with st.form("habitos"):
        c1, c2, c3, c4 = st.columns(4)
        fecha_h = c1.date_input("Fecha", date.today()) # Calendario
        h_gym = c2.selectbox("Gym", ["Pierna", "Brazo", "Cardio", "Descanso"])
        h_ingles = c3.number_input("Min. Inglés", step=15)
        h_agua = c4.slider("Agua", 0.0, 4.0, 1.5)
        if st.form_submit_button("Guardar"):
            n = pd.DataFrame([{"Fecha": fecha_h.strftime("%Y-%m-%d"), "Enfoque_Gym": h_gym, "Min_Lectura": 0, "Min_Biblia": 0, "Min_Ingles": h_ingles, "Agua_Litros": h_agua}])
            guardar_datos("HABITOS", pd.concat([cargar_datos("HABITOS", 6), n], ignore_index=True))
    
    st.dataframe(cargar_datos("HABITOS", 6), use_container_width=True)

# --- (RESTO DE MÓDULOS IGUALES) ---
elif selected == "✨ Sueños":
    st.title("✨ Mis Sueños")
    df = cargar_datos("SUENOS", 4)
    if not df.empty:
        ed = st.data_editor(df, num_rows="dynamic", use_container_width=True, column_config={"Fecha Meta": st.column_config.DateColumn("Fecha")})
        if st.button("Guardar"): guardar_datos("SUENOS", ed)

elif selected == "📝 Notas":
    st.title("📝 Notas")
    with st.form("notas"):
        tit = st.text_input("Nota")
        if st.form_submit_button("Guardar"):
            n = pd.DataFrame([{"Fecha": str(date.today()), "Categoria": "General", "Titulo": tit, "Contenido": "-", "Importante": False}])
            guardar_datos("NOTAS", pd.concat([cargar_datos("NOTAS", 5), n], ignore_index=True))
    st.data_editor(cargar_datos("NOTAS", 5), use_container_width=True)

elif selected == "💙 MIRA":
    st.title("💙 MIRA")
    df = cargar_datos("MIRA", 4)
    if not df.empty:
        ed = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("Guardar"): guardar_datos("MIRA", ed)

elif selected == "🧠 Estudio":
    st.title("🧠 Estudio")
    df = cargar_datos("PLAN_INGLES", 4)
    if not df.empty:
        ed = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("Actualizar"): guardar_datos("PLAN_INGLES", ed)