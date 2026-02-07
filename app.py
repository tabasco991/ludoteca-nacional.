import streamlit as st
import requests
import random
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN Y ESTILO
st.set_page_config(page_title="Ludoteca Nacional | Pro", page_icon="🏟️", layout="wide")

# Inicializar la bitácora en la memoria de la sesión si no existe
if 'bitacora' not in st.session_state:
    st.session_state.bitacora = []

st.markdown("""
    <style>
    .main { background-color: #0d1117; color: white; }
    .gadget-box {
        background: linear-gradient(145deg, #161b22, #0d1117);
        border: 1px solid #30363d;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.3);
    }
    .metric-value { color: #00ffcc; font-size: 28px; font-weight: bold; font-family: 'Courier New', monospace; }
    .status-online { color: #3fb950; font-size: 14px; animation: blinker 2s linear infinite; }
    @keyframes blinker { 50% { opacity: 0; } }
    .match-card {
        background: #1c2128;
        border-radius: 10px;
        padding: 15px;
        margin-bottom: 12px;
        border-left: 4px solid #00ffcc;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. ENCABEZADO
st.markdown("""
    <div style="background-color: #161b22; padding: 15px; border-radius: 10px; border-bottom: 3px solid #00ffcc; margin-bottom: 25px; text-align: center;">
        <h1 style="margin: 0; color: #f0f6fc; letter-spacing: 3px;">🏟️ LUDOTECA NACIONAL</h1>
        <span class="status-online">● TERMINAL DE INTELIGENCIA ESTRATÉGICA</span>
    </div>
    """, unsafe_allow_html=True)

# 3. GADGETS SUPERIORES
col_a, col_b, col_c, col_d = st.columns(4)
with col_a:
    st.markdown(f'<div class="gadget-box"><small>VOLUMEN MERCADO</small><br><span class="metric-value">2.1M</span><br><small style="color:#8b949e;">USD 24H</small></div>', unsafe_allow_html=True)
with col_b:
    st.markdown(f'<div class="gadget-box"><small>PARTIDOS HOY</small><br><span class="metric-value">18</span><br><small style="color:#8b949e;">Ligas Activas</small></div>', unsafe_allow_html=True)
with col_c:
    st.markdown(f'<div class="gadget-box"><small>EFICIENCIA</small><br><span class="metric-value" style="color:#00ffcc;">68%</span><br><small style="color:#8b949e;">Algoritmo v5</small></div>', unsafe_allow_html=True)
with col_d:
    st.markdown(f'<div class="gadget-box"><small>HORA LOCAL</small><br><span class="metric-value">{datetime.now().strftime("%H:%M")}</span><br><small style="color:#8b949e;">Sync Global</small></div>', unsafe_allow_html=True)

st.write("---")

# 4. PESTAÑAS
tab_live, tab_betting, tab_history = st.tabs(["🔥 MERCADO", "🧮 CÁLCULO & VALOR", "📝 BITÁCORA DE SESIÓN"])

with tab_live:
    col_m, col_s = st.columns([2, 1])
    with col_m:
        st.subheader("📡 Feed de Partidos Real-Time")
        token = "f28172446a1a46aeb16a4ab8c2311fa4"
        headers = {'X-Auth-Token': token}
        liga = st.selectbox("Mercado:", ["Premier League", "La Liga", "Champions League", "Serie A"])
        cods = {"Premier League": "PL", "La Liga": "PD", "Champions League": "CL", "Serie A": "SA"}
        
        if st.button("ACTUALIZAR CARTELERA"):
            url = f"https://api.football-data.org/v4/competitions/{cods[liga]}/matches"
            res = requests.get(url, headers=headers)
            if res.status_code == 200:
                matches = res.json().get('matches', [])[:6]
                for m in matches:
                    st.markdown(f"""<div class="match-card">
                        <small>{m['utcDate'][:10]}</small><br>
                        <b>{m['homeTeam']['name']} vs {m['awayTeam']['name']}</b>
                    </div>""", unsafe_allow_html=True)

    with col_s:
        st.subheader("🔍 Smart Tips")
        st.info("El algoritmo detecta alta probabilidad de goles en la Premier League hoy.")
        st.write("Presión de Venta:")
        st.progress(random.randint(20, 80))

with tab_betting:
    st.subheader("⚙️ Análisis de Valor")
    c1, c2 = st.columns(2)
    
    with c1:
        st.write("### Calculadora de Entrada")
        nombre_jugada = st.text_input("Etiqueta de la jugada (Ej: Real Madrid ML)", "Nueva Jugada")
        bet_amt = st.number_input("Inversión ($)", value=100.0)
        odd_val = st.number_input("Momio Decimal", value=2.00, step=0.05)
        
        # Lógica del Semáforo
        prob_implicita = (1 / odd_val) * 100
        prob_real = st.slider("Tu probabilidad estimada (%)", 10, 90, 50)
        
        st.write(f"Probabilidad Implicada del Momio: **{prob_implicita:.1f}%**")
        
        if prob_real > prob_implicita:
            st.success(f"🟢 VALOR DETECTADO: Tienes un ventaja del {(prob_real - prob_implicita):.1f}%")
        elif abs(prob_real - prob_implicita) < 5:
            st.warning("🟡 RIESGO EQUILIBRADO: El momio es justo.")
        else:
            st.error("🔴 SIN VALOR: El riesgo es mayor al pago.")

    with c2:
        st.write("### Retorno Esperado")
        ganancia = bet_amt * odd_val
        st.metric("Total a Cobrar", f"${ganancia:.2f}", f"+${ganancia-bet_amt:.2f}")
        
        if st.button("📥 REGISTRAR EN BITÁCORA"):
            nueva_fila = {
                "Hora": datetime.now().strftime("%H:%M:%S"),
                "Jugada": nombre_jugada,
                "Inversión": f"${bet_amt:.2f}",
                "Momio": odd_val,
                "Cobro Potencial": f"${ganancia:.2f}",
                "Ventaja": f"{(prob_real - prob_implicita):.1f}%"
            }
            st.session_state.bitacora.append(nueva_fila)
            st.balloons()
            st.toast("¡Jugada guardada en la bitácora!")

with tab_history:
    st.subheader("📝 Registro de Sesión (Hoy)")
    if st.session_state.bitacora:
        df = pd.DataFrame(st.session_state.bitacora)
        st.table(df)
        if st.button("Limpiar Bitácora"):
            st.session_state.bitacora = []
            st.rerun()
    else:
        st.write("Aún no has registrado jugadas en esta sesión.")

st.write("---")
st.caption(f"Ludoteca Nacional v5.0 | {datetime.now().strftime('%Y-%m-%d')} | Terminal Protegida")