import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

st.set_page_config(page_title="Prueba de Hipotesis", layout="wide")

st.title("App de Prueba de Hipotesis")
st.markdown("Desarrollada para el curso de Probabilidad y Estadistica")

st.sidebar.title("Menu")
seccion = st.sidebar.radio("Selecciona una seccion:", [
    "Inicio",
    "Cargar datos",
    "Visualizacion",
    "Prueba Z",
    "Asistente IA"
], key="menu")

if seccion == "Inicio":
    st.header("Bienvenida")
    st.write("Esta aplicacion permite:")
    st.write("- Cargar o generar datos estadisticos")
    st.write("- Visualizar su distribucion")
    st.write("- Realizar pruebas de hipotesis Z")
    st.write("- Consultar un asistente de IA para interpretar resultados")

elif seccion == "Cargar datos":
    st.header("Cargar datos")
    opcion = st.radio("Como quieres ingresar los datos?", ["Subir CSV", "Generar datos sinteticos"])

    if opcion == "Subir CSV":
        archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
        if archivo:
            df = pd.read_csv(archivo)
            st.session_state["datos"] = df
            st.success("Archivo cargado correctamente")
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

elif seccion == "Visualizacion":
    st.header("Visualizacion de datos")

    if "datos" not in st.session_state:
        st.warning("Primero debes cargar o generar datos en la seccion Cargar datos")
    else:
        df = st.session_state["datos"]
        columna = df.columns[0]
        datos = df[columna]

        st.subheader("Estadisticas basicas")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Media", f"{datos.mean():.4f}")
        col2.metric("Desv. estandar", f"{datos.std():.4f}")
        col3.metric("Minimo", f"{datos.min():.4f}")
        col4.metric("Maximo", f"{datos.max():.4f}")

        st.subheader("Histograma")
        fig1, ax1 = plt.subplots(figsize=(4, 2))
        ax1.hist(datos, bins=20, edgecolor="black", color="steelblue", density=True)
        xmin, xmax = ax1.get_xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.norm.pdf(x, datos.mean(), datos.std())
        ax1.plot(x, p, "r", linewidth=2, label="Curva normal")
        ax1.set_xlabel("Valor")
        ax1.set_ylabel("Densidad")
        ax1.set_title("Histograma con curva normal")
        ax1.legend()
        st.pyplot(fig1, use_container_width=False)

        st.subheader("Boxplot")
        fig2, ax2 = plt.subplots(figsize=(2, 0.5))
        ax2.boxplot(datos, vert=False)
        ax2.set_xlabel("Valor")
        ax2.set_title("Boxplot de los datos")
        st.pyplot(fig2)

        st.subheader("Analisis de la distribucion")
        skewness = datos.skew()
        if abs(skewness) < 0.5:
            st.write("La distribucion parece aproximadamente normal (sesgo bajo).")
        elif skewness > 0:
            st.write("La distribucion tiene sesgo positivo (cola hacia la derecha).")
        else:
            st.write("La distribucion tiene sesgo negativo (cola hacia la izquierda).")

        q1 = datos.quantile(0.25)
        q3 = datos.quantile(0.75)
        iqr = q3 - q1
        outliers = datos[(datos < q1 - 1.5 * iqr) | (datos > q3 + 1.5 * iqr)]
        st.write(f"Outliers detectados: {len(outliers)}")