import streamlit as st
from streamlit_option_menu import option_menu
import plotly.express as px
import pandas as pd
from datetime import date, datetime
from streamlit_gsheets import GSheetsConnection

# --- 1. CONFIGURACIÓN INICIAL ---
st.set_page_config(page_title="Norma OS", page_icon="🧿", layout="wide")

# --- 2. ESTILOS VISUALES (MODO CLARO Y AMIGABLE) ---
st.markdown("""
<style>
    /* Fondo y Textos */
    .stApp { background-color: #F0F9FF; }
    h1, h2, h3, h4, h5, p, span, label, div { color: #1E3A8A !important; font-family: 'Helvetica Neue', sans-serif; }
    
    /* Tarjetas y Tablas */
    div.stMetric, div.stDataFrame, .css-1r6slb0 {
        background-color: #FFFFFF !important; 
        border: 1px solid #DBEAFE;
        border-radius: 15px; 
        padding: 20px; 
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
    }
    
    /* Barra Lateral */
    section[data-testid="stSidebar"] { background-color: #EFF6FF; border-right: 1px solid #BFDBFE; }
    
    /* Botones */
    .stButton>button { 
        background-color: #3B82F6; color: white !important; 
        border-radius: 10px; border: none; font-weight: bold; padding: 10px 20px;
    }
    .stButton>button:hover { background-color: #2563EB; }
    
    /* Alertas */
    .alerta-roja {
        padding: 15px; background-color: #FEF2F2; color: #991B1B !important;
        border: 1px solid #FCA5A5; border-radius: 12px; margin-bottom: 20px; font-weight: bold; text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# --- 3. CONEXIÓN A LA NUBE ---
conn = st.connection("gsheets", type=GSheetsConnection)

# --- 4. MENÚ LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=100)
    st.write("### Hola, Norma 👋")
    
    selected = option_menu(
        menu_title=None,
        options=["Dashboard", "💪 Bienestar", "💰 Finanzas", "🏛️ Alcaldía", "🚀 Numbra", "✨ Sueños", "📝 Notas", "💙 MIRA", "🧠 Estudio"],
        icons=["grid", "heart-pulse", "cash-coin", "bank", "rocket-takeoff", "stars", "journal-text", "people-fill", "book"],
        default_index=0,
    )

# --- 5. FUNCIONES MAESTRAS (INTELIGENCIA) ---
def cargar_datos(hoja, columnas=5):
    try:
        df = conn.read(worksheet=hoja, usecols=list(range(columnas)), ttl=0)
        
        # LIMPIEZA AUTOMÁTICA DE FINANZAS (Para que no salga error rojo)
        if hoja == "FINANZAS" and not df.empty:
            df['Fecha'] = pd.to_datetime(df['Fecha'], errors='coerce')
            df['Monto'] = pd.to_numeric(df['Monto'], errors='coerce').fillna(0)
            # Convierte texto raro a Checkbox Real
            df['Pagado'] = df['Pagado'].astype(str).map({
                'TRUE': True, 'FALSE': False, 'True': True, 'False': False, '1': True, '0': False
            }).fillna(False)
            
        return df
    except Exception as e:
        return pd.DataFrame() # Si falla, devuelve tabla vacía para no romper la app

def guardar_datos(hoja, df):
    try:
        conn.update(worksheet=hoja, data=df)
        st.success("✅ ¡Guardado en la nube!")
        st.rerun() # Recarga la página
    except Exception as e:
        st.error(f"Error al guardar: {e}")

# ==========================================
#              MÓDULOS DE LA APP
# ==========================================

# --- MÓDULO 1: DASHBOARD (RESUMEN) ---
if selected == "Dashboard":
    st.title("🧿 Tu Día Brillante")
    hoy = date.today()
    dias_esp = {"Monday":"Lunes", "Tuesday":"Martes", "Wednesday":"Miércoles", "Thursday":"Jueves", "Friday":"Viernes", "Saturday":"Sábado", "Sunday":"Domingo"}
    hoy_es = dias_esp.get(hoy.strftime("%A"), "Hoy")
    st.markdown(f"#### 📅 {hoy_es}, {hoy.day}")

    # 1. ALERTA DE INGLÉS (PEPE GRILLO)
    df_h = cargar_datos("HABITOS", 6)
    ingles_hecho = False
    if not df_h.empty:
        reg = df_h[df_h['Fecha'].astype(str) == str(hoy)]
        if not reg.empty and reg.iloc[0]['Min_Ingles'] > 0: ingles_hecho = True
    
    if not ingles_hecho:
        st.markdown('<div class="alerta-roja">🚨 ¡Alerta! No has registrado Inglés hoy 🇬🇧</div>', unsafe_allow_html=True)
    else:
        st.success("✅ ¡Inglés completado hoy!")

    # 2. MÉTRICAS RÁPIDAS
    c1, c2, c3 = st.columns(3)
    
    # Gym
    rutina = {"Lunes": "Pierna 🍑", "Martes": "Cardio 🔥", "Miércoles": "Espalda 💪", "Jueves": "Pierna", "Viernes": "Full Body", "Sábado": "Cardio", "Domingo": "Relax"}
    c1.metric("🏋️‍♀️ Toca Gym", rutina.get(hoy_es, "Descanso"))
    
    # Plata
    df_fin = cargar_datos("FINANZAS", 5)
    saldo = 0
    if not df_fin.empty:
        ing = df_fin[df_fin['Tipo']=='Ingreso']['Monto'].sum()
        gas = df_fin[df_fin['Tipo']=='Gasto']['Monto'].sum()
        saldo = ing - gas
    c2.metric("💰 Disponible", f"${saldo:,.0f}")
    
    c3.metric("🚀 Numbra", "Activo")

# --- MÓDULO 2: BIENESTAR (COMPLETO) ---
elif selected == "💪 Bienestar":
    st.title("💪 Salud y Hábitos")
    st.info("Registra todo lo que nutre tu mente, cuerpo y espíritu.")
    
    # Formulario Completo
    with st.expander("➕ Registrar Progreso Diario", expanded=True):
        with st.form("form_bienestar"):
            c1, c2 = st.columns(2)
            f_fecha = c1.date_input("Fecha", date.today())
            f_gym = c2.selectbox("Enfoque Gym", ["Pierna", "Glúteo", "Brazo/Espalda", "Cardio", "Descanso", "Otro"])
            
            c3, c4, c5 = st.columns(3)
            f_lectura = c3.number_input("Min. Lectura 📚", min_value=0, step=5)
            f_biblia = c4.number_input("Min. Biblia ✝️", min_value=0, step=5)
            f_ingles = c5.number_input("Min. Inglés 🇬🇧", min_value=0, step=15)
            
            f_agua = st.slider("Litros de Agua 💧", 0.0, 4.0, 1.5)
            
            if st.form_submit_button("💾 Guardar Mi Progreso"):
                nuevo = pd.DataFrame([{
                    "Fecha": f_fecha,
                    "Enfoque_Gym": f_gym,
                    "Min_Lectura": f_lectura,
                    "Min_Biblia": f_biblia,
                    "Min_Ingles": f_ingles,
                    "Agua_Litros": f_agua
                }])
                df_ant = cargar_datos("HABITOS", 6)
                guardar_datos("HABITOS", pd.concat([df_ant, nuevo], ignore_index=True))

    st.subheader("📊 Historial de Disciplina")
    st.dataframe(cargar_datos("HABITOS", 6), use_container_width=True)

# --- MÓDULO 3: FINANZAS (RECUPERADO) ---
elif selected == "💰 Finanzas":
    st.title("💰 Control Financiero")
    df_fin = cargar_datos("FINANZAS", 5)
    
    # Resumen
    if not df_fin.empty:
        ing = df_fin[df_fin['Tipo']=='Ingreso']['Monto'].sum()
        gas = df_fin[df_fin['Tipo']=='Gasto']['Monto'].sum()
        col1, col2, col3 = st.columns(3)
        col1.metric("Ingresos", f"${ing:,.0f}")
        col2.metric("Gastos", f"${gas:,.0f}", delta_color="inverse")
        col3.metric("Saldo Real", f"${(ing-gas):,.0f}")
        st.divider()
        
        # Gráficos
        g1, g2 = st.columns(2)
        gastos_df = df_fin[df_fin['Tipo'] == 'Gasto']
        if not gastos_df.empty:
            fig = px.pie(gastos_df, values='Monto', names='Concepto', title='Distribución de Gastos', hole=0.4)
            g1.plotly_chart(fig, use_container_width=True)
        
        balance = df_fin.groupby('Tipo')['Monto'].sum().reset_index()
        fig2 = px.bar(balance, x='Tipo', y='Monto', color='Tipo', title='Balance', color_discrete_map={'Ingreso':'#4ADE80', 'Gasto':'#F87171'})
        g2.plotly_chart(fig2, use_container_width=True)

    # Registro
    with st.expander("➕ Nuevo Movimiento", expanded=True):
        with st.form("fin"):
            c1, c2, c3, c4 = st.columns(4)
            tipo = c1.selectbox("Tipo", ["Gasto", "Ingreso"])
            fecha = c2.date_input("Fecha", date.today())
            monto = c3.number_input("Monto", step=1000)
            conc = c4.text_input("Concepto")
            pagado = st.checkbox("¿Pagado?", value=True)
            
            if st.form_submit_button("Registrar"):
                n = pd.DataFrame([{"Fecha": fecha, "Concepto": conc, "Monto": monto, "Tipo": tipo, "Pagado": pagado}])
                guardar_datos("FINANZAS", pd.concat([df_fin, n], ignore_index=True))
    
    st.subheader("📝 Detalle")
    if not df_fin.empty:
        st.data_editor(
            df_fin, 
            num_rows="dynamic", 
            use_container_width=True,
            column_config={
                "Fecha": st.column_config.DateColumn("Fecha"),
                "Monto": st.column_config.NumberColumn("Monto", format="$%d"),
                "Pagado": st.column_config.CheckboxColumn("Pagado")
            }
        )

# --- MÓDULO 4: ALCALDÍA ---
elif selected == "🏛️ Alcaldía":
    st.title("🏛️ Bitácora Alcaldía")
    with st.form("alc"):
        c1, c2 = st.columns([1,3])
        f = c1.date_input("Fecha", date.today())
        act = c2.text_input("Actividad")
        if st.form_submit_button("Registrar"):
            n = pd.DataFrame([{"Fecha": f, "Actividad": act, "Evidencia": "-", "Estado": "OK"}])
            guardar_datos("ALCALDIA", pd.concat([cargar_datos("ALCALDIA", 4), n], ignore_index=True))
    
    st.data_editor(cargar_datos("ALCALDIA", 4), use_container_width=True, column_config={"Fecha": st.column_config.DateColumn("Fecha")})

# --- MÓDULO 5: NUMBRA ---
elif selected == "🚀 Numbra":
    st.title("🚀 Proyecto Numbra")
    st.info("🚧 Espacio reservado para métricas de tu emprendimiento.")
    st.markdown("### Próximos Pasos:\n* Definir cronograma\n* Presupuesto inicial")

# --- MÓDULO 6: SUEÑOS ---
elif selected == "✨ Sueños":
    st.title("✨ Mapa de Sueños")
    df = cargar_datos("SUENOS", 4)
    if not df.empty:
        ed = st.data_editor(df, num_rows="dynamic", use_container_width=True, column_config={"Fecha Meta": st.column_config.DateColumn("Fecha")})
        if st.button("Guardar Sueños"): guardar_datos("SUENOS", ed)

# --- MÓDULO 7: NOTAS ---
elif selected == "📝 Notas":
    st.title("📝 Notas Rápidas")
    with st.form("nt"):
        t = st.text_input("Nota")
        cat = st.selectbox("Categoría", ["General", "Iglesia", "Trabajo", "Idea"])
        if st.form_submit_button("Guardar"):
            n = pd.DataFrame([{"Fecha": date.today(), "Categoria": cat, "Titulo": t, "Contenido": "-", "Importante": False}])
            guardar_datos("NOTAS", pd.concat([cargar_datos("NOTAS", 5), n], ignore_index=True))
    st.data_editor(cargar_datos("NOTAS", 5), use_container_width=True)

# --- MÓDULO 8: MIRA ---
elif selected == "💙 MIRA":
    st.title("💙 Gestión MIRA")
    df = cargar_datos("MIRA", 4)
    if not df.empty:
        ed = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("Guardar"): guardar_datos("MIRA", ed)

# --- MÓDULO 9: ESTUDIO ---
elif selected == "🧠 Estudio":
    st.title("🧠 Plan de Estudio")
    df = cargar_datos("PLAN_INGLES", 4)
    if not df.empty:
        ed = st.data_editor(df, num_rows="dynamic", use_container_width=True)
        if st.button("Actualizar Plan"): guardar_datos("PLAN_INGLES", ed)