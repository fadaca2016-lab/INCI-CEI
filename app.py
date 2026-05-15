import streamlit as st
import google.generativeai as genai
from PIL import Image

# 1. ESTÉTICA PROFESIONAL INCI-CEI
st.set_page_config(page_title="INCI-CEI | Analizador Pro", layout="centered")

st.markdown("""
    <style>
    .stApp { background-color: #fff0f5; }
    .stButton>button { 
        background-color: #d81b60; color: white; 
        border-radius: 15px; width: 100%; border: none; font-weight: bold; height: 3.5em;
    }
    h1 { color: #d81b60; text-align: center; font-family: 'Helvetica', sans-serif; }
    h3 { color: #ad1457; }
    .stFileUploader label { color: #ad1457; font-weight: bold; }
    </style>
    """, unsafe_allow_html=True)

st.markdown("<h1>🔬 INCI-CEI</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #ad1457;'>Auditoría técnica de componentes cosméticos para el gabinete</p>", unsafe_allow_html=True)

# 2. CONFIGURACIÓN IA
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
    model = genai.GenerativeModel('gemini-1.5-flash-latest')
else:
    st.error("⚠️ Falta la API KEY en los Secrets de Streamlit Cloud.")

st.markdown("---")

# 3. INTERFAZ DE CARGA
foto = st.file_uploader("Cargá la foto de los ingredientes (INCI):", type=['jpg', 'jpeg', 'png'])

if foto:
    img = Image.open(foto)
    st.image(img, caption="Etiqueta detectada", use_container_width=True)
    
    if st.button("🔍 EJECUTAR AUDITORÍA QUÍMICA"):
        with st.spinner("Analizando componentes..."):
            try:
                prompt = (
                    "Actuá como experto en química cosmética del CEI. "
                    "Analizá el INCI de esta imagen y armá un informe: "
                    "1. TENSIOACTIVOS: Tipo y agresividad. "
                    "2. PRINCIPIOS ACTIVOS: Beneficios según posición en la lista. "
                    "3. VEHÍCULOS Y HUMECTANTES: Calidad de la base. "
                    "4. CONSERVANTES: Presencia de alérgenos o parabenos. "
                    "5. VEREDICTO: ¿Para qué biotipo lo recomienda Olga? "
                )
                res = model.generate_content([prompt, img])
                st.markdown("---")
                st.markdown("### 📋 Resultado del Análisis")
                st.write(res.text)
            except Exception as e:
                st.error(f"Error técnico: {e}")

st.markdown("---")
st.caption("INCI-CEI v1.0 | Fabio & Olga - Centro de Estética Integral")
