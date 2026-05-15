import streamlit as st
import pandas as pd
from logica import inquilinos_compatibles
from ayudantes import generar_grafico_compatibilidad, generar_tabla_compatibilidad, obtener_id_inquilinos

# Configurar la página para utilizar un layout más amplio.
st.set_page_config(layout="wide")

resultado = None

# Mostrar una gran imagen en la parte superior.
st.image('media/portada.png')
st.write("@diegoparicio")

# Insertar un espacio vertical de 60px
st.markdown(f'<div style="margin-top: 60px;"></div>', unsafe_allow_html=True)

# Configurar el sidebar con inputs y un botón.
with st.sidebar:
    st.header("¿Quién está viviendo en el piso?")
    st.write("Inquilinos actuales. Indique ID: 1-12000")
    inquilino1 = st.text_input("Inquilino 1")
    inquilino2 = st.text_input("Inquilino 2")
    inquilino3 = st.text_input("Inquilino 3")
    
    num_compañeros = st.text_input("¿Cuántos nuevos compañeros quieres buscar?")
    
    if st.button('BUSCAR NUEVOS COMPAÑEROS'):
        # Verifica que el número de compañeros sea un valor válido
        try:
            topn = int(num_compañeros)
        except ValueError:
            st.error("Por favor, ingresa un número válido para el número de compañeros.")
            topn = None