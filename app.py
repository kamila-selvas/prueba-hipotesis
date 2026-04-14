import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats
import google.generativeai as genai

st.set_page_config(page_title="Prueba de Hipotesis", layout="wide", page_icon="📊")

st.markdown("""
<style>
    .stApp {
        background: linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%);
    }
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1a1a2e 0%, #16213e 100%);
        border-right: 1px solid #9b59b6;
    }
    h1, h2, h3 { color: #e040fb !important; }
    [data-testid="stMetric"] {
        background: rgba(155, 89, 182, 0.15);
        border: 1px solid #9b59b6;
        border-radius: 15px;
        padding: 15px;
    }
    .stButton > button {
        background: linear-gradient(90deg, #9b59b6, #e040fb);
        color: white;
        border: none;
        border-radius: 25px;
        padding: 10px 25px;
        font-weight: bold;
        transition: 0.3s;
    }
    .stButton > button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 20px rgba(155, 89, 182, 0.5);
    }
    .stMarkdown, p, label { color: #e8e8e8 !important; }
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background: rgba(255,255,255,0.05);
        border: 1px solid #9b59b6;
        border-radius: 10px;
        color: white;
    }
    .header-container {
        background: linear-gradient(90deg, rgba(155,89,182,0.3), rgba(224,64,251,0.1));
        border: 1px solid #9b59b6;
        border-radius: 20px;
        padding: 20px 30px;
        margin-bottom: 30px;
    }
</style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## Navegacion")
seccion = st.sidebar.radio("", [
    "🏠 Inicio",
    "📂 Cargar datos",
    "📈 Visualizacion",
    "🔬 Prueba Z",
    "🤖 Asistente IA"
], key="menu")

if seccion == "🏠 Inicio":
    st.markdown("""
    <div class="header-container">
        <h1 style="margin:0; font-size:2.5em;">📊 App de Prueba de Hipotesis</h1>
        <p style="margin:5px 0 0 0; color:#b39ddb;">Probabilidad y Estadistica — Desarrollado con Streamlit + Gemini AI</p>
    </div>
    """, unsafe_allow_html=True)
    st.header("👋 Bienvenido")
    st.markdown("""
    Esta aplicacion permite realizar analisis estadisticos de manera interactiva:
    - 📂 **Cargar datos** desde un archivo CSV o generarlos de forma sintetica
    - 📈 **Visualizar** la distribucion con histograma y boxplot
    - 🔬 **Realizar pruebas Z** con visualizacion de la region critica
    - 🤖 **Consultar IA** basada en Gemini para interpretar resultados

    Ingrese al menu de la izquierda para comenzar.
    """)

elif seccion == "📂 Cargar datos":
    st.header("📂 Cargar datos")
    opcion = st.radio("Como quieres ingresar los datos?", ["Subir CSV", "Generar datos sinteticos"])
    if opcion == "Subir CSV":
        archivo = st.file_uploader("Sube tu archivo CSV", type=["csv"])
        if archivo:
            df = pd.read_csv(archivo)
            st.session_state["datos"] = df
            st.success(" Archivo cargado correctamente")
            st.dataframe(df.head())
    elif opcion == "Generar datos sinteticos":
        media = st.number_input("Media de la distribucion", value=0.0)
        desviacion = st.number_input("Desviacion estandar", value=1.0, min_value=0.1)
        n = st.slider("Numero de observaciones", 30, 500, 100)
        if st.button(" Generar datos"):
            datos = np.random.normal(loc=media, scale=desviacion, size=n)
            df = pd.DataFrame({"valor": datos})
            st.session_state["datos"] = df
            st.success(f" Se generaron {n} datos con media={media} y desviacion={desviacion}")
            st.dataframe(df.head())

elif seccion == "📈 Visualizacion":
    st.header("📈 Visualizacion de datos")
    if "datos" not in st.session_state:
        st.warning("⚠️ Primero debes cargar o generar datos en la seccion Cargar datos")
    else:
        df = st.session_state["datos"]
        columna = df.columns[0]
        datos = df[columna]
        st.subheader(" Estadisticas basicas")
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("📍 Media", f"{datos.mean():.4f}")
        col2.metric("📏 Desv. estandar", f"{datos.std():.4f}")
        col3.metric("⬇️ Minimo", f"{datos.min():.4f}")
        col4.metric("⬆️ Maximo", f"{datos.max():.4f}")
        st.subheader("📉 Histograma")
        fig1, ax1 = plt.subplots(figsize=(4, 2))
        fig1.patch.set_facecolor('#1a1a2e')
        ax1.set_facecolor('#16213e')
        ax1.hist(datos, bins=20, edgecolor="#9b59b6", color="#7c3aed", density=True, alpha=0.8)
        xmin, xmax = ax1.get_xlim()
        x = np.linspace(xmin, xmax, 100)
        p = stats.norm.pdf(x, datos.mean(), datos.std())
        ax1.plot(x, p, "#e040fb", linewidth=2, label="Curva normal")
        ax1.set_xlabel("Valor", color="white")
        ax1.set_ylabel("Densidad", color="white")
        ax1.set_title("Histograma con curva normal", color="#e040fb")
        ax1.tick_params(colors="white")
        ax1.legend(facecolor='#1a1a2e', labelcolor='white')
        st.pyplot(fig1, use_container_width=False)
        st.subheader("📦 Boxplot")
        fig2, ax2 = plt.subplots(figsize=(4, 2))
        fig2.patch.set_facecolor('#1a1a2e')
        ax2.set_facecolor('#16213e')
        ax2.boxplot(datos, vert=False, patch_artist=True,
            boxprops=dict(facecolor='#7c3aed', color='#e040fb'),
            medianprops=dict(color='#e040fb', linewidth=2),
            whiskerprops=dict(color='white'),
            capprops=dict(color='white'),
            flierprops=dict(marker='o', color='#e040fb'))
        ax2.set_xlabel("Valor", color="white")
        ax2.set_title("Boxplot de los datos", color="#e040fb")
        ax2.tick_params(colors="white")
        st.pyplot(fig2, use_container_width=False)
        st.subheader("🔍 Analisis de la distribucion")
        skewness = datos.skew()
        if abs(skewness) < 0.5:
            st.info("La distribucion parece aproximadamente normal (sesgo bajo).")
        elif skewness > 0:
            st.warning("📈 La distribucion tiene sesgo positivo (cola hacia la derecha).")
        else:
            st.warning("📉 La distribucion tiene sesgo negativo (cola hacia la izquierda).")
        q1 = datos.quantile(0.25)
        q3 = datos.quantile(0.75)
        iqr = q3 - q1
        outliers = datos[(datos < q1 - 1.5 * iqr) | (datos > q3 + 1.5 * iqr)]
        st.write(f"🔎 Outliers detectados: **{len(outliers)}**")

elif seccion == "🔬 Prueba Z":
    st.header("🔬 Prueba de hipotesis Z")
    if "datos" not in st.session_state:
        st.warning("Primero debes cargar o generar datos en la seccion Cargar datos")
    else:
        df = st.session_state["datos"]
        datos = df[df.columns[0]]
        st.subheader("⚙️ Parametros de la prueba")
        mu0 = st.number_input("Hipotesis nula (media poblacional H0)", value=0.0)
        sigma = st.number_input("Desviacion estandar poblacional (sigma)", value=1.0, min_value=0.01)
        alpha = st.selectbox("Nivel de significancia (alpha)", [0.01, 0.05, 0.10])
        tipo = st.radio("Tipo de prueba", ["Bilateral", "Cola izquierda", "Cola derecha"])
        if st.button("🚀 Calcular prueba Z"):
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
            st.subheader("📋 Resultados")
            col1, col2, col3 = st.columns(3)
            col1.metric("📍 Media muestral", f"{media_muestral:.4f}")
            col2.metric("📐 Estadistico Z", f"{z:.4f}")
            col3.metric("🎯 p-value", f"{p_value:.4f}")
            if rechazar:
                st.error(f"❌ Se rechaza H0. Hay evidencia suficiente para rechazar la hipotesis nula (alpha={alpha})")
            else:
                st.success(f"✅ No se rechaza H0. No hay evidencia suficiente para rechazar la hipotesis nula (alpha={alpha})")
            st.subheader(" Grafica de la prueba")
            fig, ax = plt.subplots(figsize=(6, 3))
            fig.patch.set_facecolor('#1a1a2e')
            ax.set_facecolor('#16213e')
            x = np.linspace(-4, 4, 200)
            y = stats.norm.pdf(x)
            ax.plot(x, y, "#e040fb", linewidth=2)
            if tipo == "Bilateral":
                ax.fill_between(x, y, where=(x < -z_critico), color="#ff4757", alpha=0.4, label="Region de rechazo")
                ax.fill_between(x, y, where=(x > z_critico), color="#ff4757", alpha=0.4)
            elif tipo == "Cola izquierda":
                ax.fill_between(x, y, where=(x < z_critico), color="#ff4757", alpha=0.4, label="Region de rechazo")
            else:
                ax.fill_between(x, y, where=(x > z_critico), color="#ff4757", alpha=0.4, label="Region de rechazo")
            ax.axvline(z, color="#2ed573", linestyle="--", linewidth=2, label=f"Z calculado = {z:.4f}")
            ax.set_title("Distribucion normal con region critica", color="#e040fb")
            ax.tick_params(colors="white")
            ax.legend(facecolor='#1a1a2e', labelcolor='white')
            st.pyplot(fig, use_container_width=False)
            st.session_state["resultados_z"] = {
                "n": n, "media_muestral": media_muestral, "mu0": mu0,
                "sigma": sigma, "alpha": alpha, "tipo": tipo,
                "z": z, "p_value": p_value, "rechazar": rechazar
            }

elif seccion == "🤖 Asistente IA":
    st.header("🤖 Asistente de IA")
    if "resultados_z" not in st.session_state:
        st.warning("⚠️ Primero debes realizar una prueba Z en la seccion Prueba Z")
    else:
        r = st.session_state["resultados_z"]
        api_key = st.text_input("🔑 Ingresa tu API key de Gemini", type="password")
        if st.button("🤖 Consultar a la IA"):
            if not api_key:
                st.error("Debes ingresar tu API key")
            else:
                try:
                    genai.configure(api_key=api_key)
                    model = genai.GenerativeModel("gemini-2.5-flash")
                    prompt = (
                        "Se realizo una prueba Z con los siguientes parametros:\n"
                        f"- Media muestral: {r['media_muestral']:.4f}\n"
                        f"- Media hipotetica (H0): {r['mu0']}\n"
                        f"- Tamano de muestra: {r['n']}\n"
                        f"- Desviacion estandar poblacional: {r['sigma']}\n"
                        f"- Nivel de significancia: {r['alpha']}\n"
                        f"- Tipo de prueba: {r['tipo']}\n"
                        f"- Estadistico Z: {r['z']:.4f}\n"
                        f"- p-value: {r['p_value']:.4f}\n"
                        f"- Decision: {'Se rechaza H0' if r['rechazar'] else 'No se rechaza H0'}\n\n"
                        "Por favor explica en terminos simples:\n"
                        "1. Si la decision es correcta y por que\n"
                        "2. Si los supuestos de la prueba Z son razonables\n"
                        "3. Que significa este resultado en la practica"
                    )
                    with st.spinner("✨ Consultando a Gemini..."):
                        respuesta = model.generate_content(prompt)
                        st.subheader("💬 Respuesta de la IA")
                        st.write(respuesta.text)
                except Exception as e:
                    st.error(f" Error: {e}")