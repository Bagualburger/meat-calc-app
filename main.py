import streamlit as st
import easyocr
import numpy as np
from PIL import Image
import re

st.set_page_config(page_title="MeatCalc Pro", page_icon="🥩")

# Carga el lector una sola vez y lo guarda en memoria
@st.cache_resource
def load_reader():
    return easyocr.Reader(['es'], gpu=False)

reader = load_reader()

if 'datos' not in st.session_state:
    st.session_state.datos = [] # Guardaremos tuplas de (peso, monto)

st.title("🥩 MeatCalc Pro: Automático")

# Captura de foto
foto = st.camera_input("Enfoca la etiqueta de cerca")

if foto:
    with st.spinner("Procesando etiqueta..."):
        img = Image.open(foto)
        img_np = np.array(img)
        
        # El OCR lee la imagen
        resultados = reader.readtext(img_np)
        texto_completo = " ".join([res[1] for res in resultados])
        
        # BUSCAR MONTO: Busca números de 4 o 5 dígitos precedidos por $ o espacios
        montos = re.findall(r'\$\s?(\d+\.?\d+)', texto_completo)
        # BUSCAR PESO: Busca números que terminen en 'kg'
        pesos = re.findall(r'(\d[.,]\d{3})\s?kg', texto_completo.lower())

        if montos:
            # Limpiar puntos del monto y convertir a int
            monto_detectado = int(montos[0].replace('.', ''))
            peso_detectado = pesos[0] if pesos else "0,000"
            
            # Evitar duplicados si la cámara se queda pegada
            nueva_pieza = {"peso": peso_detectado, "monto": monto_detectado}
            st.session_state.datos.append(nueva_pieza)
            st.success(f"✅ ¡Detectado! Peso: {peso_detectado}kg | Monto: ${monto_detectado:,}")

# MOSTRAR RESULTADOS
if st.session_state.datos:
    st.divider()
    df = st.session_state.datos
    total_bruto = sum(d['monto'] for d in df)
    total_kg = sum(float(d['peso'].replace(',', '.')) for d in df)
    
    neto = total_bruto / 1.19
    retencion = neto * 0.05
    total_final = neto + (neto * 0.19) + retencion

    st.write(f"### Resumen de {len(df)} piezas")
    st.write(f"**Peso acumulado:** {total_kg:.3f} kg")
    
    c1, c2 = st.columns(2)
    c1.metric("NETO", f"${int(neto):,}")
    c2.metric("RETC. 5%", f"${int(retencion):,}")
    
    st.success(f"## TOTAL A PAGAR: ${int(total_final):,}")

    if st.button("Limpiar todo"):
        st.session_state.datos = []
        st.rerun()
