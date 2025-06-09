import streamlit as st
from modos import relacion_letras, flashcards, respuesta_libre, juegos_preguntas


st.sidebar.title("Modo de Estudio")

modo = st.sidebar.radio("Selecciona una opción", [
    "🎮 Juego de preguntas",
    "🔁 Relacionar letra ↔ nombre",
    "🧠 Flashcards",
    "✏️ Escribir la respuesta"
])

if modo == "🎮 Juego de preguntas":
    juegos_preguntas.main()

elif modo == "🔁 Relacionar letra ↔ nombre":
    relacion_letras.main()

elif modo == "🧠 Flashcards":
    flashcards.main()

elif modo == "✏️ Escribir la respuesta":
    respuesta_libre.main()
