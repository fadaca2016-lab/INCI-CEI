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

# 2. CONEXIÓN TÉCNICA (Motor v3.1 / 2.0 Flash)
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Cambiamos a gemini-2.0-flash que es el motor más moderno y estable hoy
        model = genai.GenerativeModel('gemini-1.5-flash-8b')
    else:
        st.error("⚠️ Falta la llave GEMINI_API_KEY en los Secrets.")
except Exception as e:
    st.error(f"Error de configuración: {e}")

st.markdown("---")

# 3. INTERFAZ
foto_inci = st.file_uploader("Subí la foto de la etiqueta (INCI)", type=['jpg', 'jpeg', 'png'])

if foto_inci:
    img = Image.open(foto_inci)
    st.image(img, caption="Etiqueta para analizar", use_container_width=True)
    
    if st.button("🔍 EJECUTAR ANALISIS"):
        with st.spinner("Conectando con el motor más moderno..."):
            try:
                # Prompt directo para evitar filtros innecesarios
                prompt = "Analiza el INCI de esta imagen. Lista activos y biotipo recomendado."
                
                response = model.generate_content([prompt, img])
                
                st.markdown("### 📋 Resultados:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error del motor: {e}")
                st.info("Fabio, si el error persiste, probá cambiar el nombre del modelo a 'gemini-1.5-flash-latest'")

st.markdown("---")
st.caption("Gestión Técnica: Fabio - CEI 2026")
