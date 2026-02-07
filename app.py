import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from datetime import datetime

# 1. CONFIGURACIÓN DE PÁGINA
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
    iframe { border-radius: 15px; border: 1px solid #30363d !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. HEADER
st.title("📈 LUDOTECA NACIONAL")
st.caption("Terminal de Inteligencia Deportiva | API-Sports v3.1.0")
st.divider()

# 3. PESTAÑAS
tab_mercado, tab_calculadora, tab_analisis = st.tabs(["📡 MARCADORES EN VIVO", "🧮 SMART CALCULATOR", "📊 PERFORMANCE"])

with tab_mercado:
    st.subheader("Cartelera de Partidos")
    
    # --- BLOQUE MAESTRO WIDGET v3.1.0 ---
    # Combinamos la visualización, la configuración y el script en un solo bloque HTML
    api_sports_v3_html = """
    <div style="width: 100%; font-family: sans-serif;">
        <api-sports-widget data-type="games"></api-sports-widget>

        <api-sports-widget data-type="config"
            data-key="cbb78730aad99ef987ad89e3272ab08d"
            data-sport="football"
            data-lang="es"
            data-theme="dark"
            data-show-errors="true"
            data-show-logos="true"
            data-favorite="true">
        </api-sports-widget>

        <script type="module" src="https://widgets.api-sports.io/3.1.0/widgets.js"></script>
    </div>
    <style>
        body { background-color: transparent !important; margin: 0; }
        /* Forzar que el widget use el tema oscuro de la API */
        #api-sports-widget { background: #0d1117 !important; }
    </style>
    """
    
    # Ejecutamos el componente
    components.html(api_sports_v3_html, height=850, scrolling=True)

with tab_calculadora:
    col_izq, col_der = st.columns([1, 1])
    with col_izq:
        st.markdown('<div class="jugada-card">', unsafe_allow_html=True)
        nombre = st.text_input("Nombre del Pick:", "Ej: Premier League Multi")
        monto = st.number_input("Inversión ($):", min_value=1.0, value=100.0)
        momio = st.number_input("Momio:", min_value=1.01, value=1.90, step=0.05)
        st.markdown('</div>', unsafe_allow_html=True)

    with col_der:
        total = monto * momio
        st.metric("Cobro Potencial", f"${total:.2f}")
        
        if st.button("💾 REGISTRAR JUGADA"):
            st.session_state.bitacora.append({
                "Fecha": datetime.now().strftime("%H:%M"),
                "Evento": nombre,
                "Inversión": monto,
                "Ganancia_Pot": total - monto
            })
            st.toast("¡Añadido a la bitácora!")

with tab_analisis:
    if st.session_state.bitacora:
        df = pd.DataFrame(st.session_state.bitacora)
        st.area_chart(df, y="Ganancia_Pot", color="#00ffcc")
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No hay datos en esta sesión.")

st.divider()
st.caption("Ludoteca Nacional v6.8 | Powered by API-Sports v3.1.0")