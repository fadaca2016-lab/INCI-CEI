import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ESTÉTICA CEI
st.set_page_config(page_title="CEI - Analizador INCI", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #fff0f5; }
    .stButton>button { 
        background-color: #ff69b4; color: white; 
        border-radius: 20px; width: 100%; border: none; font-weight: bold; height: 3.5em;
    }
    h1, h2 { color: #d81b60; text-align: center; font-family: 'Helvetica', sans-serif; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>Centro de Estética Integral</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='font-size: 1.2em;'>Analizador de Activos (INCI)</h2>", unsafe_allow_html=True)

# 2. CONEXIÓN TÉCNICA (Rectificación Total)
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("⚠️ Falta la llave GEMINI_API_KEY en los Secrets.")

st.markdown("---")

# 3. INTERFAZ
foto_inci = st.file_uploader("Subí la foto de la etiqueta (INCI)", type=['jpg', 'jpeg', 'png'])

if foto_inci:
    img = Image.open(foto_inci)
    st.image(img, caption="Etiqueta para analizar", use_container_width=True)
    
    if st.button("🔍 EJECUTAR ANALISIS QUÍMICO"):
        with st.spinner("Analizando componentes..."):
            try:
                # ACÁ ESTÁ EL CAMBIO: Usamos 'gemini-1.5-flash' a secas
                # El motor 1.5 es el más nuevo y estable para esto
                model = genai.GenerativeModel('gemini-1.5-flash')
                
                response = model.generate_content([
                    "Analiza el INCI de esta imagen. Lista activos, advertencias y biotipo recomendado.",
                    img
                ])
                
                st.markdown("### 📋 Resultados:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error del motor: {e}")
                st.info("Fabio, si ves un 404 acá, el problema es la versión de la librería en requirements.txt")

st.markdown("---")
st.caption("Gestión Técnica: Fabio - CEI 2026")
