import os
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document

class SemanticMemory:

    def __init__(self):
        self.embeddings = GoogleGenerativeAIEmbeddings(
            model="text-embedding-004"
        )
        self.vectorstore = None

    def cargar_documentos(self, carpeta="data/knowledge_base"):
        documentos = []
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        if not os.path.exists(carpeta) or not os.listdir(carpeta):
            documentos.append(Document(page_content="Base de conocimiento inicializada.", metadata={"source": "init"}))
        else:
            for archivo in os.listdir(carpeta):
                ruta = os.path.join(carpeta, archivo)
                if archivo.endswith(".txt"):
                    with open(ruta, "r", encoding="utf-8") as f:
                        contenido = f.read()
                    if contenido.strip():
                        documentos.append(
                            Document(
                                page_content=contenido,
                                metadata={"source": archivo}
                            )
                        )

        if documentos:
            try:
                self.vectorstore = FAISS.from_documents(
                    documentos,
                    self.embeddings
                )
            except Exception as e:
                print(f"\n[ERROR FAISS]: No se pudo conectar con los embeddings de Google. Detalles: {e}")
                print("El agente intentará continuar sin memoria semántica...\n")
                self.vectorstore = None

    def buscar(self, query: str, k: int = 3) -> str:
        if self.vectorstore is None:
            return "No hay documentos indexados o la base de conocimiento está vacía debido a un error de conexión."
        
        try:
            resultados = self.vectorstore.similarity_search(query, k=k)
            if not resultados:
                return "No se encontraron resultados relevantes."
                
            contexto = []
            for doc in resultados:
                contexto.append(f"[Fuente: {doc.metadata.get('source')}]: {doc.page_content}")
            return "\n\n".join(contexto)
        except Exception:
            return "Error al buscar en la base de conocimiento."