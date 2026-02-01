import streamlit as st
from streamlit_option_menu import option_menu
import plotly.graph_objects as go
import plotly.express as px
import PyPDF2
import pandas as pd
from datetime import date, datetime, timedelta # Importamos el reloj 🕰️

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Norma LifeOS", page_icon="🧿", layout="wide")

# --- ESTILOS ---
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
    .alerta-pago {
        padding: 10px; border-radius: 5px; background-color: #FEE2E2; color: #991B1B; border: 1px solid #F87171; margin-bottom: 10px;
    }
</style>
""", unsafe_allow_html=True)

# --- BARRA LATERAL ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4140/4140048.png", width=80)
    st.write("## Hola, Norma 👋")
    
    selected = option_menu(
        menu_title="Menú Principal",
        options=["Dashboard", "💰 Finanzas", "💙 MIRA", "🧠 Inteligencia Doc", "🏛️ Alcaldía", "🚀 Numbra"],
        icons=["grid", "cash-coin", "people-fill", "file-earmark-text", "bank", "rocket-takeoff"],
        default_index=1,
    )
    
    st.divider()
    st.info("Versión 5.0 - Control Total")

# --- LÓGICA PRINCIPAL ---

if selected == "Dashboard":
    st.title("🧿 Centro de Comando")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Pendientes MIRA", "3", "Activos")
    col2.metric("Numbra", "Fase 2", "En Proceso")
    col3.metric("Alertas Pago", "2", "Esta semana", delta_color="inverse")
    col4.metric("Energía", "⚡️ Alta", "Estable")

elif selected == "💰 Finanzas":
    st.title("💰 Control Total del Dinero")
    
    # --- SECCIÓN 1: INGRESOS ---
    st.subheader("1. ¿Cuánto entra? (Ingresos)")
    if 'ingresos' not in st.session_state:
        st.session_state['ingresos'] = [
            {"Concepto": "Salario Mensual", "Monto": 0},
            {"Concepto": "Extras / Otros", "Monto": 0},
        ]
    df_ingresos = pd.DataFrame(st.session_state['ingresos'])
    edited_ingresos = st.data_editor(df_ingresos, num_rows="dynamic", use_container_width=True, key="ingresos_table")
    total_ingresos = edited_ingresos["Monto"].sum()
    st.info(f"💰 Total Ingresos: **${total_ingresos:,.0f}**")

    st.divider()

    # --- SECCIÓN 2: COMPROMISOS FIJOS (CON FECHAS) ---
    st.subheader("2. Compromisos Ineludibles (Cuentas por Pagar)")
    st.markdown("Aquí van: Arriendo, Diezmo, Servicios, Ahorro Viaje, Mamá, Tarjetas.")

    if 'compromisos' not in st.session_state:
        # Creamos una fecha por defecto (hoy)
        hoy = date.today()
        st.session_state['compromisos'] = [
            {"Concepto": "Arriendo", "Monto": 0, "Fecha Límite": hoy, "Pagado": False},
            {"Concepto": "Diezmo", "Monto": 0, "Fecha Límite": hoy, "Pagado": False},
            {"Concepto": "Ayuda Mamá", "Monto": 0, "Fecha Límite": hoy, "Pagado": False},
            {"Concepto": "Ahorro Viaje", "Monto": 0, "Fecha Límite": hoy, "Pagado": False},
        ]
    
    df_compromisos = pd.DataFrame(st.session_state['compromisos'])
    
    # Configuración avanzada de la tabla
    edited_compromisos = st.data_editor(
        df_compromisos,
        num_rows="dynamic",
        use_container_width=True,
        key="compromisos_table",
        column_config={
            "Fecha Límite": st.column_config.DateColumn("Fecha Límite", format="DD/MM/YYYY"),
            "Pagado": st.column_config.CheckboxColumn("¿Ya pagué?", help="Marca si ya lo pagaste"),
            "Monto": st.column_config.NumberColumn("Valor a Pagar", format="$%d")
        }
    )

    # --- LÓGICA DE ALERTAS ---
    total_compromisos = edited_compromisos["Monto"].sum()
    pagado_real = edited_compromisos[edited_compromisos["Pagado"] == True]["Monto"].sum()
    pendiente_pagar = total_compromisos - pagado_real

    # Buscamos fechas cercanas para alertar
    hoy = date.today()
    alerta_activa = False
    
    st.write("---")
    st.subheader("🔔 Tablero de Alertas")
    
    # Filtramos solo lo que NO está pagado
    pendientes = edited_compromisos[edited_compromisos["Pagado"] == False]
    
    if not pendientes.empty:
        for index, row in pendientes.iterrows():
            fecha_pago = row["Fecha Límite"]
            # Convertir a fecha si es necesario (pandas a veces usa timestamp)
            if isinstance(fecha_pago, pd.Timestamp): fecha_pago = fecha_pago.date()
                
            dias_restantes = (fecha_pago - hoy).days
            
            if dias_restantes < 0:
                st.error(f"🚨 **¡URGENTE!** El pago de **{row['Concepto']}** está VENCIDO por {abs(dias_restantes)} días.")
                alerta_activa = True
            elif 0 <= dias_restantes <= 5:
                st.warning(f"⚠️ **Atención:** El pago de **{row['Concepto']}** vence en {dias_restantes} días ({fecha_pago}).")
                alerta_activa = True
        
        if not alerta_activa:
            st.success("✅ No tienes vencimientos urgentes en los próximos 5 días.")
    else:
        st.balloons()
        st.success("✨ ¡Felicidades! Has pagado todos tus compromisos.")

    st.divider()

    # --- SECCIÓN 3: LA REALIDAD (SALDO DISPONIBLE) ---
    st.subheader("📊 Tu Realidad Financiera")
    
    disponible_real = total_ingresos - total_compromisos
    
    c1, c2, c3 = st.columns(3)
    c1.metric("Ingresos Totales", f"${total_ingresos:,.0f}")
    c2.metric("Compromisos Totales", f"${total_compromisos:,.0f}", delta_color="inverse")
    
    # Lógica de color para el saldo
    color_saldo = "normal" if disponible_real > 0 else "inverse"
    c3.metric("💰 Disponible para Ti", f"${disponible_real:,.0f}", 
              f"Para transporte, celular y gastos diarios", delta_color=color_saldo)

    # Gráfico de Distribución
    if total_compromisos > 0:
        # Preparamos datos para el gráfico
        datos_grafico = edited_compromisos.copy()
        # Agregamos el saldo disponible como una categoría para ver el total real
        if disponible_real > 0:
            nueva_fila = pd.DataFrame([{"Concepto": "Disponible (Gastos Diarios)", "Monto": disponible_real}])
            datos_grafico = pd.concat([datos_grafico, nueva_fila], ignore_index=True)
            
        fig = px.pie(datos_grafico, values='Monto', names='Concepto', title='¿Cómo se reparte tu pastel?', hole=0.4)
        st.plotly_chart(fig, use_container_width=True)


# --- MÓDULOS RESTANTES (Igual que antes) ---
elif selected == "💙 MIRA":
    st.title("💙 Gestión Política - MIRA")
    if 'mira_data' not in st.session_state:
        st.session_state['mira_data'] = [{"Actividad": "Reunión", "Responsable": "Norma", "Estado": "Pendiente", "Avance": 0}]
    df = pd.DataFrame(st.session_state['mira_data'])
    st.data_editor(df, num_rows="dynamic", use_container_width=True)

elif selected == "🧠 Inteligencia Doc":
    st.title("🧠 Analizador de Documentos")
    uploaded_file = st.file_uploader("PDF", type="pdf")
    if uploaded_file: st.success("Documento cargado.")