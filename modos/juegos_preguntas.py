import streamlit as st
import pandas as pd
import random

@st.cache_data
def cargar_preguntas(archivo_csv):
    df = pd.read_csv(archivo_csv, encoding='utf-8')
    preguntas = df.to_dict(orient='records')
    random.shuffle(preguntas)
    return preguntas

def main():
    st.markdown("## 🎮 Juego de Preguntas")

    temas_disponibles = {
        "🍞 Carbohidratos": "preguntas_carbohidratos.csv",
        "🥓 Lípidos": "preguntas_lipidos.csv",
        "🫁 Tórax": "preguntas_torax.csv",
        "🧠 Neuro": "preguntas_neuro.csv",
        "💀 Miembro torácico": "preguntas_miembro_toracico.csv",
        "🦵 Estructura y Funcion": "preguntas_EYF.csv",
    }

    tema_seleccionado = st.selectbox("Selecciona un tema:", list(temas_disponibles.keys()))

    if "tema_actual" not in st.session_state or st.session_state.tema_actual != tema_seleccionado:
        st.session_state.tema_actual = tema_seleccionado
        archivo_csv = temas_disponibles[tema_seleccionado]
        st.session_state.preguntas = cargar_preguntas(archivo_csv)
        st.session_state.indice = 0
        st.session_state.correctas = 0
        st.session_state.incorrectas = 0
        st.session_state.respondido = False
        st.session_state.correcta_actual = ""
        st.session_state.fue_correcto = None
        st.session_state.respuestas_ordenadas = []
        st.rerun()

    if st.session_state.indice < len(st.session_state.preguntas):
        pregunta_actual = st.session_state.preguntas[st.session_state.indice]
        st.markdown(f"### Pregunta {st.session_state.indice + 1}: {pregunta_actual['Pregunta']}")

        # Mostrar barra de progreso
        progreso = (st.session_state.indice + 1) / len(st.session_state.preguntas)
        st.progress(progreso, text=f"{int(progreso * 100)}% completado")

        if not st.session_state.respuestas_ordenadas:
            st.session_state.respuestas_ordenadas = [
                pregunta_actual['Correcta'],
                pregunta_actual['Incorrecta1'],
                pregunta_actual['Incorrecta2'],
                pregunta_actual['Incorrecta3']
            ]
            random.shuffle(st.session_state.respuestas_ordenadas)

        if not st.session_state.respondido:
            for r in st.session_state.respuestas_ordenadas:
                if st.button(r, key=f"btn_{st.session_state.indice}_{r}"):
                    st.session_state.correcta_actual = pregunta_actual['Correcta']
                    if r == pregunta_actual['Correcta']:
                        st.session_state.correctas += 1
                        st.session_state.fue_correcto = True
                    else:
                        st.session_state.incorrectas += 1
                        st.session_state.fue_correcto = False
                    st.session_state.respondido = True
                    st.rerun()

        if st.session_state.respondido:
            if st.session_state.fue_correcto:
                st.success("✅ ¡Correcto!")
            else:
                st.error("❌ Incorrecto")
                st.info(f"💡 La respuesta correcta era: **{st.session_state.correcta_actual}**")

            if st.button("➡️ Siguiente pregunta"):
                st.session_state.indice += 1
                st.session_state.respondido = False
                st.session_state.correcta_actual = ""
                st.session_state.fue_correcto = None
                st.session_state.respuestas_ordenadas = []
                if st.session_state.indice >= len(st.session_state.preguntas):
                    st.rerun()

    if st.session_state.indice >= len(st.session_state.preguntas):
        total = st.session_state.correctas + st.session_state.incorrectas
        aciertos = st.session_state.correctas
        errores = st.session_state.incorrectas
        calificacion = round((aciertos / total) * 100, 2)

        st.markdown("## 🎉 ¡Juego terminado!")
        st.progress(1.0, text="100% completado")
        st.markdown(f"- ✅ Aciertos: **{aciertos}**")
        st.markdown(f"- ❌ Errores: **{errores}**")
        st.markdown(f"- 📊 Calificación final: **{calificacion}%**")

        if st.button("🔁 Reiniciar juego"):
            for key in ['preguntas', 'indice', 'correctas', 'incorrectas', 'respondido',
                        'correcta_actual', 'fue_correcto', 'respuestas_ordenadas', 'tema_actual']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()

if __name__ == "__main__":
    main()
