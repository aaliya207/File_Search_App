import os
import threading
from tkinter import filedialog, messagebox
import tkinter as tk
from pathlib import Path

class FileSearchApp:
    def __init__(self, master):
        self.master = master
        self.master.title("🔍 Kawaii File Ninja")
        self.master.geometry("500x500")
        self.master.configure(bg="#ffe4f7")
        self.index = {}

        self.label = tk.Label(master, text="✨ Choose folder to index ✨", bg="#ffe4f7", fg="#8b008b", font=("Comic Sans MS", 16, "bold"))
        self.label.pack(pady=15)

        self.browse_button = tk.Button(master, text="📁 Browse", font=("Comic Sans MS", 14), bg="#ffb3ff", fg="#4b0082",
                                       relief="groove", bd=3, command=self.browse_folder)
        self.browse_button.pack(pady=10)

        self.search_label = tk.Label(master, text="🔎 Type keyword below", bg="#ffe4f7", fg="#8b008b", font=("Comic Sans MS", 14))
        self.search_label.pack(pady=5)

        self.search_var = tk.StringVar()
        self.search_entry = tk.Entry(master, textvariable=self.search_var, font=("Comic Sans MS", 12), width=40, bg="#fff0fa",
                                     fg="#4b0082", relief="ridge", bd=3)
        self.search_entry.pack(pady=10)

        self.search_button = tk.Button(master, text="💫 Search", font=("Comic Sans MS", 12), bg="#ffb3ff", fg="#4b0082",
                                       relief="groove", bd=3, command=self.search_files)
        self.search_button.pack(pady=5)

        self.wait_label = tk.Label(master, text="", bg="#ffe4f7", fg="#ff69b4", font=("Comic Sans MS", 12))
        self.wait_label.pack()

        self.results_listbox = tk.Listbox(master, font=("Comic Sans MS", 10), width=60, height=15, bg="#fff0fa", fg="#4b0082",
                                          relief="sunken", bd=2, selectbackground="#ffc1e3", selectforeground="#000")
        self.results_listbox.pack(pady=10)

    def browse_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.index.clear()
            threading.Thread(target=self.index_files, args=(folder_path,), daemon=True).start()

    def index_files(self, folder_path):
        for root, _, files in os.walk(folder_path):
            for file in files:
                path = os.path.join(root, file)
                try:
                    with open(path, 'r', errors='ignore') as f:
                        content = f.read()
                    self.index[path] = content
                except:
                    self.index[path] = ""
        messagebox.showinfo("🌸 Indexing Complete!", "Ready to search your kawaii files! 🐱")

    def search_files(self):
        keyword = self.search_var.get().lower()
        self.results_listbox.delete(0, tk.END)
        if not self.index:
            messagebox.showwarning("Oops!", "Please select your file first 🥺")
            return
        self.wait_label.config(text="Please wait... ⏳")
        self.master.update()
        local_index = dict(self.index)
        for path, content in local_index.items():
            if keyword in path.lower() or keyword in content.lower():
                self.results_listbox.insert(tk.END, path)
        self.wait_label.config(text="")

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSearchApp(root)
    root.mainloop()
