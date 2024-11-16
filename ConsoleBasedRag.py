import os
import re
import pymupdf
from ollama import chat, embeddings
import numpy as np
from dataclasses import dataclass

# Application constants
MXBAI_EMBED_MODEL = "mxbai-embed-large"
LLAMA_CHAT_MODEL = "llama3.2:3b"
SENTENCE_SPLIT_PATTERN = r"(?<=[.!?]) +"
WHITESPACE_CLEANUP_PATTERN = r"\s+"
PDF_DOCUMENT_NAME = "Logic-math.pdf"


@dataclass
class SearchConfig:
    top_k: int = 3
    similarity_threshold: float = 0.5


class Config:
    """Central configuration for easy modifications"""

    VAULT_FILE = "vault.txt"
    CHUNK_SIZE = 500
    COLORS = {"highlight": "\033[96m", "answer": "\033[92m", "reset": "\033[0m"}
    SYSTEM_PROMPT = "You are an expert at answering question using relevant text."


class PDFProcessor:
    def __init__(self, chunk_size: int):
        self.chunk_size = chunk_size

    def extract_text(self, file_path: str) -> str | None:
        if not os.path.exists(file_path):
            print(f"Error: File {file_path} not found!")
            return None

        try:
            pdf_document = pymupdf.open(file_path)
            text = " ".join(page.get_text() for page in pdf_document)  # type: ignore
            pdf_document.close()
            return re.sub(WHITESPACE_CLEANUP_PATTERN, " ", text).strip()
        except Exception as e:
            print(f"Error processing PDF: {str(e)}")
            return None

    def create_sentence_chunks(self, text: str) -> list[str]:
        """Manages sentence-based text chunking"""
        chunks: list[str] = []
        current_chunk = ""

        for sentence in re.split(SENTENCE_SPLIT_PATTERN, text):
            if len(current_chunk) + len(sentence) < self.chunk_size:
                current_chunk += sentence + " "
            else:
                chunks.append(current_chunk.strip())
                current_chunk = sentence + " "

        if current_chunk:
            chunks.append(current_chunk.strip())
        return chunks


class EmbeddingService:
    def __init__(self, model: str = MXBAI_EMBED_MODEL):
        self.model = model

    def get_embedding(self, text: str) -> np.ndarray:
        return np.array(embeddings(model=self.model, prompt=text)["embedding"])

    def get_bulk_embeddings(self, texts: list[str]) -> np.ndarray:
        return np.array(
            [embeddings(model=self.model, prompt=text)["embedding"] for text in texts]
        )


class SemanticSearch:
    @staticmethod
    def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
        return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

    def find_top_matching_chunks(
        self,
        query: str,
        vault_embeddings: np.ndarray,
        vault_content: list[str],
        config: SearchConfig,
    ) -> list[str]:
        embedding_service = EmbeddingService()
        query_embedding = embedding_service.get_embedding(query)

        similarities = [
            self.cosine_similarity(query_embedding, vec) for vec in vault_embeddings
        ]

        top_indices = np.argsort(similarities)[-config.top_k :][::-1]
        return [vault_content[i].strip() for i in top_indices]


class QueryProcessor:
    def __init__(self, search_service: SemanticSearch):
        self.search_service = search_service

    def create_chat_messages(
        self, query: str, context: str | None = None
    ) -> list[dict[str, str]]:
        content = f"{context}\n{query}" if context else query
        return [
            {"role": "system", "content": Config.SYSTEM_PROMPT},
            {"role": "user", "content": content},
        ]

    def format_response(self, context: list[str]) -> str:
        if not context:
            return ""
        context_str = "\n".join(context)
        return f"\nRelevant context:\n{Config.COLORS['highlight']}{context_str}{Config.COLORS['reset']}\n"

    def process_query(
        self, query: str, vault_embeddings: np.ndarray, vault_content: list[str]
    ) -> str:
        context = self.search_service.find_top_matching_chunks(
            query, vault_embeddings, vault_content, SearchConfig()
        )

        if context:
            print(self.format_response(context))
            context_str = "\n".join(context)
            messages = self.create_chat_messages(query, context_str)
        else:
            messages = self.create_chat_messages(query)

        try:
            response = chat(model=LLAMA_CHAT_MODEL, messages=messages)["message"]["content"]  # type: ignore
            return response
        except Exception as e:
            return f"Error generating response: {str(e)}"


class RAGSystem:
    def __init__(self):
        self.pdf_processor = PDFProcessor(Config.CHUNK_SIZE)
        self.embedding_service = EmbeddingService()
        self.search_service = SemanticSearch()
        self.query_processor = QueryProcessor(self.search_service)

    def process_document(self, file_path: str) -> bool:
        text = self.pdf_processor.extract_text(file_path)
        if not text:
            return False

        chunks = self.pdf_processor.create_sentence_chunks(text)
        with open(Config.VAULT_FILE, "w", encoding="utf-8") as f:
            f.write("\n".join(chunks))
        return True

    def run(self):
        if not self.process_document(PDF_DOCUMENT_NAME):
            print("Error: No content available.")
            return

        print("Loading content and generating embeddings...")
        with open(Config.VAULT_FILE, "r", encoding="utf-8") as f:
            vault_content = f.readlines()

        vault_embeddings = self.embedding_service.get_bulk_embeddings(vault_content)
        print("Ready to answer questions!")

        while True:
            query = input("\nAsk about the document (or 'quit' to exit): ")
            if query.lower() == "quit":
                break

            response = self.query_processor.process_query(
                query, vault_embeddings, vault_content
            )
            print(f"\n{Config.COLORS['answer']}{response}{Config.COLORS['reset']}")


if __name__ == "__main__":
    rag_system = RAGSystem()
    rag_system.run()
