import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ESTÉTICA CEI (Rosa y Profesional)
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

# 2. CONEXIÓN TÉCNICA (Batería del Bólido)
try:
    if "GEMINI_API_KEY" in st.secrets:
        genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
        # Usamos el nombre de modelo más estable
        model = genai.GenerativeModel('gemini-1.5-flash')
    else:
        st.error("⚠️ Falta la llave GEMINI_API_KEY en los Secrets de Streamlit.")
except Exception as e:
    st.error(f"Error de conexión: {e}")

st.markdown("---")

# 3. INTERFAZ DE CARGA
foto_inci = st.file_uploader("Subí la foto de la etiqueta (INCI)", type=['jpg', 'jpeg', 'png'])

if foto_inci:
    img = Image.open(foto_inci)
    st.image(img, caption="Etiqueta cargada", use_container_width=True)
    
    if st.button("🔍 EJECUTAR AUDITORÍA QUÍMICA"):
        with st.spinner("El Dr. Nano (IA) está analizando los activos..."):
            try:
                # El prompt específico para Olga y las alumnas
                prompt = """
                Analiza el INCI de esta etiqueta cosmética. 
                1. Lista los principios activos principales.
                2. Indica si contiene ingredientes comedogénicos o irritantes.
                3. Determina para qué biotipo de piel es más adecuado.
                Responde en español y de forma profesional.
                """
                response = model.generate_content([prompt, img])
                
                st.markdown("### 📋 Resultados del Análisis:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error técnico durante el análisis: {e}")
                st.info("Nota: Revisá que tu API Key sea válida y que el modelo gemini-1.5-flash esté habilitado.")

st.markdown("---")
st.caption("Sistema de Respaldo CEI - Gestión Técnica: Fabio")
