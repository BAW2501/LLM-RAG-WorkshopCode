from ConsoleBasedRag import RAGSystem, SemanticSearch, SearchConfig, Config
from ollama_gui import OllamaInterface, LayoutManager
from threading import Thread
from tkinter import filedialog, font
from tkinter import ttk
import os
import tkinter as tk

# Application constants
DEFAULT_API_URL = "http://127.0.0.1:11434"
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
SUPPORTED_FILE_TYPES = (("PDF files", "*.pdf"), ("All files", "*.*"))


# Extends base layout with PDF processing capabilities
class RagLayoutManager(LayoutManager):
    def __init__(self, interface: OllamaInterface):
        super().__init__(interface)
        self.vault_embeddings = None
        self.document_chunks = None
        self.rag_system = RAGSystem()

    def _header_frame(self):
        super()._header_frame()
        self.setup_pdf_button()

    def setup_pdf_button(self):
        pdf_button = ttk.Button(
            self.interface.root, text="Open PDF", command=self.on_pdf_button_click
        )
        pdf_button.grid(row=0, column=0, padx=(5, 0))

    def on_pdf_button_click(self):
        file_path = filedialog.askopenfilename(
            title="Select a PDF file", filetypes=SUPPORTED_FILE_TYPES
        )

        if file_path:
            self.on_pdf_load(file_path)

    def on_pdf_load(self, file_path: str):
        self.rag_system.process_document(file_path)
        self.load_vault_contents()
        if self.document_chunks:
            self.vault_embeddings = (
                self.rag_system.embedding_service.get_bulk_embeddings(
                    self.document_chunks
                )
            )

    def load_vault_contents(self):
        if os.path.exists(Config.VAULT_FILE):
            with open(Config.VAULT_FILE, "r", encoding="utf-8") as f:
                self.document_chunks = f.readlines()
        else:
            print("Error: No content available.")
            return


class RagUi(OllamaInterface):
    def __init__(self, root: tk.Tk):
        self.root = root
        self.api_url = DEFAULT_API_URL
        self.chat_history: list[dict[str, str]] = []
        self.label_widgets = []
        self.default_font = font.nametofont("TkTextFont").actual()["family"]
        self.layout = RagLayoutManager(self)
        self.semantic_search = SemanticSearch()

        self.layout.init_layout()
        self.root.after(200, self.check_system)
        self.refresh_models()

    def on_send_button(self, _=None):
        message = self.user_input.get("1.0", "end-1c")
        if message:
            processed_message = self.process_message_with_context(message)
            self.layout.create_inner_label(on_right_side=True)
            self.append_filtered_text_to_chat(processed_message, use_label=True)
            self.append_filtered_text_to_chat("\n\n")
            self.user_input.delete("1.0", "end")
            self.chat_history.append({"role": "user", "content": processed_message})

            Thread(
                target=self.generate_ai_response,
                daemon=True,
            ).start()

    def process_message_with_context(self, message: str):
        if self.layout.vault_embeddings is None or self.layout.document_chunks is None:
            return message
        context = self.semantic_search.find_top_matching_chunks(
            message,
            self.layout.vault_embeddings,
            self.layout.document_chunks,
            SearchConfig(),
        )
        if context:
            context_str = "\n".join(context)
            return f"{message}[CONTEXT_PROVIDED_AFTER]{context_str}"
        return message

    # Filters out context information before displaying messages
    def append_filtered_text_to_chat(
        self, text: str, *args: str | list[str], use_label: bool = False
    ):
        text = text.split("[CONTEXT_PROVIDED_AFTER]")[0]
        super().append_text_to_chat(text, *args, use_label=use_label)


if __name__ == "__main__":
    # Main application window initialization and configuration
    root = tk.Tk()
    root.title("Ollama GUI")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(
        f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{(screen_width - WINDOW_WIDTH) // 2}+{(screen_height - WINDOW_HEIGHT) // 2}"
    )

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=0)

    rag_interface = RagUi(root)

    # Chat interface customization
    rag_interface.chat_box.tag_configure(
        "Bold", foreground="#ff007b", font=(rag_interface.default_font, 10, "bold")
    )
    rag_interface.chat_box.tag_configure("Error", foreground="red")
    rag_interface.chat_box.tag_configure("Right", justify="right")

    root.mainloop()
