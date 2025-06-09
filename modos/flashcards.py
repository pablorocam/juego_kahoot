import streamlit as st

def main():
    st.header("🧠 Flashcards")
    st.markdown("**Nombre:** Arteria mediana")

    if st.button("Mostrar ubicación"):
        st.image("img/ejemplo.png", caption="Ubicación de la arteria mediana", use_container_width =True)
