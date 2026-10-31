import streamlit as st
from styles import aplicar_estilo_vice

# 1. Configuración de página
st.set_page_config(page_title="Dashboard GTA VI", page_icon="🌴", layout="wide")

# 2. Aplicar la atmósfera Vice City
aplicar_estilo_vice()

# 3. Título principal
st.markdown("""
<h1 style='text-align: center; color: #ff007f; text-shadow: 0 0 15px rgba(255, 0, 127, 0.8); font-size: 4rem; margin-bottom: 0; text-transform: uppercase; letter-spacing: 2px;'>
    Dashboard GTA VI
</h1>
<h3 style='text-align: center; color: #00f3ff; text-shadow: 0 0 10px rgba(0, 243, 255, 0.6); margin-top: 5px; font-weight: normal; margin-bottom: 30px;'>
    Análisis de Sentimiento de la Comunidad
</h3>
""", unsafe_allow_html=True)

# 4. Imagen de Portada (Lucía y Jason)
# Usamos columnas para que la imagen quede centrada y tenga un ancho elegante (50% de la pantalla)
col_img1, col_img_center, col_img3 = st.columns([1, 2, 1])
with col_img_center:
    try:
        # Asegúrate de que la imagen se llame así y esté en la misma carpeta
        st.image("gta_hero.jpg", use_container_width=True)
    except FileNotFoundError:
        st.warning("⚠️ No se encontró la imagen 'gta_hero.jpg'. Asegúrate de guardarla en la misma carpeta que este script.")

st.divider()

# 5. Texto de introducción
st.markdown("""
### 🎮 Bienvenido al Centro de Comando
Este dashboard interactivo procesa y visualiza las reacciones, expectativas y comentarios de la comunidad frente a los avances del juego. Utiliza el menú lateral para navegar por las distintas secciones analíticas:
""")

st.write("") 

# 6. Tarjetas de presentación para las vistas
col1, col2, col3 = st.columns(3)

with col1:
    st.info("""
    #### 📊 1. Resumen Ejecutivo
    Visión global del impacto. Analiza el volumen total de interacciones, métricas de engagement y la polaridad general.
    """)

with col2:
    st.info("""
    #### 🏙️ 2. Temas y Comparaciones
    Profundiza en lo que la gente habla. Descubre el ranking de temáticas más discutidas y explora el mapa de sentimientos.
    """)

with col3:
    st.info("""
    #### 📈 3. Evidencia y Calidad
    Transparencia de datos. Inspecciona la tabla de comentarios en bruto, aplica filtros específicos y revisa la base.
    """)