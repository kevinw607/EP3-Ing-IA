import time

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import ToolMessage

from tools.knowledge_tool import consultar_base_conocimiento
from tools.approval_tool import evaluar_solicitud_compra
from tools.report_tool import registrar_reporte_local
from tools.history_tool import consultar_historial_casos

from memory.short_term import ShortTermMemory
from agent.planner import PurchasePlanner

from observability.resource_monitor import ResourceMonitor
from observability.logger import (
    log_info,
    log_error
)

from observability.metrics import MetricsManager
from observability.tracer import Trace


class OrganizationalAgent:

    def __init__(self):

        self.memory = ShortTermMemory()

        self.metrics = MetricsManager()

        self.resource_monitor = ResourceMonitor()

        self.tools_map = {
            "consultar_base_conocimiento": consultar_base_conocimiento,
            "evaluar_solicitud_compra": evaluar_solicitud_compra,
            "registrar_reporte_local": registrar_reporte_local,
            "consultar_historial_casos": consultar_historial_casos
        }

        self.llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash",
            temperature=0.2
        )

        self.llm_tools = self.llm.bind_tools(
            list(self.tools_map.values())
        )

        self.prompt = ChatPromptTemplate.from_messages([

            (
                "system",
                """
Eres un agente autónomo organizacional experto en auditoría de adquisiciones.

REGLAS CRÍTICAS DE NEGOCIO

1. Si el monto evaluado es MENOR o IGUAL a 500 USD:
Se aprueba automáticamente.

2. Si el monto es MAYOR a 500 USD:
Debe solicitar aprobación al área de Finanzas
y generar un reporte obligatorio.

SIEMPRE debes corroborar la información utilizando
las herramientas correspondientes.

Nunca inventes información.
"""
            ),

            MessagesPlaceholder(
                variable_name="chat_history"
            ),

            (
                "human",
                "Plan Estratégico Sugerido: {plan_sugerido}\n\nSolicitud del Usuario: {input}"
            )
        ])

    def ejecutar(self, input_usuario: str) -> str:

        inicio = time.time()

        self.metrics.increment("total_requests")

        log_info("=" * 70)
        log_info("NUEVA SOLICITUD")
        log_info(f"Usuario: {input_usuario}")

        try:

            with Trace("Planner"):

                plan = PurchasePlanner.construir_plan(
                    input_usuario
                )

            log_info(f"Plan generado: {plan}")

            historial = self.memory.get_messages()

            mensajes = self.prompt.format_messages(

                input=input_usuario,

                plan_sugerido=", ".join(plan)
                if plan
                else "Ninguno",

                chat_history=historial

            )

            self.memory.add_user_message(
                input_usuario
            )

            while True:

                with Trace("LLM"):

                    respuesta = self.llm_tools.invoke(
                        mensajes
                    )

                self.memory.add_message(
                    respuesta
                )

                mensajes.append(
                    respuesta
                )

                if not respuesta.tool_calls:

                    tiempo = time.time() - inicio

                    self.metrics.update_latency(
                        tiempo
                    )

                    self.metrics.increment(
                        "successful_requests"
                    )

                    resources = (
                        self.resource_monitor.snapshot()
                    )

                    self.metrics.save_execution(
                        question=input_usuario,
                        latency=tiempo,
                        cpu=resources["cpu_percent"],
                        memory=resources["memory_percent"],
                        status="SUCCESS"
                    )

                    log_info(
                        f"Tiempo total: {tiempo:.3f} segundos"
                    )

                    contenido_final = respuesta.content

                    if (
                        isinstance(
                            contenido_final,
                            list
                        )
                        and len(contenido_final) > 0
                    ):

                        if (
                            "text"
                            in contenido_final[0]
                        ):

                            contenido_final = (
                                contenido_final[0]["text"]
                            )

                    log_info(
                        f"Respuesta final: {contenido_final}"
                    )

                    return str(
                        contenido_final
                    )

                for tool_call in respuesta.tool_calls:

                    tool_name = tool_call["name"]

                    tool_args = tool_call["args"]

                    tool_id = tool_call["id"]

                    log_info(
                        f"Herramienta ejecutada: {tool_name}"
                    )

                    self.metrics.add_tool_usage(
                        tool_name
                    )

                    try:

                        with Trace(tool_name):

                            resultado = (
                                self.tools_map[
                                    tool_name
                                ].invoke(
                                    tool_args
                                )
                            )

                    except Exception:

                        self.metrics.add_tool_error(
                            tool_name
                        )

                        raise

                    log_info(
                        f"Resultado herramienta: {resultado}"
                    )

                    tool_message = ToolMessage(

                        content=str(resultado),

                        tool_call_id=tool_id

                    )

                    self.memory.add_message(
                        tool_message
                    )

                    mensajes.append(
                        tool_message
                    )

        except Exception as e:

            self.metrics.increment(
                "errors"
            )

            resources = (
                self.resource_monitor.snapshot()
            )

            self.metrics.save_execution(
                question=input_usuario,
                latency=time.time() - inicio,
                cpu=resources["cpu_percent"],
                memory=resources["memory_percent"],
                status="ERROR"
            )

            log_error(str(e))

            raise