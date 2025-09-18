import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import io

# Configuración de la página de Streamlit
st.set_page_config(layout="wide", page_title="Análisis de Riesgo Crediticio")

# Función de Análisis General adaptada para Streamlit
def analisis_general_dashboard(df):
    """
    Realiza un análisis general del dataset y retorna un reporte y figuras para el dashboard.
    """
    # 1. Limpieza y preparación de datos
    df = df.rename(columns={
        'LIMIT_BAL': 'limite_credito',
        'SEX': 'genero',
        'EDUCATION': 'nivel_educativo',
        'MARRIAGE': 'estado_civil',
        'AGE': 'edad',
        'default.payment.next.month': 'incumplimiento'
    })

    df['genero'] = df['genero'].map({1: 'Hombre', 2: 'Mujer'})
    df['nivel_educativo'] = df['nivel_educativo'].map({
        1: 'Graduado', 2: 'Universidad', 3: 'Secundaria',
        4: 'Otros', 5: 'Desconocido', 6: 'Desconocido', 0: 'Desconocido'
    })
    df['estado_civil'] = df['estado_civil'].map({
        1: 'Casado', 2: 'Soltero', 3: 'Otros', 0: 'Otros'
    })
    df['retraso_reciente'] = np.where(df['PAY_0'] > 0, 1, 0)
    df['gasto_promedio'] = df[[f'BILL_AMT{i}' for i in range(1, 7)]].mean(axis=1)

    # 2. Creación del reporte
    reporte = {}
    total_clientes = len(df)
    incumplimiento_count = df['incumplimiento'].sum()
    incumplimiento_porcentaje = (incumplimiento_count / total_clientes) * 100
    reporte['1. Número total de clientes'] = total_clientes
    reporte['2. Clientes que incumplieron (número)'] = incumplimiento_count
    reporte['3. Clientes que incumplieron (%)'] = f'{incumplimiento_porcentaje:.2f}%'
    reporte['4. Edad - Media'] = df['edad'].mean()
    reporte['5. Edad - Mediana'] = df['edad'].median()
    reporte['6. Edad - Desviación Estándar'] = df['edad'].std()
    reporte['7. Límite de Crédito - Media'] = df['limite_credito'].mean()
    reporte['8. Límite de Crédito - Mediana'] = df['limite_credito'].median()
    reporte['9. Límite de Crédito - Desviación Estándar'] = df['limite_credito'].std()
    reporte['10. Gasto promedio de facturas - Media'] = df['gasto_promedio'].mean()
    reporte['11. Gasto promedio de facturas - Desviación Estándar'] = df['gasto_promedio'].std()

    reporte_df = pd.DataFrame(list(reporte.items()), columns=['Indicador', 'Valor'])

    # 3. Creación de visualizaciones
    sns.set_style("whitegrid")

    # Gráfico 1: Distribución de Incumplimiento
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    sns.countplot(x='incumplimiento', data=df, ax=ax1)
    ax1.set_title('Distribución de Clientes por Incumplimiento de Pago', fontsize=16)
    ax1.set_xlabel('Incumplimiento (0: No, 1: Sí)', fontsize=12)
    ax1.set_ylabel('Número de Clientes', fontsize=12)
    plt.close(fig1)

    # Gráfico 2: Distribución de Edad
    fig2, ax2 = plt.subplots(figsize=(10, 6))
    sns.histplot(df['edad'], bins=30, kde=True, ax=ax2)
    ax2.set_title('Distribución de la Edad de los Clientes', fontsize=16)
    ax2.set_xlabel('Edad', fontsize=12)
    ax2.set_ylabel('Frecuencia', fontsize=12)
    plt.close(fig2)

    # Gráfico 3: Distribución del Límite de Crédito
    fig3, ax3 = plt.subplots(figsize=(10, 6))
    sns.boxplot(x=df['limite_credito'], ax=ax3)
    ax3.set_title('Distribución del Límite de Crédito', fontsize=16)
    ax3.set_xlabel('Límite de Crédito', fontsize=12)
    ax3.set_ylabel('')
    plt.close(fig3)

    # Gráfico 4: Distribución de variables categóricas
    fig4, axes = plt.subplots(1, 3, figsize=(18, 6))
    sns.countplot(x='genero', data=df, ax=axes[0])
    axes[0].set_title('Distribución por Género')
    sns.countplot(x='nivel_educativo', data=df, ax=axes[1])
    axes[1].set_title('Distribución por Nivel Educativo')
    axes[1].tick_params(axis='x', rotation=45)
    sns.countplot(x='estado_civil', data=df, ax=axes[2])
    axes[2].set_title('Distribución por Estado Civil')
    plt.tight_layout()
    plt.close(fig4)

    return reporte_df, fig1, fig2, fig3, fig4

