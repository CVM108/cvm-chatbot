import streamlit as st  # Línea 1 corregida
import pandas as pd

# Cargar citas  # Línea 3 corregida
citas = pd.read_csv("citas.csv")

# Interfaz
st.title("Chatbot de Srila Prabhupada 🕉️")  # Línea 6 corregida
pregunta = st.text_input("Haz tu pregunta espiritual:")  # Línea 7 corregida

if pregunta:
    respuesta = citas[citas["pregunta"].str.contains(pregunta, case=False)]  # Línea 9 corregida
    if not respuesta.empty:  # Línea 10 corregida
        st.success(f"**Respuesta:** {respuesta.iloc[0]['respuesta']} (*{respuesta.iloc[0]['fuente']}*)")  # Línea 11 corregida
    else:
        st.warning("Por favor, pregunta sobre karma, Krishna o bhakti (ejemplos en citas.csv).")  # Línea 13 corregida
