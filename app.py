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

HF_TOKEN = st.secrets["HF_TOKEN"]

def llamar_hf_chat(prompt: str) -> str:
    API_URL = "https://api-inference.huggingface.co/models/microsoft/DialoGPT-small"
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Accept": "application/json"
    }
    payload = {
        "inputs": prompt,
        "parameters": {"max_new_tokens": 200, "temperature": 0.7},
        "options": {"wait_for_model": True}
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        data = response.json()
        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        else:
            return str(data)
    else:
        return f"Error Hugging Face API: {response.status_code} {response.text}"

tabs = st.tabs(["✅ Verificador DATIA", "📜 Consulta Histórica", "👤 Perfiles", "📊 Simulación"])

with tabs[0]:
    st.subheader("✅ Verificación de declaraciones")
    afirmacion = st.text_input("Escribe la afirmación que deseas verificar:")
    if st.button("Verificar con DATIA"):
        if not afirmacion.strip():
            st.warning("Por favor, ingresa una afirmación.")
        else:
            with st.spinner("DATIA verificando fuentes oficiales con Hugging Face..."):
                prompt = build_verifier_prompt(afirmacion)
                respuesta = llamar_hf_chat(prompt)
                st.code(respuesta, language="json")

with tabs[1]:
    st.subheader("📜 Consulta histórica de elecciones en Chile")
    q = st.text_input("Pregunta (ej: 'resultados 2021', 'qué pasa con 2025'):", key="histq")
    if st.button("Consultar historia", key="histq_btn"):
        qlow = q.lower()
        if "2025" in qlow:
            st.warning("🗳️ Las elecciones presidenciales de 2025 aún no se han realizado. Están programadas para el domingo 16 de noviembre de 2025 (fuente: Servel).")
        elif "2021" in qlow or "última" in qlow or "ultima" in qlow:
            st.write("📊 **Resultados oficiales Elección Presidencial 2021 (Segunda vuelta - 19 diciembre 2021):**")
            for c, data in RESULTADOS_2021.items():
                st.write(f"- {c}: **{data['porcentaje']}%** ({data['votos']:,} votos)")
            st.caption("Fuente: Servicio Electoral de Chile (Servel) / Biblioteca del Congreso Nacional (BCN).")
        else:
            st.info("Por ahora DATIA entrega datos históricos de la elección presidencial 2021 y el estado programado de la elección 2025.")

with tabs[2]:
    st.subheader("👤 Perfiles oficiales de figuras políticas")
    cand = st.selectbox("Selecciona un candidato:", list(CANDIDATOS.keys()))
    if cand:
        st.image(CANDIDATOS[cand], width=250)
        st.write(f"**Nombre:** {cand}")
        st.write("**Perfil oficial:** (Agrega aquí información verificada de fuentes oficiales).")

with tabs[3]:
    st.subheader("📊 Simulación en tiempo real (DEMO)")
    st.write("Simula un conteo de mesas escrutadas para demostración. No representa datos reales.")
    candidatos = list(CANDIDATOS.keys())
    votos = {c: 0 for c in candidatos}
    total_mesas = 5000
    mesas_contadas = 0
    placeholder = st.empty()
    if st.button("Iniciar simulación"):
        while mesas_contadas < total_mesas:
            mesas_contadas += 200
            if mesas_contadas > total_mesas:
                mesas_contadas = total_mesas
            for c in candidatos:
                votos[c] += random.randint(2000, 7000)
            total_votos = sum(votos.values())
            porcentajes = {c: (v / total_votos) * 100 for c, v in votos.items()}
            with placeholder.container():
                st.metric("Mesas escrutadas", f"{mesas_contadas}/{total_mesas}", f"{(mesas_contadas/total_mesas)*100:.2f}%")
                st.bar_chart(porcentajes)
                for c, p in sorted(porcentajes.items(), key=lambda x: x[1], reverse=True):
                    st.write(f"{c}: **{p:.2f}%** ({votos[c]:,} votos)")
            time.sleep(0.75)
        st.success("Conteo simulado finalizado ✅")
