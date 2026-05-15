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

# --- CONEXIÓN TÉCNICA (La Maniobra Maestra) ---
if "GEMINI_API_KEY" in st.secrets:
    # Usamos transport='rest' para forzar a que no use la v1beta que falla
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"], transport='rest')
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    st.error("⚠️ No encontré la GEMINI_API_KEY en los Secrets.")

st.markdown("---")

# --- INTERFAZ ---
foto_inci = st.file_uploader("Subí la foto del INCI", type=['jpg', 'jpeg', 'png'])

if foto_inci:
    img = Image.open(foto_inci)
    st.image(img, caption="Etiqueta cargada", use_container_width=True)
    
    if st.button("EJECUTAR ANALISIS"):
        with st.spinner("El Dr. Nano (IA) analizando..."):
            try:
                # Pedido directo
                response = model.generate_content(["Analiza los activos de este INCI. Responde en español.", img])
                
                st.markdown("### 📋 Resultados:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error del motor: {e}")
                st.info("Fabio, si sigue el 404, revisá que la clave en Secrets sea EXACTAMENTE la que generaste.")

st.markdown("---")
st.caption("Gestión Técnica: Fabio - CEI 2026")
