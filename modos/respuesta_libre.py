import streamlit as st

def main():
    st.header("✏️ Escribir la respuesta")
    st.image("img/ejemplo.png", caption="¿Qué estructura está marcada con 'C'?", use_container_width =True)

    respuesta = st.text_input("Escribe tu respuesta:")

    if st.button("Verificar"):
        if respuesta.lower().strip() == "arteria mediana":
            st.success("✅ ¡Correcto!")
        else:
            st.error("❌ Incorrecto. Es 'arteria mediana'.")
