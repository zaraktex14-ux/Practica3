import json
import tkinter as tk
from tkinter import Frame, ttk, messagebox, scrolledtext
from tkinter import filedialog 
import herramientas 
import afd, afnd

mi_afd = afd.AFD()
#mi_afnd = afnd.AFND()
def cargar_automata_archivo():
    ruta = filedialog.askopenfilename(
        title="Seleccionar Autómata",
        filetypes=(("Archivos AFD", "*.afd"), ("Archivos JFLAP", "*.jff"), ("Todos", "*.*"))
    )
    
    if not ruta:
        return

    try:
        if ruta.endswith('.afd'):
            with open(ruta, 'r') as f:
                datos = json.load(f)
                global mi_afd
                mi_afd = afd.AFD.from_dict(datos)
        
        elif ruta.endswith('.jff'):

            with open(ruta, 'r') as f:
                contenido = f.read()
                mi_afd = afd.AFD.from_jff_format(contenido)

        actualizar_interfaz_afd()
        messagebox.showinfo("Éxito", "Autómata cargado correctamente")
        
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar: {str(e)}")
def guardar_automata_archivo():
    if not mi_afd.states:
        messagebox.showwarning("Atención", "No hay un autómata configurado para guardar.")
        return

    ruta = filedialog.asksaveasfilename(
        defaultextension=".afd",
        filetypes=(("Archivos AFD", "*.afd"), ("Todos", "*.*"))
    )
    
    if ruta:
        try:
            datos = mi_afd.to_dict()
            with open(ruta, 'w') as f:
                json.dump(datos, f, indent=4)
            messagebox.showinfo("Éxito", f"Autómata guardado en:\n{ruta}")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo guardar: {str(e)}")

def limpiar_interfaz_y_datos():
    if messagebox.askyesno("Confirmar", "¿Estás seguro de que quieres borrar el autómata actual?"):
        global mi_afd
        mi_afd = afd.AFD() 
        actualizar_interfaz_afd() 
        lbl_res_afd.config(text="")
        entry_probar.delete(0, tk.END) 
        messagebox.showinfo("Limpiar", "Simulador reiniciado correctamente.")

def actualizar_interfaz_afd():
    for item in tree_trans.get_children():
        tree_trans.delete(item)
   
    for (f, s), t in mi_afd.transitions.items():
        tree_trans.insert("", "end", values=(f.name, s, t.name))

    nombres = [s.name for s in mi_afd.states]
    cb_desde['values'] = nombres
    cb_hacia['values'] = nombres

def agregar_estado_interfaz():
    nombre = entry_estado_nombre.get().strip()
    es_ini = var_es_inicial.get()
    es_fin = var_es_final.get()
    
    if nombre:
        nuevo = mi_afd.add_state(nombre, es_ini, es_fin)
        if nuevo:
            listado = [s.name for s in mi_afd.states]
            cb_desde['values'] = listado
            cb_hacia['values'] = listado
            messagebox.showinfo("Éxito", f"Estado {nombre} agregado")
        else:
            messagebox.showerror("Error", "El estado ya existe")
    
def agregar_transicion_interfaz():
    f = cb_desde.get()
    s = entry_simbolo.get()
    t = cb_hacia.get()
    if mi_afd.add_transition(f, s, t):
        tree_trans.insert("", "end", values=(f, s, t))
    else:
        messagebox.showerror("Error", "Datos invalidos o estados no seleccionados")

def probar_cadena():
    cadena = entry_probar.get()
    valido, camino = mi_afd.validate_string(cadena)
    color = "green" if valido else "red"
    lbl_res_afd.config(text=f"Resultado: {'Aceptada' if valido else 'Rechazada'}\nRuta: {camino}", fg=color)
    
def probar_cadena():
    cadena = entry_probar.get()
    
    # Obtenemos el resultado booleano y la LISTA de pasos
    valido, pasos = mi_afd.validate_string(cadena)

    # 1. El Label SOLO muestra el resultado (Aceptada/Rechazada)
    color = "green" if valido else "red"
    lbl_res_afd.config(
        text=f"Resultado: {'Válido' if valido else 'Inválido'}",
        fg=color
    )

    # 2. Mostramos los pasos en el ScrolledText (tu "tabla")
    # Asegúrate de que el nombre del widget sea el que tú usas (ej. txt_analisis)
    txt_analisis.config(state="normal") # Habilitar edición
    txt_analisis.delete(1.0, "end")    # Limpiar lo anterior
    
    txt_analisis.insert("end", f"ANÁLISIS DE LA CADENA: '{cadena}'\n")
    txt_analisis.insert("end", "="*45 + "\n\n")

    # Recorremos la lista de pasos para imprimirlos uno por uno
    for p in pasos:
        txt_analisis.insert("end", f"PASO {p['paso']}:\n")
        txt_analisis.insert("end", f"  Estado Actual: \t{p['estado']}\n")
        txt_analisis.insert("end", f"  Símbolo Leído: \t{p['leer']}\n")
        txt_analisis.insert("end", f"  Restante:      \t{p['cadena_restante']}\n")
        txt_analisis.insert("end", f"  Operación:     \t{p['info']}\n")
        txt_analisis.insert("end", "-"*30 + "\n")

    txt_analisis.config(state="disabled") 

