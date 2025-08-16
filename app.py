import streamlit as st
import pandas as pd

# Configuración de la página
st.set_page_config(
    page_title="Chatbot CVM - Sabiduría Védica",
    page_icon="🕉️",
    layout="centered"
)

# CSS personalizado
st.markdown("""
<style>
.stButton>button {
    background-color: #FFD700;
    color: #000000;
    border-radius: 5px;
    border: 1px solid #FFD700;
    padding: 0.5rem 1rem;
}
.stButton>button:hover {
    background-color: #FFC000;
    color: #000000;
    border: 1px solid #FFC000;
}
</style>
""", unsafe_allow_html=True)

# Encabezado
st.markdown("""
<div style="text-align: center;">
    <h1 style="color: #FFD700;">🕉️ Chatbot CVM 🕉️</h1>
    <p style="color: #FFFFFF; font-style: italic;">
        Sabiduría de Srila Prabhupada y las escrituras védicas
    </p>
</div>
""", unsafe_allow_html=True)

# Cargar datos
@st.cache_data
def load_data():
    try:
        citas = pd.read_csv("citas.csv")
        required_columns = ["pregunta", "respuesta", "fuente"]
        if all(col in citas.columns for col in required_columns):
            return citas
        else:
            st.error("Formato de citas.csv incorrecto")
            return None
    except Exception as e:
        st.error(f"Error al cargar citas: {str(e)}")
        return None

citas = load_data()
if citas is None:
    st.stop()

# Estado de la sesión
if 'show_new_question' not in st.session_state:
    st.session_state.show_new_question = False

# Función para reiniciar
def reset_question():
    st.session_state.show_new_question = True
    st.session_state.pregunta = ""

# Formulario de pregunta
with st.form("pregunta_form"):
    st.markdown("## Haz tu pregunta espiritual")
    pregunta = st.text_input(
        "Escribe tu pregunta sobre conciencia de Krishna:",
        placeholder="Ej: ¿Quién es Krishna? ¿Qué es el bhakti-yoga?",
        key="pregunta"
    )
    submitted = st.form_submit_button("Enviar pregunta")

# Procesar pregunta
if submitted and pregunta:
    try:
        pregunta_limpia = pregunta.lower().strip("¿?¡!.,")
        mask = citas["pregunta"].str.lower().str.contains(pregunta_limpia, regex=False, na=False)
        respuesta = citas[mask]
        
        if not respuesta.empty:
            st.markdown("---")
            st.markdown("## Respuesta divina")
            
            mejor_respuesta = respuesta.iloc[0]
            st.success(f"""
            🕉️ **{mejor_respuesta['respuesta']}**  
            📖 *{mejor_respuesta['fuente']}*
            """)
            
            if len(respuesta) > 1:
                st.markdown("#### Otras enseñanzas relacionadas:")
                for idx, row in respuesta[1:].iterrows():
                    st.info(f"• {row['respuesta']} (*{row['fuente']}*)")
            
            # Botón para nueva pregunta
            st.markdown("---")
            if st.button("🔄 Hacer otra pregunta", on_click=reset_question):
                st.experimental_rerun()
                
        else:
            st.warning("""
            🙏 No encontré respuesta específica. Intenta con:
            - Preguntas sobre Krishna/Vishnu
            - Dudas sobre karma
            - Consultas sobre Bhagavad-gita
            - Preguntas sobre bhakti-yoga
            """)
            
            # Botón para reintentar
            if st.button("🔄 Intentar con otra pregunta", on_click=reset_question):
                st.experimental_rerun()
                
    except Exception as e:
        st.error(f"Error al procesar: {str(e)}")

# Pie de página
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #A9A9A9; font-size: small;">
    <p>Chatbot CVM - Conciencia de Krishna</p>
    <p>Basado en las enseñanzas de Srila Prabhupada</p>
</div>
""", unsafe_allow_html=True)
