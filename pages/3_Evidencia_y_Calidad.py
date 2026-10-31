import streamlit as st
import pandas as pd
from styles import aplicar_estilo_vice

# Configuración inicial (Única)
st.set_page_config(page_title="Dashboard GTA VI", layout="wide")

# Aplica la atmósfera unificada
aplicar_estilo_vice()

# Inyección Visual Unificada Vice City
st.markdown("""
<style>
    /* 1. Transparencia universal en gráficos Plotly */
    .stPlotlyChart, div[data-testid="stPlotlyChart"] > div {
        background-color: transparent !important;
    }
    /* 2. Fondo ambiental con degradado radial */
    .stApp {
        background: radial-gradient(circle at 50% -20%, #1a0536 0%, #05020a 60%, #020105 100%) !important;
        background-attachment: fixed !important;
    }
    /* 3. Menú lateral (Sidebar) con degradado nocturno */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0d061f 0%, #05020a 100%) !important;
        border-right: 1px solid rgba(139, 0, 255, 0.2) !important;
    }
    /* 4. Resplandor en desplegables de filtro (select / multiselect) */
    div[data-baseweb="select"] > div {
        background-color: #0d071e !important;
        border: 1px solid rgba(0, 243, 255, 0.3) !important;
        border-radius: 8px !important;
        box-shadow: 0 0 10px rgba(0, 243, 255, 0.15) !important;
    }
    /* 5. Etiquetas de filtros (tags) con degradado magenta/púrpura y sombra */
    span[data-baseweb="tag"] {
        background: linear-gradient(135deg, #8b00ff 0%, #ff007f 100%) !important;
        border: 1px solid rgba(255, 255, 255, 0.2) !important;
        border-radius: 6px !important;
        box-shadow: 0 2px 8px rgba(139, 0, 255, 0.5) !important;
    }
</style>
""", unsafe_allow_html=True)

st.title("Vista 3: Evidencia y Calidad")
st.caption("¿Qué textos respaldan la lectura y qué tan confiable es la muestra?")

# Carga de datos
@st.cache_data
def load_data():
    return pd.read_excel("data/datos_gta.xlsx", sheet_name="Datos")

df = load_data()

# Normalizar columnas de texto
df['sentimiento'] = df['sentimiento'].astype(str).str.lower().str.strip()

# --- NUEVOS INDICADORES DINÁMICOS ---
st.subheader("Indicadores Clave de la Conversación")

total_registros = len(df)

if total_registros > 0:
    sentimiento_top = df['sentimiento'].mode()[0].capitalize()
    tema_top = df['tema_principal'].mode()[0]
    
    polarizados = len(df[df['sentimiento'].isin(['positivo', 'negativo'])])
    tasa_polaridad = f"{(polarizados / total_registros) * 100:.1f}%"
else:
    sentimiento_top = "N/A"
    tema_top = "N/A"
    tasa_polaridad = "0%"

col1, col2, col3, col4 = st.columns(4)
col1.metric("Volumen Analizado", f"{total_registros} registros")
col2.metric("Sentimiento Predominante", sentimiento_top)
col3.metric("Tema Más Debatido", tema_top)
col4.metric("Tasa de Polaridad", tasa_polaridad, help="Porcentaje de comentarios explícitamente positivos o negativos.")

st.divider()

# --- CONTRAEVIDENCIA Y SEÑALES MIXTAS ---
col_contra, col_limites = st.columns(2)

with col_contra:
    st.subheader("⚠️ Contraevidencia y Riesgos")
    st.error("""
    **Principales Fricciones en la Comunidad:**
    - Preocupación recurrente por la tasa de fotogramas (30 FPS vs 60 FPS) en consolas base.
    - Quejas preventivas sobre el precio estimado de lanzamiento ($70 USD o superior).
    """)

with col_limites:
    st.subheader("📌 Alcance y Limitación de la Muestra")
    st.warning("""
    **Alcance:**
    - Datos recopilados exclusivamente de comentarios públicos de YouTube en trailers oficiales.
    - Etiquetado asistido que requiere validación continua para sarcasmo o ironía.
    """)

st.divider()

# --- FILTROS PRÁCTICOS Y TABLA INTERACTIVA ---
st.subheader("Tabla de Comentarios (Evidencia Cualitativa)")

col_busqueda, col_video, col_tema, col_sent = st.columns([2, 1, 1, 1])

with col_busqueda:
    busqueda = st.text_input("🔍 Buscar texto:", "")

with col_video:
    opciones_video = ["Todos"] + list(df['video'].dropna().unique())
    sel_video = st.selectbox("Video:", opciones_video)

with col_tema:
    opciones_tema = ["Todos"] + list(df['tema_principal'].dropna().unique())
    sel_tema = st.selectbox("Tema Principal:", opciones_tema)

with col_sent:
    opciones_sent = ["Todos"] + list(df['sentimiento'].dropna().unique())
    sel_sent = st.selectbox("Sentimiento:", opciones_sent)

# Filtrado dinámico de la tabla
df_tabla = df.copy()

if busqueda:
    df_tabla = df_tabla[df_tabla['comentario'].astype(str).str.contains(busqueda, case=False, na=False)]

if sel_video != "Todos":
    df_tabla = df_tabla[df_tabla['video'] == sel_video]

if sel_tema != "Todos":
    df_tabla = df_tabla[df_tabla['tema_principal'] == sel_tema]

if sel_sent != "Todos":
    df_tabla = df_tabla[df_tabla['sentimiento'] == sel_sent]

cols_mostrar = ['id_comentario', 'video', 'tema_principal', 'sentimiento', 'comentario']
cols_existentes = [c for c in cols_mostrar if c in df_tabla.columns]

st.dataframe(
    df_tabla[cols_existentes],
    use_container_width=True,
    height=400
)