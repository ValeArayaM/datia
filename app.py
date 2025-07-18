import streamlit as st
from openai import OpenAI

# ------------------------------------------------------------------
# CONFIGURACIÓN GENERAL DE LA APP
# ------------------------------------------------------------------
st.set_page_config(page_title="DATIA", page_icon="🧠", layout="wide")

# Branding
st.markdown("<h1 style='text-align: center; color: #1565C0;'>🧠 DATIA</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555;'>Periodismo Inteligente, Información Verificada</h4>", unsafe_allow_html=True)

# Inicializar cliente OpenAI
client = OpenAI()

# ------------------------------------------------------------------
# DATOS HISTÓRICOS SERVEL (1970–2021)
# ------------------------------------------------------------------
RESULTADOS_SERVEL = {
    1970: {
        "Salvador Allende": "36.61%",
        "Jorge Alessandri": "35.27%",
        "Radomiro Tomic": "28.11%"
    },
    1989: {
        "Patricio Aylwin": "55.17%",
        "Hernán Büchi": "29.40%",
        "Francisco Javier Errázuriz": "15.43%"
    },
    1993: {
        "Eduardo Frei Ruiz-Tagle": "57.98%",
        "Arturo Alessandri": "24.40%",
        "José Piñera": "6.18%"
    },
    1999: {
        "Ricardo Lagos": "51.31%",
        "Joaquín Lavín": "48.69%"
    },
    2005: {
        "Michelle Bachelet": "53.50%",
        "Sebastián Piñera": "46.50%"
    },
    2009: {
        "Sebastián Piñera": "51.61%",
        "Eduardo Frei Ruiz-Tagle": "48.39%"
    },
    2013: {
        "Michelle Bachelet": "62.16%",
        "Evelyn Matthei": "37.83%"
    },
    2017: {
        "Sebastián Piñera": "54.57%",
        "Alejandro Guillier": "45.43%"
    },
    2021: {
        "Gabriel Boric": "55.87%",
        "José Antonio Kast": "44.13%"
    }
}

ELECCIONES = [
    1970,
    "1973 (Golpe de Estado)",
    1989,
    1993,
    1999,
    2005,
    2009,
    2013,
    2017,
    2021,
    2025,
]

# ------------------------------------------------------------------
# FUNCIÓN AUXILIAR: PROMPT PARA VERIFICADOR
# ------------------------------------------------------------------
def build_verifier_prompt(afirmacion: str) -> str:
    return f"""
Eres DATIA, un asistente de fact-checking diseñado para periodistas en Chile.
Tu trabajo: verificar declaraciones atribuidas a figuras políticas.
Reglas estrictas:
- Usa solo FUENTES OFICIALES o MEDIOS PERIODÍSTICOS CONFIABLES (ej: Servel, BCN, Diario Oficial, ministerios, medios nacionales reconocidos).
- NO cites redes sociales (X/Twitter, Facebook, Instagram, TikTok) como fuente primaria.
- Si la pregunta es sobre resultados de las elecciones presidenciales 2025, responde que AÚN NO SE HAN REALIZADO. Las elecciones están programadas para el 16 de noviembre de 2025 según Servel.
- Si la pregunta es sobre resultados de elecciones pasadas (ej. 2021), usa los datos oficiales de Servel.
- Si no encuentras evidencia suficiente en fuentes legítimas, devuelve veredicto NO_VERIFICABLE.

Afirmación a verificar: '{afirmacion}'

Devuelve SOLO un JSON válido con los campos:
- veredicto: VERDADERO | FALSO | PARCIAL | NO_VERIFICABLE
- explicacion: breve (máx 80 palabras), clara y neutral periodísticamente.
- fuentes: lista de 2 a 5 URLs oficiales o de medios confiables.
"""

# ------------------------------------------------------------------
# PESTAÑAS DE LA APP
# ------------------------------------------------------------------
tabs = st.tabs(["✅ Verificador DATIA", "📜 Consulta Histórica"])

# ------------------------------------------------------------------
# TAB 1: VERIFICADOR
# ------------------------------------------------------------------
with tabs[0]:
    st.subheader("✅ Verificación de declaraciones")
    afirmacion = st.text_input("Escribe la afirmación que deseas verificar:")
    if st.button("Verificar con DATIA"):
        if not afirmacion.strip():
            st.warning("Por favor, ingresa una afirmación.")
        else:
            try:
                with st.spinner("DATIA verificando fuentes oficiales..."):
                    prompt = build_verifier_prompt(afirmacion)
                    response = client.chat.completions.create(
                        model="gpt-4o-mini",
                        messages=[{"role": "user", "content": prompt}],
                        temperature=0.2,
                        max_tokens=500,
                    )
                    salida = response.choices[0].message.content.strip()
                    st.code(salida, language="json")
            except Exception as e:
                st.error(f"Error al llamar a OpenAI: {e}")

# ------------------------------------------------------------------
# TAB 2: CONSULTA HISTÓRICA (SERVEL)
# ------------------------------------------------------------------
with tabs[1]:
    st.subheader("📜 Consulta histórica de elecciones presidenciales en Chile")
    seleccion = st.selectbox("Selecciona el evento:", ELECCIONES)

    if st.button("Consultar resultados"):
        if seleccion == 2025:
            st.warning("🗳️ Las elecciones presidenciales de 2025 aún no se han realizado. Están programadas para el domingo 16 de noviembre de 2025 (fuente: Servel).")
        elif seleccion == "1973 (Golpe de Estado)":
            st.write("📜 **Golpe de Estado en Chile (11 de septiembre de 1973)**")
        else:
            st.write(f"📊 **Resultados oficiales Elección Presidencial {seleccion}:**")
            resultados = RESULTADOS_SERVEL[seleccion]
            for candidato, porcentaje in resultados.items():
                st.write(f"- {candidato}: **{porcentaje}**")
            st.caption("Fuente: Servicio Electoral de Chile (Servel). [Ir al sitio oficial](https://www.servel.cl/)")
