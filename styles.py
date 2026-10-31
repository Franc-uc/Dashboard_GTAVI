import streamlit as st

def aplicar_estilo_vice():
    st.markdown("""
    <style>
        /* 1. Transparencia universal en gráficos Plotly */
        .stPlotlyChart, div[data-testid="stPlotlyChart"] > div {
            background-color: transparent !important;
        }

        /* 2. Fondo ambiental con halo radial neón en la capa base */
        .stApp {
            background: radial-gradient(circle at 50% -10%, #2d0b5a 0%, #12052b 50%, #05020a 100%) !important;
            background-attachment: fixed !important;
        }

        /* 3. Transparentar capas internas de Streamlit para dejar pasar la luz */
        [data-testid="stAppViewContainer"],
        [data-testid="stHeader"],
        [data-testid="stMain"],
        .main,
        .block-container {
            background: transparent !important;
            background-color: transparent !important;
        }

        /* 4. Sidebar con degradado nocturno */
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #0d061f 0%, #05020a 100%) !important;
            border-right: 1px solid rgba(139, 0, 255, 0.2) !important;
        }

        /* 5. Resplandor en desplegables de filtro */
        div[data-baseweb="select"] > div {
            background-color: #0d071e !important;
            border: 1px solid rgba(0, 243, 255, 0.3) !important;
            border-radius: 8px !important;
            box-shadow: 0 0 10px rgba(0, 243, 255, 0.15) !important;
        }

        /* 6. Etiquetas de filtro (tags) con degradado magenta/púrpura y sombra */
        span[data-baseweb="tag"] {
            background: linear-gradient(135deg, #8b00ff 0%, #ff007f 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 6px !important;
            box-shadow: 0 2px 8px rgba(139, 0, 255, 0.5) !important;
        }
    </style>
    """, unsafe_allow_html=True)



