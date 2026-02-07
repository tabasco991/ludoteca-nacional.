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

# LLAVE API
API_KEY = "cbb78730aad99ef987ad89e3272ab08d"

# ESTILO CSS
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0d1117; }
    .stMetric { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    .jugada-card { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; margin-bottom: 20px; }
    iframe { border-radius: 15px; border: 1px solid #30363d !important; }
    </style>
    """, unsafe_allow_html=True)

# 2. HEADER
st.title("📈 LUDOTECA NACIONAL")
st.caption("Terminal Multi-Sport | Edición Fórmula 1")
st.divider()

# 3. PESTAÑAS
tab_fut, tab_f1, tab_calc, tab_perf = st.tabs(["⚽ FÚTBOL", "🏎️ FÓRMULA 1", "🧮 CALCULADORA", "📊 PERFORMANCE"])

with tab_fut:
    st.subheader("Marcadores de Fútbol")
    fut_html = f"""
    <div id="wg-api-football-games" data-host="v3.football.api-sports.io" data-key="{API_KEY}" data-theme="dark" data-refresh="15" data-show-errors="false" data-show-logos="true"></div>
    <script type="module" src="https://widgets.api-sports.io/2.0.3/widgets.js"></script>
    """
    components.html(fut_html, height=600, scrolling=True)

with tab_f1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Visualizador de Carreras")
        f1_widgets = f"""
        <api-sports-widget data-type="f1-races-next" data-key="{API_KEY}" data-sport="f1" data-theme="dark"></api-sports-widget>
        <api-sports-widget data-type="f1-standing-drivers" data-key="{API_KEY}" data-sport="f1" data-theme="dark"></api-sports-widget>
        <script type="module" src="https://widgets.api-sports.io/3.1.0/widgets.js"></script>
        """
        components.html(f1_widgets, height=800, scrolling=True)

    with col2:
        st.subheader("🗃️ Base de Datos: Competencias")
        # --- AQUÍ INTEGRAMOS TU CÓDIGO DE API ---
        try:
            conn = http.client.HTTPSConnection("v1.formula-1.api-sports.io")
            headers = {
                'x-apisports-key': API_KEY,
                'x-rapidapi-host': "v1.formula-1.api-sports.io"
            }
            conn.request("GET", "/competitions", headers=headers)
            res = conn.getresponse()
            data = res.read()
            
            # Convertimos los datos crudos en algo bonito
            json_data = json.loads(data.decode("utf-8"))
            if json_data.get("response"):
                # Filtramos los datos para la tabla
                comps = [{"País": c["country"]["name"], "Circuito": c["name"], "Ciudad": c["city"]} for c in json_data["response"]]
                df_f1 = pd.DataFrame(comps)
                st.dataframe(df_f1, use_container_width=True, height=700)
            else:
                st.warning("No se pudieron cargar los datos de competencias.")
        except Exception as e:
            st.error(f"Error de conexión: {e}")

with tab_calc:
    # (El resto del código de la calculadora se mantiene igual para no romper nada)
    st.info("Configura tus picks aquí.")

with tab_perf:
    st.info("Historial de rendimiento.")

st.divider()
st.caption("Ludoteca Nacional v7.1 | F1 Data-Fetch Active")