# Cargar citas
citas = pd.read_csv("citas.csv")

# Interfaz
st.title("Chatbot de Srila Prabhupada 💬")
pregunta = st.text_input("Haz tu pregunta espiritual:")

if pregunta:
    pregunta_limpia = pregunta.lower().strip("¿?¡!")  # Normaliza el texto
    respuesta = citas[citas["pregunta"].str.lower().str.contains(pregunta_limpia, regex=False)]
    
    if not respuesta.empty:
        st.success(f"**Respuesta:** {respuesta.iloc[0]['respuesta']} (\"{respuesta.iloc[0]['fuente']}\")")
    else:
        st.warning("Por favor, pregunta sobre karma, Krishna o bhakti (ejemplos en citas.csv).")
