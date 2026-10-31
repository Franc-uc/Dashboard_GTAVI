import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from styles import aplicar_estilo_vice

st.set_page_config(page_title="Dashboard GTA VI", layout="wide")

# Aplica la atmósfera unificada en una sola línea
aplicar_estilo_vice()

st.title("Vista 2: Temas y Comparaciones")
st.caption("¿Qué temas y videos explican la señal?")

# Cargar los datos
@st.cache_data
def load_data():
    return pd.read_excel("data/datos_gta.xlsx", sheet_name="Datos")

df = load_data()

# Normalizar texto de sentimientos y unificar variantes ("neutral" -> "neutro")
df['sentimiento'] = df['sentimiento'].astype(str).str.lower().str.strip()
df['sentimiento'] = df['sentimiento'].replace({'neutral': 'neutro'})

# --- FILTROS EN BARRA LATERAL ---
st.sidebar.header("Filtros de Análisis")

# 1. Filtro por Video
lista_videos = ["Todos"] + list(df['video'].dropna().unique())
sel_video = st.sidebar.selectbox("Filtrar por Video:", lista_videos)

# 2. Filtro por Tema Principal
lista_temas = list(df['tema_principal'].dropna().unique())
sel_temas = st.sidebar.multiselect("Filtrar por Tema(s):", lista_temas, default=lista_temas)

# Aplicar lógica de filtrado sobre el DataFrame
df_filtrado = df.copy()

if sel_video != "Todos":
    df_filtrado = df_filtrado[df_filtrado['video'] == sel_video]

if sel_temas:
    df_filtrado = df_filtrado[df_filtrado['tema_principal'].isin(sel_temas)]

# --- TÍTULO QUE INTERPRETA ---
st.info("📊 **Lectura Interpretativa:** El interés de la comunidad se concentra predominantemente en el mapa y apartado gráfico; sin embargo, el volumen de comentarios varía significativamente según el tema y el video analizado.")

total_comentarios = len(df_filtrado)

if sel_video == "Todos":
    st.markdown(f"### 🎬 Analizando: **Todos los Videos** `({total_comentarios} comentarios totales)`")
else:
    st.markdown(f"### 🎬 Analizando: **{sel_video}** `({total_comentarios} comentarios filtrados)`")

st.divider()

# --- LAYOUT DE GRÁFICOS ---
col_left, col_right = st.columns(2)

with col_left:
    st.subheader("Ranking de Temas Más Discutidos")
    df_ranking = df_filtrado.groupby('tema_principal').size().reset_index(name='menciones')
    df_ranking = df_ranking.sort_values(by='menciones', ascending=True)
    
    # Gráfico de barras con degradado usando escala de color continua
    fig_ranking = px.bar(
        df_ranking,
        x='menciones',
        y='tema_principal',
        orientation='h',
        text='menciones',
        color='menciones', 
        color_continuous_scale=['#ff007f', '#00f3ff'], # Rosa a Cian
        labels={'menciones': 'Nº de Menciones', 'tema_principal': 'Tema'},
        template='plotly_dark'
    )
    
    fig_ranking.update_coloraxes(showscale=False)
    fig_ranking.update_traces(textposition='outside')
    st.plotly_chart(fig_ranking, use_container_width=True)

with col_right:
    st.subheader("Volumen de Menciones por Sentimiento")
    
    df_sent_count = df_filtrado.groupby('sentimiento').size().reset_index(name='menciones')
    
    # Gráfico Anular con colores Vice City ajustados
    fig_sent = px.pie(
        df_sent_count,
        names='sentimiento',
        values='menciones',
        color='sentimiento',
        hole=0.6,
        template='plotly_dark',
        color_discrete_map={
            'positivo': '#00f3ff', 
            'negativo': '#ff7b00', 
            'neutro': '#7000ff'
        }
    )
    
    fig_sent.update_traces(
        textinfo='label+value+percent',
        textposition='outside'
    )
    
    fig_sent.update_layout(
        showlegend=False
    )
    
    st.plotly_chart(fig_sent, use_container_width=True)

