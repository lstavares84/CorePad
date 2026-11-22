"""CorePad local configuration editor. USB transport is not yet implemented."""
import json
import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox, ttk
from device import Simulator, default_config, load, validate

class Configurator:
    def __init__(self, root):
        self.root=root; self.simulator=Simulator(); self.config=default_config()
        root.title("CorePad Beta — configurador de desenvolvimento")
        ttk.Label(root,text="Modo local / simulador — conexão USB ainda indisponível").pack(padx=16,pady=10)
        bar=ttk.Frame(root);bar.pack(fill="x",padx=16)
        self.color=tk.StringVar(value="#00ff00");self.brightness=tk.IntVar(value=32);self.enabled=tk.BooleanVar()
        ttk.Button(bar,text="Escolher cor RGB",command=self.choose).pack(side="left")
        ttk.Label(bar,textvariable=self.color).pack(side="left",padx=8)
        ttk.Checkbutton(bar,text="Iluminação ligada",variable=self.enabled).pack(side="left")
        ttk.Label(root,text="Brilho (0–255)").pack()
        tk.Scale(root,from_=0,to=255,orient="horizontal",variable=self.brightness,length=400).pack()
        notebook=ttk.Notebook(root);notebook.pack(fill="both",expand=True,padx=16,pady=8)
        self.entries=[]
        for layer in range(2):
            tab=ttk.Frame(notebook);notebook.add(tab,text=f"Camada {layer+1}");items=[]
            for key in range(9):
                ttk.Label(tab,text=f"Tecla {key+1}").grid(row=key,column=0,padx=5,pady=3)
                entry=ttk.Entry(tab,width=70);entry.grid(row=key,column=1,padx=5,pady=3);items.append(entry)
            self.entries.append(items)
        footer=ttk.Frame(root);footer.pack(pady=12)
        for name,callback in [("Abrir JSON",self.open),("Salvar JSON",self.save),("Aplicar no simulador",self.apply)]:
            ttk.Button(footer,text=name,command=callback).pack(side="left",padx=5)
        ttk.Label(root,text="A camada protegida não é exportada por este editor.").pack(pady=5)
    def choose(self):
        color=colorchooser.askcolor(color=self.color.get())[1]
        if color:self.color.set(color)
    def current(self):
        return validate({"version":1,"rgb":{"color":self.color.get(),"brightness":self.brightness.get(),"enabled":self.enabled.get()},
                         "macros":[[entry.get() for entry in layer] for layer in self.entries]})
    def open(self):
        path=filedialog.askopenfilename(filetypes=[("CorePad JSON","*.json")])
        if not path:return
        try:
            c=load(path);self.color.set(c["rgb"]["color"]);self.brightness.set(c["rgb"]["brightness"]);self.enabled.set(c["rgb"]["enabled"])
            for entries,values in zip(self.entries,c["macros"]):
                for entry,value in zip(entries,values):entry.delete(0,tk.END);entry.insert(0,value)
        except (ValueError,OSError,UnicodeError) as error:messagebox.showerror("Configuração",str(error))
    def save(self):
        try:
            config=self.current();path=filedialog.asksaveasfilename(defaultextension=".json",filetypes=[("CorePad JSON","*.json")])
            if path:
                with open(path,"w",encoding="utf-8") as stream:json.dump(config,stream,ensure_ascii=False,indent=2)
        except (ValueError,OSError) as error:messagebox.showerror("Configuração",str(error))
    def apply(self):
        try:
            self.simulator.request({"command":"set_config","config":self.current()})
            messagebox.showinfo("Simulador","Configuração aplicada ao simulador em memória.")
        except ValueError as error:messagebox.showerror("Configuração",str(error))

if __name__=="__main__":
    root=tk.Tk();Configurator(root);root.mainloop()
