from ollama_gui import OllamaInterface
import tkinter as tk


if __name__ == "__main__":
    root = tk.Tk()

    root.title("Ollama LLM GUI")
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    root.geometry(f"800x600+{(screen_width - 800) // 2}+{(screen_height - 600) // 2}")

    root.grid_columnconfigure(0, weight=1)
    root.grid_rowconfigure(1, weight=1)
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=0)

    app = OllamaInterface(root)

    app.chat_box.tag_configure(
        "Bold", foreground="#ff007b", font=(app.default_font, 10, "bold")
    )
    app.chat_box.tag_configure("Error", foreground="red")
    app.chat_box.tag_configure("Right", justify="right")

    root.mainloop()
