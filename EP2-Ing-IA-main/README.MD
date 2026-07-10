======================================================================
SISTEMA AUTÓNOMO DE EVALUACIÓN Y APROBACIÓN DE COMPRAS (SAEAC)
         CON DASHBOARD DE OBSERVABILIDAD EN TIEMPO REAL
======================================================================

SAEAC es un agente organizacional autónomo desarrollado con Inteligencia Artificial Generativa que automatiza la evaluación de solicitudes de compra dentro de una empresa. El sistema analiza requerimientos en lenguaje natural, consulta una base de conocimiento corporativa mediante búsqueda semántica (RAG), aplica reglas de negocio para determinar si una compra requiere aprobación financiera, mantiene memoria contextual de las interacciones y genera reportes automáticamente.

Esta versión integra un Dashboard de Observabilidad en Tiempo Real que monitorea de manera gráfica el uso de recursos, la latencia de las respuestas y la telemetría operacional del agente.

----------------------------------------------------------------------
1. CARACTERÍSTICAS CLAVE
----------------------------------------------------------------------

* Ciclo ReAct Autónomo: Orquestación basada en la vinculación nativa de herramientas (bind_tools) al modelo Gemini, permitiendo un ciclo dinámico de Pensamiento -> Acción -> Observación.
* Memoria Semántica Local (RAG): Indexación de reglamentos corporativos utilizando FAISS. Cuenta con tolerancia defensiva a fallos para seguir operando de forma autónoma si existen intermitencias con las cuotas de embeddings.
* Memoria de Corto Plazo Contextual: Encapsula el historial de mensajes de LangChain para resolver referencias abstractas consecutivas (ej. el Escenario 2).
* Dashboard de Observabilidad: Interfaz en Streamlit que calcula telemetría crítica en tiempo real (solicitudes exitosas, tasa de errores, latencias mínimas/máximas/promedio y contadores de reportes).
* Gráficos de Telemetría: Visualización dinámica mediante Matplotlib del consumo de CPU (%) y latencia (segundos) por cada consulta procesada.

----------------------------------------------------------------------
# 📁 Estructura del proyecto
----------------------------------------------------------------------

El repositorio cuenta con una estructura de raíz interna optimizada para despliegues locales:

EP3-Ing-IA-main/
└── EP3-Ing-IA-main/           # Carpeta raíz del proyecto y scripts
    ├── agent/                 # Lógica del agente, planificador estático y orquestador ReAct
    ├── dashboard/             # Interfaz web de observabilidad (app.py)
    ├── data/                  # Base de conocimiento (.txt corporativos) y reportes de auditoría
    ├── logs/                  # Telemetría persistente (agent.log, metrics.json, execution_history.csv)
    ├── memory/                # Gestión de memoria semántica (FAISS) y de corto plazo (LangChain)
    ├── tools/                 # Herramientas del agente (evaluación, reportes, historial corporativo)
    ├── .env                   # Archivo privado de credenciales (API Key)
    ├── main.py                # Script principal que gatilla los escenarios automáticos del agente
    └── requirements.txt       # Lista unificada de dependencias del ecosistema

----------------------------------------------------------------------
3. GUÍA PASO A PASO: INSTALACIÓN Y CONFIGURACIÓN
----------------------------------------------------------------------

Sigue los comandos en orden desde tu terminal para desplegar el entorno virtual aislado y ejecutar los componentes.

PASO 3.1: Clonar el proyecto e ingresar a la subcarpeta raíz
Descarga el repositorio y posiciónate estrictamente en el directorio interno del proyecto:
> git clone https://github.com/kevinw607/EP3-Ing-IA.git
> cd EP3-Ing-IA/EP3-Ing-IA-main

PASO 3.2: Activar el Entorno Virtual (.venv)
El proyecto incluye un entorno preconfigurado para aislar las librerías y evitar conflictos con el Python global del sistema.

* En Windows (PowerShell):
> ..\.venv\Scripts\Activate.ps1
(Nota: Si PowerShell arroja un error de restricciones de ejecución, levanta los permisos temporalmente con: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process y vuelve a ejecutar el comando de activación).

* En macOS o Linux:
> source ../.venv/bin/activate

Sabrás que se activó correctamente porque verás el prefijo (.venv) al inicio de tu línea de comandos.

