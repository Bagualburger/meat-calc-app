import streamlit as st
from PIL import Image
import pandas as pd

# Configuración ultra liviana
st.set_page_config(page_title="MeatCalc Pro", page_icon="🥩")

if 'piezas' not in st.session_state:
    st.session_state.piezas = []

st.title("🥩 MeatCalc Pro")
st.write("Ingresa el monto de la etiqueta manualmente para un cálculo exacto.")

# Entrada manual rápida (mientras arreglamos el sensor automático)
with st.form("add_form", clear_on_submit=True):
    monto = st.number_input("Monto total de la etiqueta ($)", min_value=0, step=1)
    submit = st.form_submit_button("Añadir Pieza")
    
    if submit and monto > 0:
        st.session_state.piezas.append(monto)
        st.success(f"¡Pieza de ${monto:,} añadida!")

# Lógica de Factura
if st.session_state.piezas:
    total_bruto = sum(st.session_state.piezas)
    neto = total_bruto / 1.19
    iva = neto * 0.19
    retencion = neto * 0.05
    total_final = neto + iva + retencion

    st.divider()
    st.subheader(f"Resumen: {len(st.session_state.piezas)} piezas")
    
    col1, col2 = st.columns(2)
    col1.metric("NETO", f"${int(neto):,}")
    col1.metric("IVA (19%)", f"${int(iva):,}")
    col2.metric("RETENCIÓN (5%)", f"${int(retencion):,}")
    col2.metric("TOTAL A PAGAR", f"${int(total_final):,}")

    if st.button("Vaciar Carrito"):
        st.session_state.piezas = []
        st.rerun()
