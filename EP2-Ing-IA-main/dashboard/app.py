import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st

from analysis.analyzer import Analyzer
from analysis.recommendations import Recommendations
from analysis.health import HealthStatus

st.set_page_config(
    page_title="Dashboard Observabilidad",
    layout="wide"
)

st.title("📊 Dashboard de Observabilidad del Agente IA")

metrics_path = Path("logs/metrics.json")
history_path = Path("logs/execution_history.csv")

analyzer = Analyzer()
recommendations = Recommendations()

summary = analyzer.summary()
health = HealthStatus(summary).evaluate()
# =============================
# Sidebar
# =============================

st.sidebar.title("⚙️ Estado del Sistema")

st.sidebar.metric(
    "Estado",
    health["status"]
)

st.sidebar.metric(
    "Health Score",
    f"{health['score']} / 100"
)

st.sidebar.progress(
    health["score"] / 100
)

st.sidebar.divider()

st.sidebar.metric(
    "Solicitudes",
    summary["total_requests"]
)

st.sidebar.metric(
    "Errores",
    summary["errors"]
)

st.sidebar.metric(
    "Latencia",
    f"{summary['average_latency']:.2f} s"
)

st.sidebar.divider()

st.sidebar.write(
    "Dashboard desarrollado para Ingeniería de Soluciones con IA."
)


# -----------------------------
# Cargar métricas
# -----------------------------

if metrics_path.exists():

    with open(metrics_path, encoding="utf-8") as f:

        metrics = json.load(f)

else:

    st.error("No existe metrics.json")
    st.stop()

# -----------------------------
# KPIs
# -----------------------------

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "Solicitudes",
    summary["total_requests"]
)

col2.metric(
    "Éxito",
    f"{summary['success_rate']} %"
)

col3.metric(
    "Errores",
    summary["errors"]
)

col4.metric(
    "Latencia Promedio",
    f"{summary['average_latency']:.3f} s"
)

st.divider()
# -----------------------------
# Estado del Agente
# -----------------------------

st.subheader("Estado General del Agente")

col1, col2 = st.columns(2)

col1.metric(
    "Estado",
    health["status"]
)

col2.metric(
    "Health Score",
    f"{health['score']} / 100"
)

if health["reasons"]:

    st.warning(
        "Problemas detectados:"
    )

    for reason in health["reasons"]:

        st.write("•", reason)

else:

    st.success(
        "El sistema funciona correctamente."
    )

st.divider()

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "CPU Promedio",
    f"{summary['average_cpu']} %"
)

col2.metric(
    "RAM Promedio",
    f"{summary['average_memory']} %"
)

col3.metric(
    "Consultas Lentas",
    summary["slow_requests"]
)

col4.metric(
    "Reportes",
    metrics["reports_generated"]
)

st.divider()


# -----------------------------
# Herramientas
# -----------------------------

col1, col2 = st.columns(2)

most_tool = summary["most_used_tool"] or "Sin registros"

error_tool = summary["tool_with_most_errors"] or "Sin errores registrados"

col1.info(
    f"**Herramienta más utilizada**\n\n"
    f"{most_tool}"
)

col2.info(
    f"**Herramienta con más errores**\n\n"
    f"{error_tool}"
)


st.divider()

# -----------------------------
# Historial
# -----------------------------

if history_path.exists():

    df = pd.read_csv(history_path)

    st.subheader("Historial de ejecuciones")

    st.dataframe(
        df.style.background_gradient(
            subset=["latency"],
            cmap="YlOrRd"
        ),
        use_container_width=True
    )

    if not df.empty:

        x = range(1, len(df) + 1)

        # -------------------------
        # Latencia
        # -------------------------

        st.subheader("Latencia por consulta")

        fig, ax = plt.subplots(figsize=(9, 4))

        ax.plot(
            x,
            df["latency"],
            marker="o",
            linewidth=2
        )

        ax.set_xticks(list(x))
        ax.set_xlabel("Consulta")
        ax.set_ylabel("Segundos")
        ax.set_title("Latencia")
        ax.grid(True)

        st.pyplot(fig)

        # -------------------------
        # CPU
        # -------------------------

        st.subheader("Uso de CPU")

        fig, ax = plt.subplots(figsize=(9, 4))

        ax.plot(
            x,
            df["cpu"],
            marker="o",
            linewidth=2
        )

        ax.set_xticks(list(x))
        ax.set_xlabel("Consulta")
        ax.set_ylabel("% CPU")
        ax.set_title("Consumo de CPU")
        ax.grid(True)

        st.pyplot(fig)

        # -------------------------
        # Memoria
        # -------------------------

        st.subheader("Uso de Memoria")

        fig, ax = plt.subplots(figsize=(9, 4))

        ax.plot(
            x,
            df["memory"],
            marker="o",
            linewidth=2
        )

        ax.set_xticks(list(x))
        ax.set_xlabel("Consulta")
        ax.set_ylabel("% RAM")
        ax.set_title("Consumo de Memoria")
        ax.grid(True)

        st.pyplot(fig)

    else:

        st.info(
            "Aún no existen ejecuciones registradas."
        )

else:

    st.warning(
        "Aún no existen ejecuciones registradas."
    )

st.divider()

# -----------------------------
# Uso de herramientas
# -----------------------------

st.subheader("Uso de herramientas")

tool_calls = metrics["tool_calls"]

if tool_calls:

    fig, ax = plt.subplots(figsize=(9, 4))

    ax.barh(
        list(tool_calls.keys()),
        list(tool_calls.values())
    )

    ax.set_title(
        "Cantidad de ejecuciones por herramienta"
    )

    ax.set_xlabel(
         "Cantidad de ejecuciones"
    )

    ax.set_ylabel(
        "Herramienta"
    )

    ax.grid(axis="x")

    st.pyplot(fig)

else:

    st.info(
        "No hay uso de herramientas registrado."
    )

st.divider()
st.subheader("Resumen Ejecutivo")

st.info(
    f"""
El agente ha procesado **{summary['total_requests']} solicitudes**
con una tasa de éxito del **{summary['success_rate']} %**.

La latencia promedio es de
**{summary['average_latency']:.2f} segundos**.

La herramienta más utilizada fue
**{summary['most_used_tool']}**.

El estado general del sistema es
**{health['status']}** con un puntaje de
**{health['score']} / 100**.
"""
)

st.divider()
# -----------------------------
# Cuellos de botella
# -----------------------------

st.subheader("Cuellos de botella")

for item in summary["bottlenecks"]:

    st.write("•", item)

st.divider()

# -----------------------------
# Recomendaciones
# -----------------------------

st.subheader("Recomendaciones")

for recommendation in recommendations.generate():

    if recommendation["priority"] == "Alta":

        st.error(recommendation["message"])

    elif recommendation["priority"] == "Media":

        st.warning(recommendation["message"])

    else:

        st.success(recommendation["message"])

st.divider()

st.caption(
    "Dashboard de Observabilidad - Ingeniería de Soluciones con IA"
)