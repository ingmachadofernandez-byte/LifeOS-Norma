import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
from datetime import date, datetime
from streamlit_gsheets import GSheetsConnection

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Norma LifeOS", page_icon="🧿", layout="wide")

# --- 🎨 ESTILOS (MODO CLARO) ---
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
</style>
""", unsafe_allow_html=True)

# --- CONEXIÓN ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- MENÚ (CON NUMBRA INCLUIDO) ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=100)
    st.write("### Hola, Norma 👋")
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "💰 Finanzas", "🚀 Numbra", "🏛️ Alcaldía", "💪 Bienestar", "✨ Sueños", "📝 Notas", "💙 MIRA", "🧠 Estudio"],
        icons=["grid", "cash-coin", "rocket-takeoff", "bank", "heart-pulse", "stars", "journal-text", "people-fill", "book"],
        default_index=0,
    )

# --- FUNCIONES MAESTRAS ---
def cargar_datos(hoja, columnas=5):
    try:
        df = conn.read(worksheet=hoja, usecols=list(range(columnas)), ttl=0)
        # LIMPIEZA DE FINANZAS
        if hoja == "FINANZAS" and not df.empty:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            df['Pagado'] = df['Pagado'].astype(str).map({'TRUE': True, 'FALSE': False, 'True': True, 'False': False, '1': True, '0': False}).fillna(False)
            df['Monto'] = pd.to_numeric(df['Monto'], errors='coerce').fillna(0)
        return df
    except Exception as e:
        return pd.DataFrame()

def guardar_datos(hoja, df):
    try:
        conn.update(worksheet=hoja, data=df)
        st.success("✅ ¡Guardado!")
        st.rerun()
    except Exception as e:
        st.error(f"Error: {e}")

# --- 1. DASHBOARD ---
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
    if not hecho: st.markdown('<div class="alerta-roja">🚨 ¡Recuerda tu Inglés hoy! 🇬🇧</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    df_fin = cargar_datos("FINANZAS", 5)
    saldo = 0
    if not df_fin.empty:
        saldo = df_fin[df_fin['Tipo']=='Ingreso']['Monto'].sum() - df_fin[df_fin['Tipo']=='Gasto']['Monto'].sum()
    
    rutina = {"Lunes": "Pierna 🍑", "Martes": "Cardio 🔥", "Miércoles": "Espalda 💪", "Jueves": "Pierna", "Viernes": "Full Body", "Domingo": "Relax"}
    
    c1.metric("🏋️‍♀️ Gym", rutina.get(hoy_es, "Descanso"))
    c2.metric("💰 Disponible", f"${saldo:,.0f}")
    c3.metric("🚀 Numbra", "Fase 1")

# --- 2. FINANZAS ---
elif selected == "💰 Finanzas":
    st.title("💰 Tablero Financiero")
    df_fin = cargar_datos("FINANZAS", 5)
    
    if not df_fin.empty:
        ing = df_fin[df_fin['Tipo']=='Ingreso']['Monto'].sum()
        gas = df_fin[df_fin['Tipo']=='Gasto']['Monto'].sum()
        k1, k2, k3 = st.columns(3)
        k1.metric("Ingresos", f"${ing:,.0f}")
        k2.metric("Gastos", f"${gas:,.0f}", delta_color="inverse")
        k3.metric("Disponible", f"${(ing-gas):,.0f}")
        st.divider()

        c_chart1, c_chart2 = st.columns(2)
        gastos_df = df_fin[df_fin['Tipo'] == 'Gasto']
        if not gastos_df.empty:
            fig1 = px.pie(gastos_df, values='Monto', names='Concepto', title='Gastos', hole=0.4)
            c_chart1.plotly_chart(fig1, use_container_width=True)
        
        resumen = df_fin.groupby('Tipo')['Monto'].sum().reset_index()
        fig2 = px.bar(resumen, x='Tipo', y='Monto', color='Tipo', title='Balance', color_discrete_map={'Ingreso':'#4ADE80', 'Gasto':'#F87171'})
        c_chart2.plotly_chart(fig2, use_container_width=True)

    with st.expander("➕ Registrar Movimiento", expanded=True):
        with st.form("fin"):
            c1, c2, c3, c4 = st.columns(4)
            tipo = c1.selectbox("Tipo", ["Gasto", "Ingreso"])
            fecha = c2.date_input("Fecha", date.today())
            monto = c3.number_input("Monto", step=1000)
            conc = c4.text_input("Concepto")
            pagado = st.checkbox("Pagado", value=True)
            if st.form_submit_button("Guardar"):
                n = pd.DataFrame([{"Fecha": fecha, "Concepto": conc, "Monto": monto, "Tipo": tipo, "Pagado": pagado}])
                guardar_datos("FINANZAS", pd.concat([df_fin, n], ignore_index=True))

    if not df_fin.empty:
        st.data_editor(df_fin, num_rows="dynamic", use_container_width=True, column_config={"Fecha": st.column_config.DateColumn("Fecha"), "Monto": st.column_config.NumberColumn("Monto", format="$%d"), "Pagado": st.column_config.CheckboxColumn("Pagado")})

# --- 3. NUMBRA ---
elif selected == "🚀 Numbra":
    st.title("🚀 Proyecto Numbra")
    st.info("🚧 Área de Proyecto")
    st.markdown("### 📊 Estado del Proyecto\nAquí podrás gestionar cronogramas y presupuestos.")

# --- 4. ALCALDÍA ---
elif selected == "🏛️ Alcaldía":
    st.title("🏛️ Alcaldía")
    with st.form("alc"):
        c1, c2 = st.columns([1,3])
        f = c1.date_input("Fecha", date.today())
        act = c2.text_input("Actividad")
        if st.form_submit_button("Registrar"):
            n = pd.DataFrame([{"Fecha": f, "Actividad": act, "Evidencia": "-", "Estado": "OK"}])
            guardar_datos("ALCALDIA", pd.concat([cargar_datos("ALCALDIA", 4), n], ignore_index=True))
    st.data_editor(cargar_datos("ALCALDIA", 4), use_container_width=True, column_config={"Fecha": st.column_config.DateColumn("Fecha")})

# --- 5. BIENESTAR ---
elif selected == "💪 Bienestar":
    st.title("💪 Salud")
    with st.form("hab"):
        c1, c2, c3 = st.columns(3)
        f = c1.date_input("Fecha", date.today())
        gym = c2.selectbox("Gym", ["Pierna", "Brazo", "Cardio", "Descanso"])
        ing = c3.number_input("Min. Inglés", step=15)
        if st.form_submit_button("Guardar"):
            n = pd.DataFrame([{"Fecha": f, "Enfoque_Gym": gym, "Min_Lectura": 0, "Min_Biblia": 0, "Min_Ingles": ing, "Agua_Litros": 1.5}])
            guardar_datos("HABITOS", pd.concat([cargar_datos("HABITOS", 6), n], ignore_index=True))
    st.dataframe(cargar_datos("HABITOS", 6), use_container_width=True)

# --- 6. SUEÑOS ---
elif selected == "✨ Sueños":
    st.title("✨ Sueños")
    df = cargar_datos("SUENOS", 4)
    if not df.empty:
        ed = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("Guardar"): guardar_datos("SUENOS", ed)

# --- 7. NOTAS ---
elif selected == "📝 Notas":
    st.title("📝 Notas")
    with st.form("nt"):
        t = st.text_input("Nota")
        if st.form_submit_button("Guardar"):
            n = pd.DataFrame([{"Fecha": date.today(), "Categoria": "General", "Titulo": t, "Contenido": "-", "Importante": False}])
            guardar_datos("NOTAS", pd.concat([cargar_datos("NOTAS", 5), n], ignore_index=True))
    st.data_editor(cargar_datos("NOTAS", 5), use_container_width=True)

# --- 8. MIRA ---
elif selected == "💙 MIRA":
    st.title("💙 MIRA")
    df = cargar_datos("MIRA", 4)
    if not df.empty:
        ed = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("Guardar"): guardar_datos("MIRA", ed)

# --- 9. ESTUDIO ---
elif selected == "🧠 Estudio":
    st.title("🧠 Estudio")
    df = cargar_datos("PLAN_INGLES", 4)
    if not df.empty:
        ed = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("Actualizar"): guardar_datos("PLAN_INGLES", ed)