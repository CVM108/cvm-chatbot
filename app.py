import streamlit as st
import pandas as pd
from PIL import Image
import base64
import os

# Configuración de la página con ícono Om y título personalizado
st.set_page_config(
    page_title="Chatbot CVM - Sabiduría Védica",
    page_icon="🕉️",
    layout="centered"
)

# CSS personalizado para estilo védico
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Intenta cargar CSS local (opcional)
try:
    local_css("style.css")
except:
    pass

# Encabezado con logo Om
st.markdown("""
<div style="text-align: center;">
    <h1 style="color: #FFD700; font-family: 'Arial', sans-serif;">
        🕉️ Chatbot CVM 🕉️
    </h1>
    <p style="color: #FFFFFF; font-style: italic;">
        Sabiduría de Srila Prabhupada y las escrituras védicas
    </p>
</div>
""", unsafe_allow_html=True)

try:
    # Intenta cargar el archivo CSV desde diferentes ubicaciones
    try:
        citas = pd.read_csv("citas.csv")
    except FileNotFoundError:
        # Intenta cargar desde GitHub si no lo encuentra localmente
        github_url = "https://raw.githubusercontent.com/CVM108/cvm-chatbot/main/citas.csv"
        citas = pd.read_csv(github_url)
        
    # Verificar que el CSV tenga las columnas correctas
    required_columns = ["pregunta", "respuesta", "fuente"]
    if not all(col in citas.columns for col in required_columns):
        st.error("El formato de citas.csv es incorrecto. Requiere columnas: 'pregunta', 'respuesta', 'fuente'")
        st.stop()

except Exception as e:
    st.error(f"Error al cargar las citas: {str(e)}")
    st.stop()

# Campo de entrada con estilo
with st.container():
    st.markdown("### Haz tu pregunta espiritual")
    pregunta = st.text_input(
        "",
        placeholder="Ej: ¿Quién es Krishna? ¿Qué es el bhakti-yoga?",
        key="pregunta_input"
    )

# Procesamiento de preguntas
if pregunta:
    try:
        # Normalización avanzada de preguntas
        pregunta_limpia = (
            pregunta.lower()
            .strip("¿?¡!.,")
            .replace("quien", "quién")
            .replace("q ", "qué ")
            .replace(" x ", " por ")
        )
        
        # Búsqueda flexible
        mask = (
            citas["pregunta"].str.lower()
            .str.contains(pregunta_limpia, regex=False, na=False)
        )
        respuesta = citas[mask]
        
        # Mostrar resultados
        if not respuesta.empty:
            st.markdown("---")
            st.markdown("### Respuesta divina")
            
            # Mejor coincidencia
            mejor_respuesta = respuesta.iloc[0]
            st.success(f"""
            🕉️ **{mejor_respuesta['respuesta']}**  
            📖 *{mejor_respuesta['fuente']}*
            """)
            
            # Otras respuestas relevantes
            if len(respuesta) > 1:
                st.markdown("#### Otras enseñanzas relacionadas:")
                for idx, row in respuesta[1:].iterrows():
                    st.info(f"• {row['respuesta']} (*{row['fuente']}*)")
        else:
            st.warning("""
            🙏 No encontré una respuesta específica. Intenta con:
            - Preguntas sobre Krishna o Vishnu
            - Dudas sobre karma y reencarnación
            - Consultas sobre Bhagavad-gita
            - Preguntas sobre bhakti-yoga
            """)
            
    except Exception as e:
        st.error(f"Error al procesar: {str(e)}")

# Pie de página védico
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #A9A9A9; font-size: small;">
    <p>Chatbot CVM - Conciencia de Krishna</p>
    <p>Basado en las enseñanzas de Srila Prabhupada</p>
</div>
""", unsafe_allow_html=True)
