import streamlit as st
import qrcode
from io import BytesIO
import json


productos = {
    "Detergente Ultra 1L": "DET-001",
    "Detergente Ultra 500ml": "DET-002",
    "Detergente Industrial 5L": "DET-003"
    }


# Configuración de página
st.set_page_config(
    page_title="Generador de QR",
    page_icon="📦",
    layout="wide"
)

st.title("Generador de QR para Inventario 📦")
st.subheader("Sistema interno para generación de etiquetas")

st.divider()

# Layout en columnas
col1, col2 = st.columns([1,1])

with col1:

    st.subheader("Datos del producto")

    nombre = st.selectbox(
        "Seleccione el producto",
        list(productos.keys())
    )

    producto = productos[nombre]

    lote = st.text_input(
        "Lote",
        placeholder="Ej: L45"
    )

    fecha_fab = st.date_input("Fecha de fabricación")
    tiene_exp = st.checkbox("El producto tiene fecha de expiración")

    if tiene_exp:
        fecha_exp = st.date_input("Fecha de expiración")
    else:
        fecha_exp = None

    generar = st.button("Generar QR", use_container_width=True)


## COLUMNA 2: VISTA PREVIA Y DESCARGA
with col2:

    st.subheader("Vista previa")

    # Estado inicial (antes de generar QR)
    if not generar:

        st.markdown('<div class="qr-box">', unsafe_allow_html=True)

        st.info("Aquí aparecerá el código QR generado")

        st.markdown("""
        **Ejemplo de etiqueta**

        Producto: Detergente Ultra 1L  
        SKU: DET-001  
        Lote: L45  
        Fecha: 2026-03-10
        """)

        st.markdown('</div>', unsafe_allow_html=True)

    # Cuando se presiona el botón
    else:

        if producto and nombre and lote:

            data = {
                "producto": producto,
                "nombre": nombre,
                "lote": lote,
                "fecha_fab": fecha_fab.isoformat(),
                "fecha_exp": fecha_exp.isoformat()
            }

            qr_data = json.dumps(data)

            qr = qrcode.make(qr_data)

            buffer = BytesIO()
            qr.save(buffer, format="PNG")

            st.markdown('<div class="qr-box">', unsafe_allow_html=True)

            st.image(buffer, width=250)
            if fecha_exp:
                st.caption(
                    f"Producto: {nombre} | SKU: {producto} | Lote: {lote} | "
                    f"Fecha de fabricación: {fecha_fab} | Fecha de expiración: {fecha_exp}"
                )
            else:
                st.caption(
                    f"Producto: {nombre} | SKU: {producto} | Lote: {lote} | "
                    f"Fecha de fabricación: {fecha_fab} | Sin fecha de expiración"
                )

            st.success("QR generado correctamente")

            st.download_button(
                label="Descargar QR",
                data=buffer.getvalue(),
                file_name=f"{producto}_qr.png",
                mime="image/png",
                use_container_width=True
            )

            st.markdown('</div>', unsafe_allow_html=True)

        else:
            st.warning("Complete todos los campos para generar el QR")