# Proyecto: Análisis y Modelo — Credit Card Default

Repositorio para el proyecto **Credit Card Default** (Kaggle). Objetivo: generar un análisis descriptivo poblacional y entrenar un modelo para predecir `default.payment.next.month`.

---

## Descripción del proyecto

Este proyecto toma el dataset **Credit Card Default** (Kaggle) y realiza:

1. Un análisis poblacional agregando indicadores generales y 3 indicadores adicionales de riesgo.
2. Entrenamiento y evaluación de un modelo de clasificación (Regresión Logística por defecto) para predecir `default.payment.next.month`.
3. Un dashboard en Streamlit para visualizar los datos y ejecutar las funciones desde la interfaz.

### Indicadores del reporte
- Número total de clientes.
- Número y porcentaje de clientes que incumplieron con su pago.
- Distribución de la edad (media, mediana, desviación estándar).
- Distribución del límite de crédito (media, mediana, desviación estándar).
- Número y porcentaje por nivel educativo (`EDUCATION`).
- Número y porcentaje por estado civil (`MARRIAGE`).

---

## Dashboard en Streamlit
[Dashboard en Streamlit](https://xwdjziwwc6pg2jexkpw9rf.streamlit.app/)

---

## Instrucciones para uso local

1. Clona el repositorio.
2. Ejectuta el notebook con el archivo .csv cargado
