import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import http.client
import json
from datetime import datetime

# 1. CONFIGURACIÓN
st.set_page_config(page_title="Ludoteca Nacional Pro", page_icon="🏎️", layout="wide")

if 'bitacora' not in st.session_state:
    st.session_state.bitacora = []

# TU LLAVE API
API_KEY = "cbb78730aad99ef987ad89e3272ab08d"

# ESTILO CSS
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0d1117; }
    .stMetric { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    .jugada-card { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; margin-bottom: 20px; }
    iframe { border-radius: 15px; }
    </style>
    """, unsafe_allow_html=True)

# 2. HEADER
st.title("📈 LUDOTECA NACIONAL")
st.caption("Terminal Multi-Sport | Estabilidad v7.2")
st.divider()

# 3. PESTAÑAS
tab_fut, tab_f1, tab_calc, tab_perf = st.tabs(["⚽ FÚTBOL", "🏎️ FÓRMULA 1", "🧮 CALCULADORA", "📊 PERFORMANCE"])

with tab_fut:
    st.subheader("Marcadores de Fútbol en Vivo")
    # Widget de Fútbol (Regresamos a la versión que ya te funcionaba)
    fut_html = f"""
    <div id="wg-api-football-games" data-host="v3.football.api-sports.io" data-key="{API_KEY}" data-theme="dark" data-refresh="15" data-show-errors="false" data-show-logos="true"></div>
    <script type="module" src="https://widgets.api-sports.io/2.0.3/widgets.js"></script>
    <style>body {{ background: transparent; margin: 0; }}</style>
    """
    components.html(fut_html, height=650, scrolling=True)

with tab_f1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Visualizador F1")
        f1_widgets = f"""
        <api-sports-widget data-type="f1-races-next" data-key="{API_KEY}" data-sport="f1" data-theme="dark"></api-sports-widget>
        <api-sports-widget data-type="f1-standing-drivers" data-key="{API_KEY}" data-sport="f1" data-theme="dark"></api-sports-widget>
        <script type="module" src="https://widgets.api-sports.io/3.1.0/widgets.js"></script>
        """
        components.html(f1_widgets, height=800, scrolling=True)

    with col2:
        st.subheader("🏁 Circuitos de F1")
        try:
            conn = http.client.HTTPSConnection("v1.formula-1.api-sports.io")
            headers = {{'x-apisports-key': API_KEY, 'x-rapidapi-host': "v1.formula-1.api-sports.io"}}
            conn.request("GET", "/competitions", headers=headers)
            res = conn.getresponse()
            data = res.read()
            json_data = json.loads(data.decode("utf-8"))
            
            if json_data.get("response"):
                lista_limpia = []
                for item in json_data["response"]:
                    # FIX: Verificamos que existan los datos antes de pedirlos
                    pais = item.get("country", {}).get("name", "N/A") if item.get("country") else "N/A"
                    lista_limpia.append({
                        "País": pais,
                        "Circuito": item.get("name", "Desconocido"),
                        "Ciudad": item.get("city", "N/A")
                    })
                
                df_f1 = pd.DataFrame(lista_limpia)
                st.dataframe(df_f1, use_container_width=True, height=600)
            else:
                st.info("Buscando datos de la temporada...")
        except:
            st.error("No se pudo conectar con la base de datos de F1, pero los widgets deberían funcionar.")

with tab_calc:
    # Código de calculadora...
    st.write("Configuración de picks activos.")

with tab_perf:
    if st.session_state.bitacora:
        st.area_chart(pd.DataFrame(st.session_state.bitacora), y="Ganancia_Pot")
    else:
        st.info("Sin datos.")

st.divider()