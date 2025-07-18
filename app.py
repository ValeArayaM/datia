import streamlit as st
import requests
from bs4 import BeautifulSoup
from openai import OpenAI

# ------------------------------------------------------------------
# CONFIGURACIÓN GENERAL DE LA APP
# ------------------------------------------------------------------
st.set_page_config(page_title="DATIA", page_icon="🧠", layout="wide")

# Branding (título + eslogan)
st.markdown("<h1 style='text-align: center; color: #1565C0;'>🧠 DATIA</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555;'>Periodismo Inteligente, Información Verificada</h4>", unsafe_allow_html=True)

# Inicializar cliente OpenAI
client = OpenAI()

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
# FUNCIÓN PARA OBTENER RESULTADOS DE ELECCIONES (Wikipedia)
# ------------------------------------------------------------------
def obtener_resultados_eleccion(anio: int) -> dict:
    url = f"https://es.wikipedia.org/wiki/Elecci%C3%B3n_presidencial_de_Chile_de_{anio}"
    resp = requests.get(url)
    if resp.status_code != 200:
        return {"error": "No se pudo acceder a la página de Wikipedia."}
    
    soup = BeautifulSoup(resp.text, "html.parser")
    
    # Buscar tabla con resultados
    tablas = soup.find_all("table", {"class": "wikitable"})
    resultados = {}
    
    for tabla in tablas:
        filas = tabla.find_all("tr")
        for fila in filas:
            celdas = fila.find_all(["th", "td"])
            if len(celdas) >= 3:
                candidato = celdas[0].get_text(strip=True)
                porcentaje = celdas[-1].get_text(strip=True)
                if "%" in porcentaje:  # Filtrar filas con porcentaje
                    resultados[candidato] = porcentaje
    return resultados

# ------------------------------------------------------------------
# LISTA DE ELECCIONES
# ------------------------------------------------------------------
ELECCIONES = [1970, 1989, 1993, 1999, 2005, 2009, 2013, 2017, 2021, 2025]

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
# TAB 2: CONSULTA HISTÓRICA
# ------------------------------------------------------------------
with tabs[1]:
    st.subheader("📜 Consulta histórica de elecciones presidenciales en Chile")
    anio = st.selectbox("Selecciona el año de la elección:", ELECCIONES)

    if st.button("Consultar resultados"):
        if anio == 2025:
            st.warning("🗳️ Las elecciones presidenciales de 2025 aún no se han realizado. Están programadas para el domingo 16 de noviembre de 2025 (fuente: Servel).")
        else:
            with st.spinner(f"Obteniendo resultados oficiales de {anio}..."):
                datos = obtener_resultados_eleccion(anio)
                if "error" in datos:
                    st.error(datos["error"])
                else:
                    st.write(f"📊 **Resultados oficiales Elección Presidencial {anio}:**")
                    for candidato, porcentaje in datos.items():
                        st.write(f"- {candidato}: **{porcentaje}**")
                    st.caption(f"Fuente: Wikipedia (basado en datos del Servel). [Ver página oficial](https://es.wikipedia.org/wiki/Elección_presidencial_de_Chile_de_{anio})")
