Proyecto Sistema Autonomo de Evaluacion y Aprobacion de compras (SAEAC)
======================================================================
SAEAC es un agente organizacional autónomo desarrollado con Inteligencia Artificial Generativa que automatiza la evaluación de solicitudes de compra dentro de una empresa. El sistema analiza requerimientos en lenguaje natural, consulta una base de conocimiento corporativa mediante búsqueda semántica, aplica reglas de negocio para determinar si una compra requiere aprobación financiera, mantiene memoria contextual de las interacciones y genera reportes automáticamente cuando corresponde. Su arquitectura integra LangChain, Gemini, herramientas autónomas (Tool Calling), memoria conversacional y memoria semántica con FAISS, permitiendo una toma de decisiones adaptativa y trazable frente a distintos escenarios operacionales.


GUÍA PASO A PASO: INSTALACIÓN Y CONFIGURACIÓN EN LA TERMINAL
======================================================================

Sigue esta lista de comandos en orden para dejar el entorno listo y ejecutar el agente de LangChain.

PASO 1: Clonar el proyecto e ingresar a la carpeta
--------------------------------------------------
Ejecuta el comando para descargar el repositorio y luego muévete dentro del directorio:
> git clone https://github.com/kevinw607/EP2-Ing-IA.git
> cd EP2-Ing-IA

PASO 2: Crear el entorno virtual (Recomendado)
----------------------------------------------
Esto evitará conflictos globales con otras librerías de Python.

* Si la otra persona está en WINDOWS:
> python -m venv venv

* Si la otra persona está en MACOS o LINUX:
> python3 -m venv venv

PASO 3: Activar el entorno virtual
----------------------------------
Es obligatorio activarlo antes de instalar las librerías.

* En WINDOWS (PowerShell o CMD):
> .\venv\Scripts\activate

* En MACOS o LINUX (Terminal):
> source venv/bin/activate

Nota: Sabrás que se activó porque aparecerá un "(venv)" al inicio de la línea de comandos.

PASO 4: Actualizar el gestor de paquetes (Opcional pero recomendado)
-------------------------------------------------------------------
Asegura que las descargas no fallen por herramientas desactualizadas:
> pip install --upgrade pip

PASO 5: Instalar las dependencias del proyecto
----------------------------------------------
Aquí se instalan las librerías del ecosistema LangChain y el lector de archivos de entorno:
> pip install langchain-google-genai python-dotenv

Nota alternativa: Si le dejas un archivo 'requirements.txt' en la raíz, la persona puede instalar todo con un solo comando:
> pip install -r requirements.txt

PASO 6: Configurar la API Key de Google
---------------------------------------
Antes de correr el script, se debe crear el archivo que almacena las credenciales.
En la misma terminal puedes crearlo rápidamente:

* En WINDOWS (PowerShell):
> echo "GOOGLE_API_KEY=tu_api_key_real_aqui" > .env

* En MACOS o LINUX:
> echo "GOOGLE_API_KEY=tu_api_key_real_aqui" > .env

(Si no usan comandos, pueden crear manualmente un archivo de texto llamado exactamente '.env' en la carpeta raíz y pegar la línea dentro).

PASO 7: Ejecutar el script principal
------------------------------------
Una vez completado todo lo anterior, el agente autónomo ya se puede iniciar desde la terminal:
> python nombre_de_tu_archivo.py
======================================================================

Comportamiento en Escenarios de Prueba
Al ejecutarse, el flujo simula el ingreso secuencial de dos solicitudes en lenguaje natural para verificar el razonamiento y la memoria del agente:

Escenario 1: Gasto de 600 USD
Entrada: "Revisa el procedimiento de compras, analiza un gasto de 600 USD y genera un reporte."

Acción del Agente: Inicializa la memoria semántica con FAISS, detecta el monto mediante el planificador estático, invoca la herramienta de evaluación y determina que al superar los 500 USD requiere aprobación obligatoria. Finalmente, invoca la herramienta local de reportes para persistir un archivo físico de auditoría.

Escenario 2: Gasto de 300 USD (Validación de Memoria Contextual)
Entrada: "Llegó otra solicitud por un gasto de 300 USD. ¿Se requiere reporte?"

Acción del Agente: Recupera el historial de mensajes a corto plazo para entender a qué reporte se refiere el usuario. Al evaluar matemáticamente que 300 USD es menor o igual al umbral restrictivo de 500 USD establecido en las políticas de compras.txt, determina autónomamente que no se requiere la generación de un reporte formal, respondiendo de manera precisa sin alucinaciones.


# 📁 Estructura del proyecto
```
Proyecto para ING IA/
├── agent/
│   ├── orchestrator.py        <-- Clase OrganizationalAgent (Con el ciclo ReAct y prompt corregidos)
│   └── planner.py             <-- Clase PurchasePlanner (Planificación estática)
├── data/
│   ├── knowledge_base/        <-- Base de conocimiento (.txt corporativos indexados por FAISS)
│   │   ├── casos_historicos.txt
│   │   ├── compras.txt
│   │   ├── finanzas.txt
│   │   ├── politicas_auditoria.txt
│   │   └── proveedores.txt
│   └── reports/               <-- Carpeta donde el agente guarda los reportes de auditoría (.txt)
├── logs/
│   └── agente.log             <-- Registro persistente de los planes y tiempos de ejecución
├── memory/
│   ├── semantic_memory.py     <-- Clase SemanticMemory (Con la búsqueda FAISS y lecturas corregidas)
│   └── short_term.py          <-- Clase ShortTermMemory (Con el historial de mensajes de LangChain)
├── tools/
│   ├── approval_tool.py       <-- Regla de aprobación automatizada (Límites de presupuesto)
│   ├── history_tool.py        <-- Herramienta para consultar casos históricos
│   ├── knowledge_tool.py      <-- Herramienta para consultar políticas organizacionales
│   └── report_tool.py         <-- Herramienta que escribe los reportes locales en disco
├── .env                       <-- Tu variable privada GOOGLE_API_KEY
├── main.py                    <-- Script principal que gatilla los escenarios automáticos
└── requirements.txt           <-- Librerías del proyecto para tu entorno virtual (venv)
```

Justificación Técnica de la Arquitectura
Ciclo ReAct Autónomo (orchestrator.py): Implementado mediante la vinculación nativa de herramientas (bind_tools) al modelo gemini-2.5-flash. Permite que el LLM genere un ciclo de Pensamiento -> Acción -> Observación dinámico, decidiendo qué herramientas invocar y procesando de forma segura múltiples respuestas intermedias mediante objetos ToolMessage.

Memoria Semántica de Baja Latencia (semantic_memory.py): Se utiliza FAISS acoplado con GoogleGenerativeAIEmbeddings (models/embedding-001) para vectorizar los reglamentos en disco. Esto otorga capacidades de recuperación RAG locales, asegurando que el modelo fundacional responda bajo políticas corporativas reales sin depender de bases de datos en la nube de alta complejidad.

Memoria a Corto Plazo Contextual (short_term.py): Basada en la abstracción orientada a objetos de LangChain, encapsula los mensajes de los turnos previos. Es el componente crítico que le permite al agente resolver referencias abstractas en el Escenario 2, asociando la palabra "reporte" con el flujo de transacciones evaluado inmediatamente antes.

Trazabilidad Defensiva de Operaciones (logs/): El sistema escribe de manera persistente cada plan concebido por la clase PurchasePlanner y cronometra el tiempo total de ejecución de la inferencia, cumpliendo de manera estricta con las directrices de rendición de cuentas de la pauta de auditoría.
