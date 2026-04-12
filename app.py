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
        fig2, ax2 = plt.subplots(figsize=(4, 2))
        ax2.boxplot(datos, vert=False)
        ax2.set_xlabel("Valor")
        ax2.set_title("Boxplot de los datos")
        st.pyplot(fig2, use_container_width=False)

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

elif seccion == "Prueba Z":
    st.header("Prueba de hipotesis Z")

    if "datos" not in st.session_state:
        st.warning("Primero debes cargar o generar datos en la seccion Cargar datos")
    else:
        df = st.session_state["datos"]
        datos = df[df.columns[0]]

        st.subheader("Parametros de la prueba")

        mu0 = st.number_input("Hipotesis nula (media poblacional H0)", value=0.0)
        sigma = st.number_input("Desviacion estandar poblacional (sigma)", value=1.0, min_value=0.01)
        alpha = st.selectbox("Nivel de significancia (alpha)", [0.01, 0.05, 0.10])
        tipo = st.radio("Tipo de prueba", ["Bilateral", "Cola izquierda", "Cola derecha"])

        if st.button("Calcular prueba Z"):
            n = len(datos)
            media_muestral = datos.mean()
            z = (media_muestral - mu0) / (sigma / np.sqrt(n))

            if tipo == "Bilateral":
                p_value = 2 * (1 - stats.norm.cdf(abs(z)))
                z_critico = stats.norm.ppf(1 - alpha / 2)
                rechazar = abs(z) > z_critico
            elif tipo == "Cola izquierda":
                p_value = stats.norm.cdf(z)
                z_critico = stats.norm.ppf(alpha)
                rechazar = z < z_critico
            else:
                p_value = 1 - stats.norm.cdf(z)
                z_critico = stats.norm.ppf(1 - alpha)
                rechazar = z > z_critico

            st.subheader("Resultados")
            col1, col2, col3 = st.columns(3)
            col1.metric("Media muestral", f"{media_muestral:.4f}")
            col2.metric("Estadistico Z", f"{z:.4f}")
            col3.metric("p-value", f"{p_value:.4f}")

            if rechazar:
                st.error(f"Se rechaza H0. Hay evidencia suficiente para rechazar la hipotesis nula (alpha={alpha})")
            else:
                st.success(f"No se rechaza H0. No hay evidencia suficiente para rechazar la hipotesis nula (alpha={alpha})")

            st.subheader("Grafica de la prueba")
            fig, ax = plt.subplots(figsize=(6, 3))
            x = np.linspace(-4, 4, 200)
            y = stats.norm.pdf(x)
            ax.plot(x, y, "b", linewidth=2)

            if tipo == "Bilateral":
                ax.fill_between(x, y, where=(x < -z_critico), color="red", alpha=0.4, label="Region de rechazo")
                ax.fill_between(x, y, where=(x > z_critico), color="red", alpha=0.4)
            elif tipo == "Cola izquierda":
                ax.fill_between(x, y, where=(x < z_critico), color="red", alpha=0.4, label="Region de rechazo")
            else:
                ax.fill_between(x, y, where=(x > z_critico), color="red", alpha=0.4, label="Region de rechazo")

            ax.axvline(z, color="green", linestyle="--", linewidth=2, label=f"Z calculado = {z:.4f}")
            ax.set_title("Distribucion normal con region critica")
            ax.legend()
            st.pyplot(fig, use_container_width=False)

            st.session_state["resultados_z"] = {
                "n": n,
                "media_muestral": media_muestral,
                "mu0": mu0,
                "sigma": sigma,
                "alpha": alpha,
                "tipo": tipo,
                "z": z,
                "p_value": p_value,
                "rechazar": rechazar
            }