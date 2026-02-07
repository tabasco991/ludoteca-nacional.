import streamlit as st
import requests
import random
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN Y ESTILO AVANZADO
st.set_page_config(page_title="Ludoteca Nacional Pro", page_icon="📈", layout="wide")

if 'bitacora' not in st.session_state:
    st.session_state.bitacora = []

st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0d1117; }
    .stMetric { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    .stTabs [data-baseweb="tab-list"] { gap: 8px; }
    .stTabs [data-baseweb="tab"] {
        background-color: #161b22; border-radius: 4px 4px 0px 0px; color: white; padding: 10px 20px;
    }
    .stTabs [aria-selected="true"] { border-bottom: 2px solid #00ffcc !important; }
    .jugada-card {
        background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. HEADER PROFESIONAL
col_h1, col_h2 = st.columns([3, 1])
with col_h1:
    st.title("📈 LUDOTECA NACIONAL")
    st.caption("Sistema de Gestión de Riesgo y Análisis de Mercados Deportivos")
with col_h2:
    st.write(f"**Status:** 🟢 Online \n\n **Fecha:** {datetime.now().strftime('%d/%m/%Y')}")

st.divider()

# 3. CUERPO DE LA APP
tab_mercado, tab_calculadora, tab_analisis = st.tabs(["📡 MERCADO REAL", "🧮 SMART CALCULATOR", "📊 PERFORMANCE"])

with tab_mercado:
    st.subheader("Eventos Sugeridos del Día")
    token = "f28172446a1a46aeb16a4ab8c2311fa4"
    headers = {'X-Auth-Token': token}
    liga = st.selectbox("Cambiar Mercado:", ["Premier League", "La Liga", "Champions League"])
    cods = {"Premier League": "PL", "La Liga": "PD", "Champions League": "CL"}
    
    if st.button("Sincronizar API"):
        url = f"https://api.football-data.org/v4/competitions/{cods[liga]}/matches"
        res = requests.get(url, headers=headers)
        if res.status_code == 200:
            matches = res.json().get('matches', [])[:5]
            for m in matches:
                with st.container():
                    st.markdown(f"""<div style='background:#1c2128; padding:10px; border-radius:5px; margin-bottom:5px;'>
                    <b>{m['homeTeam']['name']} vs {m['awayTeam']['name']}</b><br><small>{m['utcDate'][:10]}</small></div>""", unsafe_allow_html=True)

with tab_calculadora:
    col_izq, col_der = st.columns([1, 1])
    
    with col_izq:
        st.markdown('<div class="jugada-card">', unsafe_allow_html=True)
        st.write("### Definir Jugada")
        nombre = st.text_input("Nombre del Pick:", "Ej: Manchester City ML")
        monto = st.number_input("Inversión ($):", min_value=1.0, value=100.0)
        momio = st.number_input("Momio:", min_value=1.01, value=1.90, step=0.05)
        
        # Lógica de Valor
        prob_est = st.slider("Tu Confianza (%):", 5, 95, 50)
        prob_imp = (1 / momio) * 100
        valor = prob_est - prob_imp
        
        st.markdown('</div>', unsafe_allow_html=True)

    with col_der:
        total = monto * momio
        utilidad = total - monto
        st.metric("Cobro Potencial", f"${total:.2f}", f"+${utilidad:.2f} Neto")
        
        if valor > 0:
            st.success(f"🔥 VALOR POSITIVO: +{valor:.1f}% de ventaja.")
        else:
            st.error(f"⚠️ RIESGO ALTO: {valor:.1f}% debajo del valor.")

        if st.button("💾 REGISTRAR Y COPIAR"):
            resumen = f"📌 PICK: {nombre} | Momio: {momio} | Inversión: ${monto} | Cobro: ${total:.2f}"
            st.session_state.bitacora.append({
                "Fecha": datetime.now().strftime("%H:%M"),
                "Evento": nombre,
                "Inversión": monto,
                "Momio": momio,
                "Ganancia_Pot": utilidad
            })
            st.code(resumen, language="text")
            st.toast("Copiado al portapapeles y guardado")

with tab_analisis:
    st.subheader("Estadísticas de la Sesión")
    if st.session_state.bitacora:
        df = pd.DataFrame(st.session_state.bitacora)
        
        col_res1, col_res2 = st.columns(2)
        with col_res1:
            st.write("#### Crecimiento de Cartera (Simulado)")
            # Gráfica de área para ver la proyección
            df['Acumulado'] = df['Ganancia_Pot'].cumsum()
            st.area_chart(df, x="Fecha", y="Acumulado", color="#00ffcc")
        
        with col_res2:
            st.write("#### Tabla de Registro")
            st.dataframe(df[["Fecha", "Evento", "Inversión", "Momio"]], use_container_width=True)
        
        if st.button("🗑️ Reiniciar Sesión"):
            st.session_state.bitacora = []
            st.rerun()
    else:
        st.info("Registra tu primera jugada para ver el análisis visual.")

st.divider()
st.caption("Ludoteca Nacional v6.0 | Desarrollado para William Tabares")