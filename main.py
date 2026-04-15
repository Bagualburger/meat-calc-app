import streamlit as st
import easyocr
from PIL import Image
import numpy as np
import re

# Configuración de la App
st.set_page_config(page_title="MeatCalc Pro", page_icon="🥩")
st.title("🥩 MeatCalc Pro: OCR Edition")
st.subheader("Escanea tus etiquetas y calcula la factura")

# Inicializar el lector OCR (Soporta Español e Inglés)
@st.cache_resource
def load_ocr():
    return easyocr.Reader(['es'])

reader = load_ocr()

# Estado de la app (para guardar múltiples piezas)
if 'piezas' not in st.session_state:
    st.session_state.piezas = []

# --- INTERFAZ DE CARGA ---
uploaded_file = st.file_uploader("📷 Toma una foto o sube la etiqueta", type=["jpg", "png", "jpeg"])

if uploaded_file:
    image = Image.open(uploaded_file)
    st.image(image, caption="Etiqueta cargada", width=300)
    
    if st.button("🔍 Escanear y Agregar"):
        # Convertir imagen para OCR
        img_np = np.array(image)
        results = reader.readtext(img_np)
        
        # Lógica para encontrar el precio (Buscamos el número después de "$")
        # O el número más grande que parezca un precio total
        textos = [res[1] for res in results]
        precios_encontrados = []
        
        for t in textos:
            # Limpiar el texto para dejar solo números (maneja puntos y comas)
            limpio = re.sub(r'[^\d]', '', t)
            if limpio and 1000 < int(limpio) < 50000: # Rango normal de una pieza
                precios_encontrados.append(int(limpio))
        
        if precios_encontrados:
            monto = max(precios_encontrados) # El total suele ser el número más grande
            st.session_state.piezas.append(monto)
            st.success(f"Pieza agregada: ${monto:,}")
        else:
            st.error("No se detectó el precio. Intenta con una foto más clara.")

# --- CÁLCULOS TIPO FACTURA ---
if st.session_state.piezas:
    st.divider()
    total_etiquetas = sum(st.session_state.piezas)
    neto = total_etiquetas / 1.19
    iva = neto * 0.19
    retencion = neto * 0.05
    total_final = neto + iva + retencion

    # Mostrar Resumen (Como en tu diseño)
    st.write(f"### RESUMEN FINAL ({len(st.session_state.piezas)} PIEZAS)")
    
    col1, col2 = st.columns(2)
    with col1:
        st.metric("VALOR NETO", f"${int(neto):,}")
        st.metric("IVA (19%)", f"${int(iva):,}")
    with col2:
        st.metric("RETENCIÓN CARNE (5%)", f"${int(retencion):,}")
        st.metric("TOTAL A PAGAR", f"${int(total_final):,}", delta_color="inverse")

    if st.button("🗑️ Borrar lista"):
        st.session_state.piezas = []
        st.rerun()