st.divider()

# --- DISTRIBUCIÓN POR VIDEO Y SENTIMIENTO (Skyline GTA VI) ---
st.subheader("Mapa Jerárquico de Sentimiento por Video (Estilo Vice City Skyline)")

df_group = df_filtrado.groupby(['video', 'sentimiento']).size().reset_index(name='menciones')
total_menciones = df_group['menciones'].sum()

NEON_CFG = {
    'positivo': {'top': '#00f3ff', 'glow': 'rgba(0, 243, 255, 0.4)'},
    'negativo': {'top': '#ff7b00', 'glow': 'rgba(255, 123, 0, 0.4)'}, # Actualizado a Naranja
    'neutro':   {'top': '#7000ff', 'glow': 'rgba(112, 0, 255, 0.4)'}  # Actualizado a Morado
}

html_code = """
<style>
.skyline-container { display: flex; gap: 12px; width: 100%; background-color: transparent; padding: 16px; border-radius: 10px; border: 1px solid rgba(255, 255, 255, 0.1); box-sizing: border-box; }
.building-group { display: flex; flex-direction: column; gap: 8px; background: rgba(11, 6, 24, 0.6); border: 1px solid rgba(31, 17, 61, 0.8); border-radius: 8px; padding: 10px; box-shadow: inset 0 0 20px rgba(0,0,0,0.8); flex: 1; overflow: hidden; }
.building-title { color: #d1c4e9; font-family: sans-serif; font-weight: bold; font-size: 12px; letter-spacing: 1px; text-transform: uppercase; white-space: nowrap; text-overflow: ellipsis; overflow: hidden; text-align: center; }
.building-blocks { display: flex; gap: 6px; height: 180px; align-items: flex-end; }
.building-block { border-radius: 5px 5px 2px 2px; display: flex; flex-direction: column; justify-content: space-between; padding: 8px 4px; box-sizing: border-box; transition: transform 0.2s ease; flex: 1; overflow: hidden; }
.block-label { color: #ffffff; font-size: 11px; font-weight: bold; font-family: sans-serif; text-shadow: 0 1px 3px rgba(0,0,0,0.9); text-align: center; white-space: nowrap; text-overflow: ellipsis; overflow: hidden; }
.block-val { color: rgba(255,255,255,0.85); font-size: 10px; font-weight: 600; font-family: sans-serif; text-align: center; white-space: nowrap; text-overflow: ellipsis; overflow: hidden; }
</style>
<div class="skyline-container">
"""

videos = df_group['video'].unique()

for v in videos:
    df_v = df_group[df_group['video'] == v]
    v_total = df_v['menciones'].sum()

    html_code += f'<div class="building-group">'
    html_code += f'<div class="building-title">{v} ({v_total})</div>'
    html_code += '<div class="building-blocks">'

    for _, row in df_v.iterrows():
        sent = row['sentimiento']
        count = row['menciones']
        pct = (count / v_total) * 100 if v_total > 0 else 0
        cfg = NEON_CFG.get(sent, {'top': '#7000ff', 'glow': 'rgba(112, 0, 255, 0.4)'})
        
        grad = f"linear-gradient(180deg, {cfg['top']} 0%, rgba(18, 9, 43, 0.8) 85%)"
        shadow = f"0 -4px 10px {cfg['glow']}"
        border_top = f"3px solid {cfg['top']}"
        
        altura = max(25, pct)
        
        html_code += f'<div class="building-block" style="height: {altura}%; background: {grad}; box-shadow: {shadow}; border-top: {border_top};"><span class="block-label">{sent}</span><span class="block-val">{count} ({pct:.1f}%)</span></div>'

    html_code += '</div></div>'

html_code += '</div>'

st.markdown(html_code, unsafe_allow_html=True)