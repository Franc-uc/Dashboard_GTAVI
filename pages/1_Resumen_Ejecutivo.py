import streamlit as st
import pandas as pd
import plotly.express as px
import streamlit as st
from styles import aplicar_estilo_vice

st.set_page_config(page_title="Dashboard GTA VI", layout="wide")
# Aplica la atmósfera unificada en una sola línea
aplicar_estilo_vice()


st.title("Vista 1: Resumen Ejecutivo")
st.caption("¿Cuál es la señal principal y qué debería evaluar Rockstar?")

# Carga de datos desde la pestaña correcta
@st.cache_data
def load_data():
    return pd.read_excel("data/datos_gta.xlsx", sheet_name="Datos")

df = load_data()

# 1. Titular del Hallazgo
st.info("💡 **Titular:** La comunidad muestra gran expectativa sobre el mapa y contenido de Vice City, con especial atención a la calidad del video y rendimiento.")

# 2. Indicadores clave (KPIs automáticos con datos reales)
total_menciones = len(df)
total_videos = df['video'].nunique()
pct_positivo = round((df['sentimiento'].str.lower() == 'positivo').mean() * 100, 1)
pct_negativo = round((df['sentimiento'].str.lower() == 'negativo').mean() * 100, 1)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Menciones Totales", f"{total_menciones:,}")
c2.metric("Sentimiento Positivo", f"{pct_positivo}%")
c3.metric("Sentimiento Negativo", f"{pct_negativo}%")
c4.metric("Videos Analizados", total_videos)

st.divider()

# 3. Visual Principal & Evidencia
col_visual, col_detalle = st.columns([2, 1])

with col_visual:
    st.subheader("Comparación Central por Tema Principal")
    
    # Agrupar datos para contar menciones por tema y sentimiento
    df_counts = df.groupby(["tema_principal", "sentimiento"]).size().reset_index(name="conteo")
    
# Gráfico de Barras Horizontales para gestionar diferencias grandes de volumen
    fig = px.bar(
        df_counts,
        y="tema_principal",
        x="conteo",
        color="sentimiento",
        orientation="h",
        text="conteo",
        barmode="stack",  # Puedes cambiar a "group" si prefieres barras separadas
        labels={"tema_principal": "Tema Principal", "conteo": "Nº de Menciones", "sentimiento": "Sentimiento"},
        template="plotly_dark",
        color_discrete_map={"positivo": "#00f3ff", "negativo": "#ff007f", "neutro": "#8b00ff"}
    )
    
    fig.update_traces(textposition="auto")
    fig.update_layout(
        yaxis={'categoryorder': 'total ascending'},  # Ordena automáticamente del tema menor al mayor
        xaxis_title="Nº de Menciones",
        yaxis_title=None
    )
    
    st.plotly_chart(fig, use_container_width=True)

with col_detalle:
    st.subheader("Evidencia y Decisión")
    
    # Extraer un comentario positivo/representativo real
    ejemplo_comentario = df['comentario'].dropna().iloc[0] if not df.empty else "Sin comentarios"
    
    st.warning(f"**Comentario representativo:**\n'{ejemplo_comentario}'")
    st.error("**Decisión y Limitación:**\nPriorizar comunicación técnica previa al lanzamiento. Muestra basada en comentarios públicos de YouTube.")