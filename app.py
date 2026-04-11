import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.set_page_config(page_title="Prueba de Hipótesis", layout="wide")

st.title("App de Prueba de Hipótesis")
st.markdown("Desarrollada para  Probabilidad y Estadística")

st.sidebar.title("Menú")
seccion = st.sidebar.radio("Selecciona una sección:", [
    " Inicio",
    " Cargar datos",
    " Visualización",
    " Prueba Z",
    " Asistente de IA"
])

if seccion == " Inicio":
    st.header("Bienvenido")
    st.write("Esta aplicación permite:")
    st.write("- Cargar o generar datos estadísticos")
    st.write("- Visualizar su distribución")
    st.write("- Realizar pruebas de hipótesis Z")
    st.write("- Consultar un asistente de IA para interpretar resultados")