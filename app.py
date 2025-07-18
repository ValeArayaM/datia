import streamlit as st

st.set_page_config(page_title="DATIA - Verificador Offline", page_icon="🧠", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1565C0;'>🧠 DATIA (Modo Offline)</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555;'>Periodismo Inteligente, Información Verificada</h4>", unsafe_allow_html=True)

# Diccionario simple de afirmaciones verificadas con datos y fuentes oficiales
# Puedes ampliar con más datos y fuentes oficiales chilenas
VERIFICACIONES = {
    "gabriel boric ganó la elección presidencial 2021": {
        "veredicto": "VERDADERO",
        "explicacion": "Gabriel Boric ganó la segunda vuelta de la elección presidencial de Chile en 2021 con un 55.87% de los votos según datos oficiales del Servel.",
        "fuentes": [
            "https://www.servel.cl/",
            "https://www.bcn.cl/"
        ]
    },
    "las elecciones presidenciales de 2025 son el 16 de noviembre": {
        "veredicto": "VERDADERO",
        "explicacion": "Las elecciones presidenciales de Chile 2025 están programadas para el domingo 16 de noviembre, según el Servicio Electoral de Chile (Servel).",
        "fuentes": [
            "https://www.servel.cl/",
            "https://www.bcn.cl/"
        ]
    },
    "jose antonio kast está a favor del aborto": {
        "veredicto": "FALSO",
        "explicacion": "José Antonio Kast ha expresado posturas contrarias a la legalización del aborto en Chile, promoviendo posiciones conservadoras.",
        "fuentes": [
            "https://www.elmostrador.cl/",
            "https://www.latercera.com/"
        ]
    },
    # Puedes agregar más entradas aquí
}

def verificar_afirmacion(afirmacion: str):
    af = afirmacion.lower().strip()
    for key, data in VERIFICACIONES.items():
        if key in af:
            return data
    return None

st.subheader("✅ Verificación de declaraciones (Modo Offline)")

afirmacion_usuario = st.text_input("Ingresa la afirmación que deseas verificar:")

if st.button("Verificar"):
    if not afirmacion_usuario.strip():
        st.warning("Por favor, escribe una afirmación.")
    else:
        resultado = verificar_afirmacion(afirmacion_usuario)
        if resultado:
            st.markdown(f"**Veredicto:** {resultado['veredicto']}")
            st.markdown(f"**Explicación:** {resultado['explicacion']}")
            st.markdown("**Fuentes:**")
            for f in resultado['fuentes']:
                st.markdown(f"- [{f}]({f})")
        else:
            st.info("No se encontró información verificable para esta afirmación.")
            st.markdown("""
            Consulta las siguientes fuentes oficiales para verificar datos:
            - [Servicio Electoral de Chile (Servel)](https://www.servel.cl/)
            - [Biblioteca del Congreso Nacional (BCN)](https://www.bcn.cl/)
            - [La Tercera](https://www.latercera.com/)
            - [El Mercurio](https://www.elmercurio.com/)
            - [Emol](https://www.emol.com/)
            """)
