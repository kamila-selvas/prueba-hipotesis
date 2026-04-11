import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.set_page_config(page_title="Prueba de Hipotesis", layout="wide")

st.title("App de Prueba de Hipotesis")
st.markdown("Desarrollada para Probabilidad y Estadistica")

st.sidebar.title("Menu")
seccion = st.sidebar.radio("Selecciona una seccion:", [
    "Inicio",
    "Cargar datos",
    "Visualizacion",
    "Prueba Z",
    "Asistente de IA"
])

if seccion == "Inicio":
    st.header("Bienvenida")
    st.write("Esta aplicacion permite:")
    st.write("- Cargar o generar datos estadisticos")
    st.write("- Visualizar su distribucion")
    st.write("- Realizar pruebas de hipotesis Z")
    st.write("- Consultar un asistente de IA para interpretar resultados")

elif seccion == "Cargar datos":
    st.header("Cargar datos")
    opcion = st.radio("Como desea ingresar los datos?", ["Subir CSV", "Generar datos sinteticos"])

    if opcion == "Subir CSV":
        archivo = st.file_uploader("Sube el archivo CSV", type=["csv"])
        if archivo:
            df = pd.read_csv(archivo)
            st.session_state["datos"] = df
            st.success("El archivo se cargó correctamente")
            st.dataframe(df.head())

    elif opcion == "Generar datos sinteticos":
        media = st.number_input("Media de la distribucion", value=0.0)
        desviacion = st.number_input("Desviacion estandar", value=1.0, min_value=0.1)
        n = st.slider("Numero de observaciones", 30, 500, 100)
        if st.button("Generar datos"):
            datos = np.random.normal(loc=media, scale=desviacion, size=n)
            df = pd.DataFrame({"valor": datos})
            st.session_state["datos"] = df
            st.success(f"Se generaron {n} datos con media={media} y desviacion={desviacion}")
            st.dataframe(df.head())