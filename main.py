import streamlit as st
import google.generativeai as genai
from PIL import Image

# Configuración segura: busca la clave en la "caja fuerte" de Streamlit
try:
    # Esta es la línea 8 ahora:
    API_KEY = st.secrets["GEMINI_API_KEY"]
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except Exception as e:
    st.error("Error de Configuración: Revisa los Secrets en Streamlit Cloud.")
    st.stop()

st.set_page_config(page_title="MeatCalc Pro AI", page_icon="🥩")
st.title("🥩 MeatCalc Pro AI")

if 'datos' not in st.session_state:
    st.session_state.datos = []

# Cámara para iPhone
foto = st.camera_input("Enfoca la etiqueta de cerca")

if foto:
    img = Image.open(foto)
    with st.spinner("AI leyendo etiqueta..."):
        prompt = "Analiza la etiqueta. Extrae el PESO en kg (formato X.XXX) y el PRECIO TOTAL. Responde estrictamente así: PESO:X.XXX, PRECIO:XXXX"
        try:
            response = model.generate_content([prompt, img])
            res_text = response.text
            
            # Limpieza de datos recibidos
            peso_str = res_text.split("PESO:")[1].split(",")[0].strip()
            precio_str = res_text.split("PRECIO:")[1].strip()
            monto_int = int(''.join(filter(str.isdigit, precio_str)))
            
            st.session_state.datos.append({"peso": peso_str, "monto": monto_int})
            st.success(f"✅ Registrado: {peso_str}kg | ${monto_int:,}")
        except:
            st.error("No se pudo leer. Intenta una foto más clara.")

# Resultados acumulados
if st.session_state.datos:
    st.divider()
    total_bruto = sum(d['monto'] for d in st.session_state.datos)
    total_kg = sum(float(d['peso'].replace(',', '.')) for d in st.session_state.datos)
    
    neto = total_bruto / 1.19
    iva = neto * 0.19
    retencion = neto * 0.05
    total_final = neto + iva + retencion

    st.metric("PESO TOTAL ACUMULADO", f"{total_kg:.3f} kg")
    
    c1, c2 = st.columns(2)
    c1.metric("NETO", f"${int(neto):,}")
    c2.metric("RETC. CARNE (5%)", f"${int(retencion):,}")
    
    st.success(f"### TOTAL FACTURA: ${int(total_final):,}")

    if st.button("Vaciar Carrito"):
        st.session_state.datos = []
        st.rerun()
