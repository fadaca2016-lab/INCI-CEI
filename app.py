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

# --- CONEXIÓN TÉCNICA (Maniobra de Último Recurso) ---
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    
    # Probamos con este modelo que suele ser el más compatible con v1beta y v1
    # Es el modelo que "siempre está"
    model = genai.GenerativeModel('gemini-1.0-pro-vision-latest')
else:
    st.error("⚠️ No se encontró la llave en los Secrets.")

st.markdown("---")

# --- INTERFAZ ---
foto_inci = st.file_uploader("Subí la foto del INCI", type=['jpg', 'jpeg', 'png'])

if foto_inci:
    img = Image.open(foto_inci)
    st.image(img, caption="Etiqueta cargada", use_container_width=True)
    
    if st.button("EJECUTAR ANALISIS"):
        with st.spinner("El Dr. Nano (IA) buscando activos..."):
            try:
                # Pedido directo y corto para no marear al motor
                response = model.generate_content(["Analiza el INCI de esta imagen. Responde en español.", img])
                
                st.markdown("### 📋 Resultados:")
                st.write(response.text)
                
            except Exception as e:
                st.error(f"Error técnico: {e}")
                st.info("Fabio, si esto falla, es que Google Cloud está restringiendo el acceso por región.")

st.markdown("---")
st.caption("Gestión Técnica: Fabio - CEI 2026")
