import streamlit as st
import google.generativeai as genai
from PIL import Image

# --- ESTÉTICA CEI ---
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

# --- CONEXIÓN TÉCNICA REFORZADA ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        # Forzamos la configuración
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        
        # PROBAMOS EL MODELO POR SU NOMBRE COMPLETO DE SISTEMA
        # Si este falla, el problema es la API KEY o la Región del servidor
        model = genai.GenerativeModel(model_name="models/gemini-1.5-flash")
    else:
        st.error("⚠️ Error: No encontré la llave en los Secrets.")
except Exception as e:
    st.error(f"Error de configuración: {e}")

st.markdown("---")

# --- INTERFAZ ---
foto_inci = st.file_uploader("Subí la foto de la etiqueta (INCI)", type=['jpg', 'jpeg', 'png'])

if foto_inci:
    img = Image.open(foto_inci)
    st.image(img, caption="Etiqueta cargada", use_container_width=True)
    
    if st.button("EJECUTAR ANALISIS"):
        with st.spinner("Analizando componentes..."):
            try:
                # Prompt directo y sencillo para la primera prueba
                response = model.generate_content(["Analiza el INCI de esta imagen. Responde en español.", img])
                
                st.markdown("### 📋 Resultados:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error del motor: {e}")
                st.info("Sugerencia: Revisá si la API Key tiene restricciones en Google AI Studio.")

st.markdown("---")
st.caption("Gestión Técnica: Fabio - CEI 2026")
