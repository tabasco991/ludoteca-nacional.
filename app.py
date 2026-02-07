import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import http.client
import json
from datetime import datetime

# 1. CONFIGURACIÓN BASE
st.set_page_config(page_title="Ludoteca Nacional Pro", page_icon="📈", layout="wide")

if 'bitacora' not in st.session_state:
    st.session_state.bitacora = []

API_KEY = "cbb78730aad99ef987ad89e3272ab08d"

# ESTILO CSS SEGURO
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] { background-color: #0d1117; }
    .stMetric { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 10px; }
    .jugada-card { background: #161b22; border: 1px solid #30363d; padding: 20px; border-radius: 12px; margin-bottom: 20px; }
    iframe { border-radius: 15px; background: transparent; }
    </style>
    """, unsafe_allow_html=True)

# 2. HEADER
st.title("📈 LUDOTECA NACIONAL")
st.caption("Terminal Multi-Sport | Sistema Restaurado v7.3")
st.divider()

# 3. PESTAÑAS
tab_fut, tab_f1, tab_calc, tab_perf = st.tabs(["⚽ FÚTBOL", "🏎️ FÓRMULA 1", "🧮 CALCULADORA", "📊 PERFORMANCE"])

with tab_fut:
    st.subheader("Marcadores de Fútbol en Vivo")
    # Regresamos al widget más estable que no choca con nada
    fut_html = f"""
    <div id="wg-api-football-games" 
         data-host="v3.football.api-sports.io" 
         data-key="{API_KEY}" 
         data-theme="dark" 
         data-refresh="15" 
         data-show-errors="false" 
         data-show-logos="true">
    </div>
    <script type="module" src="https://widgets.api-sports.io/2.0.3/widgets.js"></script>
    """
    components.html(fut_html, height=600, scrolling=True)

with tab_f1:
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Próximas Carreras")
        # Widget visual de F1
        f1_visual = f"""
        <api-sports-widget data-type="f1-races-next" data-key="{API_KEY}" data-sport="f1" data-theme="dark"></api-sports-widget>
        <script type="module" src="https://widgets.api-sports.io/3.1.0/widgets.js"></script>
        """
        components.html(f1_visual, height=450)

    with col2:
        st.subheader("Clasificación de Pilotos")
        f1_standings = f"""
        <api-sports-widget data-type="f1-standing-drivers" data-key="{API_KEY}" data-sport="f1" data-theme="dark"></api-sports-widget>
        <script type="module" src="https://widgets.api-sports.io/3.1.0/widgets.js"></script>
        """
        components.html(f1_standings, height=450)
    
    st.divider()
    st.subheader("🏁 Base de Datos de Competencias")
    # Usamos un bloque "try" más fuerte para que no rompa el Fútbol si esto falla
    try:
        conn = http.client.HTTPSConnection("v1.formula-1.api-sports.io")
        headers = {'x-apisports-key': API_KEY, 'x-rapidapi-host': "v1.formula-1.api-sports.io"}
        conn.request("GET", "/competitions", headers=headers)
        res = conn.getresponse()
        data = res.read().decode("utf-8")
        json_data = json.loads(data)
        
        if json_data.get("response"):
            lista = []
            for c in json_data["response"]:
                # Verificamos cada campo con cuidado
                nombre = c.get("name", "N/A")
                pais = c.get("country", {}).get("name", "Global") if c.get("country") else "N/A"
                ciudad = c.get("city", "N/A")
                lista.append({"GP": nombre, "País": pais, "Ciudad": ciudad})
            
            st.dataframe(pd.DataFrame(lista), use_container_width=True)
    except Exception as e:
        st.warning("La base de datos de F1 está en mantenimiento, pero los widgets de arriba deberían cargar.")

with tab_calc:
    st.write("### Panel de Picks")
    st.info("La calculadora está lista para recibir tus jugadas.")

with tab_perf:
    st.write("### Rendimiento")
    if st.session_state.bitacora:
        st.table(pd.DataFrame(st.session_state.bitacora))
    else:
        st.write("Registra jugadas en la pestaña de calculadora.")