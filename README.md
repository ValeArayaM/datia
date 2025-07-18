# 🧠 DATIA
**Periodismo Inteligente, Información Verificada**

DATIA es una aplicación web sencilla (hecha con **Python + Streamlit**) orientada a periodistas que necesitan:
- ✅ Verificar declaraciones atribuidas a figuras políticas usando IA (OpenAI) y fuentes oficiales.
- 📜 Consultar resultados históricos de elecciones presidenciales en Chile (incluye 2021).
- 🗳️ Responder correctamente que **las elecciones presidenciales 2025 aún no se han realizado** (según Servel).
- 👤 Ver perfiles con foto de figuras políticas.
- 📊 Mostrar una **simulación de conteo de votos** para demostraciones o presentaciones.

---

## 📦 Contenido del repositorio

```
DATIA/
├── app.py              # Código principal de la app Streamlit
├── requirements.txt    # Dependencias
└── logo_DATIA.png      # Logo (para usar en docs/presentaciones)
```

> **Importante:** Tu clave de OpenAI **NO** se sube al repositorio. Se configura como *secret* dentro de Streamlit Cloud.

---

## 🚀 Ejecución rápida local (5 minutos)

### 1. Clona o descarga este proyecto
```bash
git clone <URL_DE_TU_REPO> datia
cd datia
```

### 2. Crea entorno virtual (opcional pero recomendado)
```bash
python -m venv .venv
source .venv/bin/activate   # En Windows: .venv\Scripts\activate
```

### 3. Instala dependencias
```bash
pip install -r requirements.txt
```

### 4. Configura tu API Key de OpenAI como variable de entorno
**Linux / macOS:**
```bash
export OPENAI_API_KEY="tu_api_key_aqui"
```

**Windows (PowerShell):**
```powershell
setx OPENAI_API_KEY "tu_api_key_aqui"
```

### 5. Ejecuta la app
```bash
streamlit run app.py
```
Abre el enlace que aparece en la terminal (por defecto: http://localhost:8501).

---

## ☁️ Publicar GRATIS en Streamlit Cloud (10-15 min)

### Paso 0 – Requisitos previos
- Cuenta en **GitHub** (gratis) → https://github.com/join
- Cuenta en **Streamlit Cloud** (entra con GitHub) → https://streamlit.io/cloud
- Clave **OpenAI API Key** → https://platform.openai.com/api-keys

### Paso 1 – Sube los archivos a GitHub
1. Inicia sesión en GitHub.
2. Crea un repositorio nuevo (ej: `datia`).
3. Sube: `app.py`, `requirements.txt`, `logo_DATIA.png`, y este README.

### Paso 2 – Crear la app en Streamlit Cloud
1. Ve a https://share.streamlit.io/ (o desde streamlit.io/cloud → "New app").
2. Conecta tu cuenta de GitHub si es la primera vez.
3. Selecciona el repositorio `datia` y la rama `main`.
4. En *Main file path* escribe: `app.py`.
5. Haz clic en **Deploy**.

### Paso 3 – Configurar tu API Key en Streamlit Secrets
1. Una vez desplegada, abre la sección **Settings → Secrets**.
2. Pega esto:
   ```
   OPENAI_API_KEY = "tu_api_key_aqui"
   ```
3. Guarda. Streamlit reiniciará la app con la clave disponible.

---

## 🧠 Cómo usar DATIA

### 🟢 Verificador DATIA
1. Ve a la pestaña **"Verificador DATIA"**.
2. Escribe una afirmación como: `¿Kast dijo que eliminaría el IVA?`
3. Haz clic en **Verificar con DATIA**.
4. La respuesta será un bloque JSON con:
   - veredicto (VERDADERO, FALSO, PARCIAL, NO_VERIFICABLE)
   - explicación breve
   - fuentes oficiales (Servel, BCN, medios confiables — nunca redes sociales)

### 🟢 Consulta Histórica
Pregunta: `resultados presidenciales 2021` o `qué pasa con 2025`.
- Si pregunta por **2021**, muestra resultados oficiales de segunda vuelta (Boric vs Kast).  
- Si pregunta por **2025**, DATIA responde que aún no se han realizado; programadas el **16 de noviembre 2025** (Servel).

### 🟢 Perfiles
Selecciona un nombre y verás foto + espacio para info oficial.

### 🟢 Simulación
Haz clic en **Iniciar simulación** para mostrar un conteo progresivo de votos (demo). Útil para presentaciones universitarias.

---

## 🔒 Privacidad / Buenas prácticas
- No publiques tu API Key en GitHub.
- Usa *Streamlit Secrets* para credenciales.
- Si usarás datos electorales reales, respeta la licencia y cita la fuente (Servel).

---

## 📚 Fuentes oficiales útiles
- Servicio Electoral de Chile (Servel) – resultados oficiales y calendario electoral. 
- Biblioteca del Congreso Nacional (BCN) – fichas históricas de elecciones.
- Diario Oficial / Ministerios – declaraciones y documentos oficiales.
- Medios chilenos reconocidos (CNN Chile, 24Horas, La Tercera, Emol) como apoyo secundario.

---

## 🧾 Datos usados en esta demo

**Elección Presidencial Chile 2021 (segunda vuelta, 19 dic 2021)**  
Gabriel Boric: 55.87% (4,621,231 votos)  
José Antonio Kast: 44.14% (3,650,662 votos)  
Fuente: Centro de Datos Servel; compilado en BCN.  

**Elecciones Presidenciales 2025**  
A la fecha indicada en este proyecto, la elección **aún no se realiza**. Fecha programada: **domingo 16 de noviembre 2025** (Servel).

---

## ❓ Problemas comunes

**La app dice que falta la API Key de OpenAI.**  
→ Ve a *Settings → Secrets* en Streamlit Cloud y agrega `OPENAI_API_KEY = "..."`.

**La app no carga / error de dependencias.**  
→ Revisa que `requirements.txt` esté en la raíz del repo y contenga `streamlit` y `openai`.

**Me aparece un JSON raro / error de formato**  
→ El modelo a veces devuelve texto extra. Copia el JSON entre llaves `{}`.

---

## 📄 Licencia
Uso educativo / demostración. Reemplaza datos e imágenes según tus necesidades.

---

**Hecho contigo por DATIA.** ✨
