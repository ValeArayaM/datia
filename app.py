import streamlit as st
import time
import random
import requests

# Configuración general
st.set_page_config(page_title="DATIA", page_icon="🧠", layout="wide")

st.markdown("<h1 style='text-align: center; color: #1565C0;'>🧠 DATIA</h1>", unsafe_allow_html=True)
st.markdown("<h4 style='text-align: center; color: #555;'>Periodismo Inteligente, Información Verificada</h4>", unsafe_allow_html=True)

CANDIDATOS = {
    "Gabriel Boric": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/59/Gabriel_Boric_portrait_2022.jpg/440px-Gabriel_Boric_portrait_2022.jpg",
    "José Antonio Kast": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Jos%C3%A9_Antonio_Kast_2020.jpg/440px-Jos%C3%A9_Antonio_Kast_2020.jpg",
    "Yasna Provoste": "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5b/Yasna_Provoste_2018.jpg/440px-Yasna_Provoste_2018.jpg",
    "Franco Parisi": "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6f/Franco_Parisi_2021.jpg/440px-Franco_Parisi_2021.jpg",
}

RESULTADOS_2021 = {
    "Gabriel Boric": {"porcentaje": 55.87, "votos": 4621231},
    "José Antonio Kast": {"porcentaje": 44.14, "votos": 3650662},
}

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

HF_TOKEN = st.secrets["HF_TOKEN"_]()_
