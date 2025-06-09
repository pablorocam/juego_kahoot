import streamlit as st
import pandas as pd
import random
import os

@st.cache_data
def cargar_preguntas(path_csv):
    df = pd.read_csv(path_csv)
    preguntas_por_imagen = {}
    for _, row in df.iterrows():
        imagen = row['Imagen']
        pregunta = {
            'Pregunta': row['Pregunta'],
            'Correcta': row['Correcta'],
            'Incorrecta1': row['Incorrecta1'],
            'Incorrecta2': row['Incorrecta2'],
            'Incorrecta3': row['Incorrecta3']
        }
        preguntas_por_imagen.setdefault(imagen, []).append(pregunta)
    return list(preguntas_por_imagen.items())

def main():
    st.title("🔁 Relacionar letra ↔ nombre (por imagen)")

    if 'grupo_preguntas' not in st.session_state:
        st.session_state.grupo_preguntas = cargar_preguntas("resources/preguntas_letras.csv")
        st.session_state.indice_imagen = 0
        st.session_state.indice_pregunta = 0
        st.session_state.correctas = 0
        st.session_state.incorrectas = 0
        st.session_state.respondido = False
        st.session_state.respuesta_correcta = ""
        st.session_state.opciones = []
        st.session_state.fue_correcto = None

    grupos = st.session_state.grupo_preguntas

    if st.session_state.indice_imagen >= len(grupos):
        total = st.session_state.correctas + st.session_state.incorrectas
        calificacion = round((st.session_state.correctas / total) * 100, 2) if total else 0
        st.markdown("## 🎉 ¡Juego terminado!")
        st.markdown(f"✅ Aciertos: **{st.session_state.correctas}**")
        st.markdown(f"❌ Errores: **{st.session_state.incorrectas}**")
        st.markdown(f"📊 Calificación final: **{calificacion}%**")

        if st.button("🔁 Reiniciar"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        return

    imagen_actual, preguntas = grupos[st.session_state.indice_imagen]
    pregunta_actual = preguntas[st.session_state.indice_pregunta]

    ruta_imagen = os.path.join("img", imagen_actual)
    if os.path.exists(ruta_imagen):
        st.image(ruta_imagen, caption=f"Imagen {st.session_state.indice_imagen + 1}", use_container_width=True)
    else:
        st.warning(f"No se encontró la imagen: {imagen_actual}")

    st.markdown(f"### {pregunta_actual['Pregunta']}")

    if not st.session_state.opciones:
        opciones = [pregunta_actual["Correcta"],
                    pregunta_actual["Incorrecta1"],
                    pregunta_actual["Incorrecta2"],
                    pregunta_actual["Incorrecta3"]]
        random.shuffle(opciones)
        st.session_state.opciones = opciones
        st.session_state.respuesta_correcta = pregunta_actual["Correcta"]

    if not st.session_state.respondido:
        for opcion in st.session_state.opciones:
            if st.button(opcion, key=f"{st.session_state.indice_imagen}_{st.session_state.indice_pregunta}_{opcion}"):
                st.session_state.respondido = True
                if opcion == st.session_state.respuesta_correcta:
                    st.success("✅ ¡Correcto!")
                    st.session_state.correctas += 1
                    st.session_state.fue_correcto = True
                else:
                    st.error("❌ Incorrecto")
                    st.info(f"💡 La respuesta correcta era: **{st.session_state.respuesta_correcta}**")
                    st.session_state.incorrectas += 1
                    st.session_state.fue_correcto = False

    elif st.session_state.respondido:
        if st.button("➡️ Siguiente pregunta"):
            st.session_state.indice_pregunta += 1
            if st.session_state.indice_pregunta >= len(preguntas):
                st.session_state.indice_imagen += 1
                st.session_state.indice_pregunta = 0
            st.session_state.respondido = False
            st.session_state.opciones = []
            st.session_state.fue_correcto = None
            st.rerun()