# ----------------- Lógica Principal del Dashboard -----------------

st.title('Análisis de Riesgo de Impago de Tarjetas de Crédito 💳')
st.markdown("""
Bienvenido al dashboard interactivo para el análisis del riesgo de impago.
Aquí podrás cargar el conjunto de datos de "Credit Card Default" para obtener un análisis
completo que incluye indicadores clave, visualizaciones y los **insights** más relevantes.
""")

st.markdown("---")
uploaded_file = st.file_uploader("Sube tu archivo 'data_credito.csv'", type="csv")

if uploaded_file is not None:
    # 1. Carga y pre-procesamiento del archivo
    try:
        df = pd.read_csv(uploaded_file)
        st.success("¡Archivo cargado exitosamente! 🎉")

        st.markdown("### 📊 Reporte General de Clientes")
        reporte_df, fig1, fig2, fig3, fig4 = analisis_general_dashboard(df)
        st.dataframe(reporte_df)

        # 2. Visualizaciones e Insights
        st.markdown("---")
        st.markdown("### 📈 Visualizaciones y Hallazgos")

        # Gráfico 1: Incumplimiento
        st.pyplot(fig1)
        st.markdown("""
        **Insight:** Este gráfico revela un desbalance notable en la clase objetivo. Un pequeño porcentaje de clientes (**22.12%**) ha incumplido sus pagos, lo que es un escenario común en problemas de detección de fraude o riesgo. Para el modelado, esto significa que la **precisión** no es una métrica suficiente. Deberemos enfocarnos en **Recall**, **Precisión** y, sobre todo, en el **F1-Score** para evaluar el rendimiento del modelo de manera robusta.
        """)

        # Gráfico 2: Edad
        st.pyplot(fig2)
        st.markdown("""
        **Insight:** La distribución de la edad de los clientes se asemeja a una campana, con una concentración de clientes entre los **25 y 45 años**. Este segmento es típicamente el más activo económicamente, por lo que es crucial entender su comportamiento de pago.
        """)

        # Gráfico 3: Límite de Crédito
        st.pyplot(fig3)
        st.markdown("""
        **Insight:** El gráfico de caja muestra que la mayoría de los clientes tienen límites de crédito bajos o moderados. Sin embargo, se observan numerosos **valores atípicos (outliers)** que corresponden a clientes con límites de crédito extremadamente altos. Estos casos podrían requerir un análisis particular, ya que su comportamiento de pago podría ser diferente.
        """)

        # Gráfico 4: Variables Categóricas
        st.pyplot(fig4)
        st.markdown("""
        **Insight:**
        * **Género:** La base de clientes está mayoritariamente compuesta por mujeres.
        * **Nivel Educativo:** La mayoría de los clientes tienen un nivel educativo de **universidad** o **graduado**.
        * **Estado Civil:** La mayor parte de la población se encuentra en estado **soltero** o **casado**.
        Estos perfiles demográficos nos dan un panorama claro de la población a la que le estamos evaluando el riesgo.
        """)

        st.balloons()

    except Exception as e:
        st.error(f"Ocurrió un error al procesar el archivo. Asegúrate de que el formato sea correcto. Error: {e}")