def validate_string(self):
    input_string = self.input_string_var.get()
    
    is_accepted, steps = mi_afd.validate_string(input_string)
    
    self.simulation_steps = steps
    self.current_step = 0

    if is_accepted:
        self.validation_result_var.set("Resultado: Válido")
        self.validation_result_label.configure(foreground="green")
    else:
        self.validation_result_var.set("Resultado: Inválido")
        self.validation_result_label.configure(foreground="red")
 
    self.update_simulation_view()



def ejecutar_minimizacion(self):
    self.simulation_text.config(state=tk.NORMAL)
    self.simulation_text.delete('1.0', tk.END)
  
    resultado_min = mi_afd.minimizar_y_reportar()
    

    self.simulation_text.insert(tk.END, resultado_min)

    self.simulation_text.insert(tk.END, "\n" + "="*50 + "\n")
    self.simulation_text.insert(tk.END, "Proceso finalizado.")
    
    self.simulation_text.config(state=tk.DISABLED)

def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()
    x = (pantalla_ancho // 2) - (ancho // 2)
    y = (pantalla_alto // 2) - (alto // 2)
    ventana.geometry(f"{ancho}x{alto}+{x}+{y}")

def ejecutar_analisis_cadena():
    cadena = entry_cadena.get()
    if not cadena:
        messagebox.showwarning("Atención", "Escribe una cadena primero")

    prefijos, sufijos, subcadenas = herramientas.obtener_analisis_cadena(cadena)
    
    txt_analisis.delete(1.0, tk.END)
    txt_analisis.insert(tk.END, f"Analizando cadena: '{cadena}'\n")
    txt_analisis.insert(tk.END, "-"*40 + "\n")
    txt_analisis.insert(tk.END, f"PREFIJOS: {', '.join([p if p != '' else 'λ' for p in prefijos])}\n\n")
    txt_analisis.insert(tk.END, f"SUFIJOS: {', '.join([s if s != '' else 'λ' for s in sufijos])}\n\n")
    txt_analisis.insert(tk.END, f"SUBCADENAS ({len(subcadenas)}): {', '.join(subcadenas)}")

def ejecutar_calculo_kleene():
    alfabeto = entry_alfabeto.get()
    try:
        limite = int(entry_limite.get())

        star, plus = herramientas.calcular_kleene_logic(alfabeto, limite)
        
        txt_resultados.delete(1.0, tk.END)
        txt_resultados.insert(tk.END, f"Σ* (Kleene): {', '.join(star)}\n\n")
        txt_resultados.insert(tk.END, f"Σ+ (Positiva): {', '.join(plus)}")
    except ValueError:
        messagebox.showerror("Error", "La longitud debe ser un número entero")

root = tk.Tk()
root.title("Practicas de Teoría de la Computación")
centrar_ventana(root, 900, 700)


portada = tk.Frame(root, bg="#0B436E", pady=20)
portada.pack(fill="x")
tk.Label(portada, text="TEORÍA DE LA COMPUTACIÓN", font=("Arial", 18, "bold"), fg="white", bg="#0B436E").pack()
tk.Label(portada, text="Resendiz Garcia Renata", font=("Arial", 10), fg="#d2dae2", bg="#0B436E").pack()
tk.Label(portada, text="Hernandez Hernandez Wendy", font=("Arial", 10), fg="#d2dae2", bg="#0B436E").pack()
tk.Label(portada, text="Perez Griselda", font=("Arial", 10), fg="#d2dae2", bg="#0B436E").pack()

notebook = ttk.Notebook(root)
notebook.pack(expand=True, fill="both", padx=20, pady=20)

# --- PESTAÑA 1: KLEENE ---
tab_kleene = tk.Frame(notebook, bg="white")
notebook.add(tab_kleene, text=" Cerraduras (Kleene) ")

frame_k = tk.Frame(tab_kleene, bg="white", pady=10)
frame_k.pack()

tk.Label(frame_k, text="Alfabeto:", bg="white").grid(row=0, column=0)
entry_alfabeto = tk.Entry(frame_k)
entry_alfabeto.grid(row=0, column=1, padx=5)

tk.Label(frame_k, text="Longitud Máx:", bg="white").grid(row=0, column=2)
entry_limite = tk.Entry(frame_k, width=5)
entry_limite.insert(0, "3")
entry_limite.grid(row=0, column=3, padx=5)

btn_k = tk.Button(frame_k, text="Calcular", command=ejecutar_calculo_kleene, bg="#344fe7", fg="white")
btn_k.grid(row=0, column=4, padx=10)

txt_resultados = scrolledtext.ScrolledText(tab_kleene, height=15, width=80)
txt_resultados.pack(pady=10, padx=10)


# --- PESTAÑA 2: SUBCADENAS ---
tab_tools = tk.Frame(notebook, bg="white")
notebook.add(tab_tools, text=" Subcadenas/Sufijos ")

frame_c = tk.Frame(tab_tools, bg="white", pady=15)
frame_c.pack()

tk.Label(frame_c, text="Cadena:", bg="white").grid(row=0, column=0)
entry_cadena = tk.Entry(frame_c, width=30)
entry_cadena.grid(row=0, column=1, padx=10)

btn_c = tk.Button(frame_c, text="Analizar", command=ejecutar_analisis_cadena, bg="#0B436E", fg="white")
btn_c.grid(row=0, column=2, padx=5)

txt_analisis = scrolledtext.ScrolledText(tab_tools, height=15, width=80)
txt_analisis.pack(pady=10, padx=20)

# --- PESTAÑA 3: AFD ---

tab_afd = tk.Frame(notebook, bg="white")
notebook.add(tab_afd, text=" Definir AFD ")
f_acciones = tk.Frame(tab_afd, bg="white")
f_acciones.pack(fill="x", padx=10, pady=5)
btn_cargar = tk.Button(f_acciones, text="Cargar", command=cargar_automata_archivo, 
                       bg="#2ecc71", fg="white", width=12)
btn_cargar.pack(side="left", padx=5)

btn_guardar = tk.Button(f_acciones, text="Guardar", command=guardar_automata_archivo, 
                        bg="#3498db", fg="white", width=12)
btn_guardar.pack(side="left", padx=5)

btn_limpiar = tk.Button(f_acciones, text="Limpiar", command=limpiar_interfaz_y_datos, 
                        bg="#e74c3c", fg="white", width=12)
btn_limpiar.pack(side="left", padx=5)

f_estados = ttk.LabelFrame(tab_afd, text=" 1. Agregar Estados ")
f_estados.pack(fill="x", padx=10, pady=5)

tk.Label(f_estados, text="Nombre:").grid(row=0, column=0, padx=5)
entry_estado_nombre = tk.Entry(f_estados, width=10)
entry_estado_nombre.grid(row=0, column=1, padx=5)

var_es_inicial = tk.BooleanVar()
tk.Checkbutton(f_estados, text="Inicial", variable=var_es_inicial).grid(row=0, column=2)

var_es_final = tk.BooleanVar()
tk.Checkbutton(f_estados, text="Final", variable=var_es_final).grid(row=0, column=3)

tk.Button(f_estados, text="Añadir", command=agregar_estado_interfaz).grid(row=0, column=4, padx=10)


f_trans = ttk.LabelFrame(tab_afd, text=" 2. Definir Transiciones ")
f_trans.pack(fill="x", padx=10, pady=5)

cb_desde = ttk.Combobox(f_trans, width=10, state="readonly")
cb_desde.grid(row=0, column=0, padx=5)
tk.Label(f_trans, text="--").grid(row=0, column=1)
entry_simbolo = tk.Entry(f_trans, width=5)
entry_simbolo.grid(row=0, column=2, padx=5)
tk.Label(f_trans, text="-->").grid(row=0, column=3)
cb_hacia = ttk.Combobox(f_trans, width=10, state="readonly")
cb_hacia.grid(row=0, column=4, padx=5)

tk.Button(f_trans, text="Asignar", command=agregar_transicion_interfaz).grid(row=0, column=5, padx=10)

#tablita
tree_trans = ttk.Treeview(tab_afd, columns=("De", "Símbolo", "A"), show="headings", height=5)
tree_trans.heading("De", text="Estado Origen")
tree_trans.heading("Símbolo", text="Símbolo")
tree_trans.heading("A", text="Estado Destino")
tree_trans.pack(fill="x", padx=10, pady=5)


f_prueba = ttk.LabelFrame(tab_afd, text=" 3. Probar Cadena ")
f_prueba.pack(fill="x", padx=10, pady=5)

entry_probar = tk.Entry(f_prueba)
entry_probar.pack(side="left", padx=10, pady=5, expand=True, fill="x")
tk.Button(f_prueba, text="Validar", command=probar_cadena).pack(side="right", padx=10)

lbl_res_afd = tk.Label(tab_afd, text="", font=("Arial", 10, "bold"), bg="white")
lbl_res_afd.pack(pady=10)

btn_cargar = tk.Button(f_acciones, text="Minimizar", command=ejecutar_minimizacion, 
                       bg="#cc9a2e", fg="white", width=12)
btn_cargar.pack(side="left", padx=5)

root.mainloop()