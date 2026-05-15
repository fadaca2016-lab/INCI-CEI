import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- ESTÉTICA CEI (Rosa y Profesional) ---
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

# --- CONEXIÓN TÉCNICA (Forzando la Versión Estable) ---
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=api_key)
    # Definimos el modelo por fuera para que sea más limpio
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ Falta la llave GEMINI_API_KEY en los Secrets.")

st.markdown("---")

# --- INTERFAZ ---
foto_inci = st.file_uploader("Subí la foto de la etiqueta (INCI)", type=['jpg', 'jpeg', 'png'])

if foto_inci:
    img = Image.open(foto_inci)
    st.image(img, caption="Etiqueta cargada", use_container_width=True)
    
    if st.button("EJECUTAR ANALISIS"):
        with st.spinner("Buscando activos..."):
            try:
                # Maniobra de seguridad: enviamos el contenido como una lista simple
                response = model.generate_content(["Analiza el INCI de esta etiqueta cosmética. Responde en español.", img])
                
                st.markdown("### 📋 Resultados:")
                st.write(response.text)
                
            except Exception as e:
                # Si esto falla, mostramos el error exacto para ver si cambió
                st.error(f"Error del motor: {e}")
                st.info("Fabio, si sigue el 404, el problema es el 'surtidor' (Google Cloud) y no el bólido.")

st.markdown("---")
st.caption("Gestión Técnica: Fabio - CEI 2026")