PASO 3.3: Instalar las dependencias del proyecto
Con el entorno virtual activo, instala el ecosistema de librerías:
> pip install -r requirements.txt

PASO 3.4: Configurar la API Key de Google
Crea un archivo de configuración de entorno llamado exactamente .env en la raíz interna de trabajo (EP3-Ing-IA-main/EP3-Ing-IA-main) e inyecta tu credencial de Google AI Studio sin comillas ni espacios adicionales:

GOOGLE_API_KEY=tu_api_key_real_aqui

----------------------------------------------------------------------
4. EJECUCIÓN DEL SISTEMA
----------------------------------------------------------------------

El sistema requiere la ejecución de dos servicios en paralelo. Se recomienda abrir dos pestañas de terminal en VS Code con el entorno virtual activo en ambas:

Servicio 1: Iniciar el Dashboard de Observabilidad (Terminal 1)
Lanza el servidor de Streamlit encargado de renderizar la interfaz gráfica de telemetría:
> streamlit run dashboard/app.py

El sistema desplegará el panel e indicará la URL local de acceso (por defecto: http://localhost:8501).

Servicio 2: Ejecutar el Agente de IA (Terminal 2)
En la otra pestaña de la terminal, ejecuta el flujo principal para despertar al agente autónomo:
> python main.py

----------------------------------------------------------------------
5. COMPORTAMIENTO EN ESCENARIOS DE PRUEBA
----------------------------------------------------------------------

Al ejecutar main.py, el agente simula de manera secuencial el ingreso de solicitudes en lenguaje natural, gatillando los logs que alimentan al Dashboard:

* Escenario 1: Gasto de 600 USD
  - Entrada: "Revisa el procedimiento de compras, analiza un gasto de 600 USD y genera un reporte."
  - Acción: El agente lee las políticas corporativas, determina que al superar el umbral restrictivo de 500 USD requiere aprobación de Finanzas, invoca de manera autónoma a report_tool.py y genera el archivo físico de auditoría.

* Escenario 2: Gasto de 300 USD (Validación de Memoria Contextual)
  - Entrada: "Llegó otra solicitud por un gasto de 300 USD. ¿Se requiere reporte?"
  - Acción: El agente recupera el historial a corto plazo para asociar el contexto. Al validar matemáticamente que 300 USD es menor o igual al umbral, determina autónomamente que se aprueba de forma automática sin necesidad de un reporte formal.

Al finalizar las simulaciones, dirígete a tu navegador en http://localhost:8501 (o presiona Rerun) para visualizar el historial completo de las transacciones y las gráficas dinámicas de latencia y uso de CPU recién calculadas.

----------------------------------------------------------------------
6. JUSTIFICACIÓN TÉCNICA DE LA ARQUITECTURA
----------------------------------------------------------------------

1. Robustez Defensiva de Operaciones (memory/semantic_memory.py): Integra un control de excepciones avanzado alrededor de FAISS y GoogleGenerativeAIEmbeddings (usando mapeos nativos del modelo text-embedding-004). Ante fallas del servicio o cuotas de embeddings restringidas de la API Key, el agente captura el error, omite elegantemente el paso semántico y continúa operando de forma segura con sus reglas de negocio para no bloquear la disponibilidad del sistema ni romper el Dashboard.

2. Evitación de División por Cero en Telemetría (dashboard/app.py): El backend del dashboard implementa validaciones condicionales estrictas sobre los divisores de métricas en metrics.json. Si el histórico de consultas inicia en cero, el software mitiga errores matemáticos garantizando una visualización fluida sin caídas de interfaz.

3. Trazabilidad y Auditoría (logs/): Cada consulta, plan concebido por la clase PurchasePlanner, llamada a herramientas (ToolMessage) e inferencia del modelo queda cronometrada y grabada de forma permanente en execution_history.csv y agent.log, garantizando la rendición de cuentas solicitada por las directrices de auditoría informática.
======================================================================

Trazabilidad Defensiva de Operaciones (logs/): El sistema escribe de manera persistente cada plan concebido por la clase PurchasePlanner y cronometra el tiempo total de ejecución de la inferencia, cumpliendo de manera estricta con las directrices de rendición de cuentas de la pauta de auditoría.
