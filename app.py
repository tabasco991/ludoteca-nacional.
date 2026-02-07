import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Ludoteca Nacional Pro", page_icon="📈", layout="wide")

if 'bitacora' not in st.session_state:
    st.session_state.bitacora = []

# ESTILO CSS
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0d1117; }
    .stMetric { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    .jugada-card {
        background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 2. HEADER
st.title("📈 LUDOTECA NACIONAL")
st.caption("Terminal Elite de Análisis Deportivo")
st.divider()

# 3. PESTAÑAS
tab_mercado, tab_calculadora, tab_analisis = st.tabs(["📡 MARCADORES EN VIVO", "🧮 SMART CALCULATOR", "📊 PERFORMANCE"])

with tab_mercado:
    st.subheader("Marcadores en Tiempo Real")
    
    # --- FIX MAESTRO PARA EL WIDGET ---
    # Usamos el formato de Widget 2.0 que es más compatible con Streamlit
    api_sports_html = """
    <!DOCTYPE html>
    <html>
    <head>
        <script type="module" src="https://widgets.api-sports.io/2.0.3/widgets.js"></script>
    </head>
    <body>
        <div id="wg-api-football-games" 
             data-host="v3.football.api-sports.io" 
             data-key="cbb78730aad99ef987ad89e3272ab08d" 
             data-theme="dark" 
             data-refresh="15" 
             data-show-errors="true" 
             data-show-logos="true"
             data-timezone="America/Los_Angeles">
        </div>
    </body>
    </html>
    """
    
    # Aumentamos la altura a 800 para dar espacio a que cargue
    components.html(api_sports_html, height=800, scrolling=True)

with tab_calculadora:
    col_izq, col_der = st.columns([1, 1])
    with col_izq:
        st.markdown('<div class="jugada-card">', unsafe_allow_html=True)
        nombre = st.text_input("Nombre del Pick:", "Ej: Real Madrid ML")
        monto = st.number_input("Inversión ($):", min_value=1.0, value=100.0)
        momio = st.number_input("Momio:", min_value=1.01, value=1.90, step=0.05)
        prob_est = st.slider("Tu Confianza (%):", 5, 95, 50)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_der:
        total = monto * momio
        utilidad = total - monto
        st.metric("Cobro Potencial", f"${total:.2f}", f"+${utilidad:.2f} Neto")
        
        if st.button("💾 REGISTRAR Y COPIAR"):
            resumen = f"📌 PICK: {nombre} | Momio: {momio} | Inversión: ${monto} | Cobro: ${total:.2f}"
            st.session_state.bitacora.append({
                "Fecha": datetime.now().strftime("%H:%M"),
                "Evento": nombre,
                "Inversión": monto,
                "Momio": momio,
                "Ganancia_Pot": utilidad
            })
            st.code(resumen)
            st.toast("Guardado!")

with tab_analisis:
    if st.session_state.bitacora:
        df = pd.DataFrame(st.session_state.bitacora)
        st.area_chart(df, x="Fecha", y="Ganancia_Pot", color="#00ffcc")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("Registra jugadas para ver el gráfico.")

st.divider()
st.caption("Ludoteca Nacional v6.6 | Fix de Widget Aplicado")