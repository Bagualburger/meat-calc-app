import streamlit as st

st.set_page_config(page_title="MeatCalc Pro", page_icon="🥩")

# Título
st.title("🥩 MeatCalc Pro")
st.write("Versión estable para iPhone")

# Inicializar lista si no existe
if 'piezas' not in st.session_state:
    st.session_state.piezas = []

# Entrada de datos simple
monto_input = st.number_input("Monto de la etiqueta ($)", min_value=0, step=1, value=0)

# Botón directo (sin Form)
if st.button("➕ AÑADIR PIEZA"):
    if monto_input > 0:
        st.session_state.piezas.append(monto_input)
        st.success(f"Agregado: ${monto_input:,}")
    else:
        st.warning("Ingresa un monto mayor a 0")

# Cálculos y Resumen
if st.session_state.piezas:
    st.divider()
    total_bruto = sum(st.session_state.piezas)
    neto = total_bruto / 1.19
    iva = neto * 0.19
    retencion = neto * 0.05
    total_final = neto + iva + retencion

    st.subheader(f"Total: {len(st.session_state.piezas)} piezas")
    
    # Mostrar lista de lo que vas sumando
    with st.expander("Ver detalle de piezas"):
        for i, p in enumerate(st.session_state.piezas):
            st.write(f"Pieza {i+1}: ${p:,}")

    # Cuadro de resultados
    st.info(f"**NETO:** ${int(neto):,}")
    st.info(f"**IVA (19%):** ${int(iva):,}")
    st.info(f"**RETENCIÓN (5%):** ${int(retencion):,}")
    st.success(f"### **TOTAL A PAGAR: ${int(total_final):,}**")

    if st.button("🗑️ Vaciar todo"):
        st.session_state.piezas = []
        st.rerun()
