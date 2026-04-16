import streamlit as st
from PIL import Image

st.set_page_config(page_title="MeatCalc Pro", page_icon="🥩")

st.title("🥩 MeatCalc Pro")
st.write("Sube la foto de la etiqueta o ingresa el monto.")

if 'piezas' not in st.session_state:
    st.session_state.piezas = []

# --- SECCIÓN DE CARGA (FOTO O MANUAL) ---
tab1, tab2 = st.tabs(["📸 Foto (OCR)", "⌨️ Manual"])

with tab1:
    foto = st.camera_input("Toma foto a la etiqueta")
    if foto:
        st.warning("⚠️ El escaneo automático requiere mucha memoria. Por ahora, mira el monto en la foto y regístralo en la pestaña 'Manual' para evitar que la app se cierre.")

with tab2:
    monto_input = st.number_input("Monto de la etiqueta ($)", min_value=0, step=1, value=0)
    if st.button("➕ AÑADIR PIEZA"):
        if monto_input > 0:
            st.session_state.piezas.append(monto_input)
            st.success(f"Agregado: ${monto_input:,}")

# --- CÁLCULOS ---
if st.session_state.piezas:
    st.divider()
    total_bruto = sum(st.session_state.piezas)
    neto = total_bruto / 1.19
    iva = neto * 0.19
    retencion = neto * 0.05
    total_final = neto + iva + retencion

    st.subheader(f"Total: {len(st.session_state.piezas)} piezas")
    
    st.info(f"**NETO:** ${int(neto):,}")
    st.info(f"**IVA (19%):** ${int(iva):,}")
    st.info(f"**RETENCIÓN (5%):** ${int(retencion):,}")
    st.success(f"### **TOTAL FACTURA: ${int(total_final):,}**")

    if st.button("🗑️ Vaciar todo"):
        st.session_state.piezas = []
        st.rerun()
