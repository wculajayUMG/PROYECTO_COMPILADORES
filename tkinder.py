import tkinter as tk
from tkinter import ttk
import re

class CompiladorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("COMPILADOR")
        self.root.state('zoomed')
        self.setup_ui()

    def setup_ui(self):
        imagen = tk.PhotoImage(file="logo.png")
        # Labels
        tk.Label(self.root, text="ANALIZADOR SINTÁCTICO", font=("Arial", 28, "bold")).place(x=500, y=50)
        tk.Label(self.root, text="ENTRADA (editor de texto)", font=("Arial", 24)).place(x=65, y=200)
        tk.Label(self.root, text="PRESIONA F5 PARA EJECUTAR", font=("Arial", 16)).place(x=50, y=580)
        tk.Label(self.root, text="V", font=("Arial Black", 18)).place(x=630, y=232)
        tk.Label(self.root, text="T", font=("Arial Black", 18)).place(x=730, y=232)
        tk.Label(self.root, text="VECTORES", font=("Arial", 24)).place(x=600, y=195)
        tk.Label(self.root, text="MATRIZ DE PRODUCCIÓN", font=("Arial", 24)).place(x=970, y=200)
        tk.Label(self.root, text="Willy Culajay", font=("Arial", 14)).place(x=5, y=20)
        tk.Label(self.root, text="Laboratorio de Compiladores", font=("ARIAL", 14)).place(x=5, y=50)
         # Mostrar la imagen en un widget Label
        label_imagen = tk.Label(self.root, image=imagen) 
        label_imagen.image = imagen
        label_imagen.pack()
        label_imagen.place(x=1400, y=10)
        # TextArea para entrada
        self.texto = tk.Text(self.root, font=("Arial", 33), wrap="word")
        self.texto.place(x=50, y=250, width=400, height=400)
        self.texto.bind("<F5>", self.procesar_texto)

        # Vectores
        self.textoA = tk.Text(self.root, font=("Arial", 25), wrap="word")
        self.textoA.place(x=600, y=280, width=80, height=370)
        self.textoA.tag_configure("center", justify="center")
        

        self.textoT = tk.Text(self.root, font=("Arial", 25), wrap="word")
        self.textoT.place(x=700, y=280, width=80, height=370)
        self.textoT.tag_configure("center", justify="center")

        # Matriz de producción
        self.tree = ttk.Treeview(self.root, columns=("Variable", "Producción"), show="headings", height=12)
        self.tree.heading("Variable", text=" Variable  ")
        self.tree.heading("Producción", text="Producción")
        self.tree.column("Variable", anchor="center", width=150)
        self.tree.column("Producción", anchor="center", width=300)
        style = ttk.Style()
        style.configure("Treeview.Heading", font=("arial black", 20), background="lightgray")
        style.configure("Treeview", font=("Arial", 20), rowheight=30)

        self.tree.place(x=950, y=250)

        # Líneas divisorias
        tk.Frame(self.root, bg="darkgray", height=7, width=1600).place(x=0, y=150)
        tk.Frame(self.root, bg="darkgray", height=7, width=1600).place(x=0, y=750)

    def procesar_texto(self, event=None):
        texto = self.texto.get("1.0", tk.END)
        variables_set = set()
        terminales_set = set()

        for i in self.tree.get_children():
            self.tree.delete(i)

        lineas = texto.strip().split("\n")
        for linea in lineas:
            partes = linea.split(":")
            if len(partes) == 2:
                variable = partes[0].strip()
                variables_set.add(variable)
                reglas = partes[1].split("|")

                for regla in reglas:
                    produccion = ""
                    regla = regla.strip()
                    tokens = re.findall(r"'[^']*'|[A-Za-z0-9]+", regla)
                    for token in tokens:
                        if token.startswith("'") and token.endswith("'"):
                            terminal = token[1:-1]
                            terminales_set.add(terminal)
                            produccion += terminal
                        elif token == "e":
                            terminales_set.add("e")
                            produccion += "e"
                        else:
                            produccion += token
                    self.tree.insert("", "end", values=(variable, produccion))

        # Mostrar vectores
        self.textoA.delete("1.0", tk.END)
        for v in sorted(variables_set):
            self.textoA.insert(tk.END, v + "\n")

        self.textoT.delete("1.0", tk.END)
        for t in sorted(terminales_set):
            self.textoT.insert(tk.END, t + "\n")
            
            variables_texto = "\n".join(sorted(variables_set))
            terminales_texto = "\n".join(sorted(terminales_set))

        self.textoA.delete("1.0", tk.END)
        self.textoA.insert(tk.END, variables_texto)
        self.textoA.tag_add("center", "1.0", tk.END) 

        self.textoT.delete("1.0", tk.END)
        self.textoT.insert(tk.END,terminales_texto)
        self.textoT.tag_add("center", "1.0",tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = CompiladorApp(root)
    root.mainloop()