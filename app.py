import tkinter as tk
from tkinter import filedialog, messagebox, Toplevel, ttk
from PIL import Image, ImageTk
from ultralytics import YOLO
import cv2
import numpy as np
import json
import glob
import os
from datetime import datetime
MODEL_PATH = 'best.pt'

# --- DICCIONARIO DE TRADUCCIÓN ---
TRADUCCION = {
    'Clear plastic bottle': 'Botella Plástica',
    'Plastic bottle cap': 'Tapa de Botella',
    'Drink can': 'Lata de Bebida',
    'Plastic film': 'Envoltura Plástica',
    'Plastic bag': 'Bolsa Plástica',
    'Other plastic': 'Otro Plástico',
    'Glass bottle': 'Botella de Vidrio',
    'Broken glass': 'Vidrio Roto',
    'Styrofoam piece': 'Icopor',
    'Cigarette': 'Colilla de Cigarro',
    'Unlabeled litter': 'Basura Genérica',
    'Single-use carrier bag': 'Bolsa de un solo uso',
    'Pop tab': 'Anillo de lata',
    'Plastic straw': 'Pitillo/Popote'
}

class SmartCityApp:
    def __init__(self, root):
        self.root = root
        self.root.title("EcoVision - Smart City PDI")
        self.root.geometry("1200x850")
        self.root.configure(bg="#ffffff")
        
        self.model = None
        self.cap = None 
        self.video_running = False
        self.ultima_deteccion_info = [] 
        
        self.cargar_modelo()
        self.mostrar_menu_principal()

    def cargar_modelo(self):
        try:
            print("Cargando modelo...")
            self.model = YOLO(MODEL_PATH)
            print("Modelo cargado.")
        except Exception as e:
            messagebox.showerror("Error", f"No se encontró el modelo best.pt\n{e}")

    def limpiar_ventana(self):
        
        self.video_running = False
        if self.cap is not None:
            self.cap.release()
        
        for widget in self.root.winfo_children():
            widget.destroy()

    # MENÚ PRINCIPAL
    def mostrar_menu_principal(self):
        self.limpiar_ventana()
        frame_menu = tk.Frame(self.root, bg="white")
        frame_menu.pack(expand=True)

        tk.Label(frame_menu, text="EcoVision", font=("Helvetica", 40, "bold"), fg="#2E7D32", bg="white").pack(pady=10)
        tk.Label(frame_menu, text="Detección Inteligente de Residuos Urbanos", font=("Helvetica", 16), fg="gray", bg="white").pack(pady=(0, 40))

        tk.Button(frame_menu, text="INICIAR ESCANEO", font=("Helvetica", 16, "bold"), bg="#4CAF50", fg="white", width=25, height=2, cursor="hand2", command=self.mostrar_app_principal).pack(pady=10)
        
        tk.Button(frame_menu, text="📂 Historial de Reportes", font=("Helvetica", 14), bg="#0D47A1", fg="white", width=25, cursor="hand2", command=self.mostrar_reportes).pack(pady=10)

        tk.Button(frame_menu, text="Instrucciones", font=("Helvetica", 12), bg="#2196F3", fg="white", width=25, cursor="hand2", command=self.mostrar_instrucciones).pack(pady=10)


    # Sección INSTRUCCIONES
    def mostrar_instrucciones(self):
        self.limpiar_ventana()
        frame_inst = tk.Frame(self.root, bg="white", padx=50, pady=20)
        frame_inst.pack(expand=True, fill="both")

        tk.Label(frame_inst, text="Instrucciones de Uso", font=("Helvetica", 24, "bold"), bg="white", fg="#333").pack(pady=10)
        
        texto = ("1. Presiona 'Subir Archivo' (Soporta IMÁGENES y VIDEOS).\n"
                 "2. Si es video, se reproducirá analizando cada cuadro.\n"
                 "3. El semáforo indicará el nivel de contaminación.\n"
                 "4. Si hay alerta, usa el botón de 'Campaña' para generar el reporte.")
        
        tk.Label(frame_inst, text=texto, font=("Helvetica", 14), justify="left", bg="white", fg="#555").pack(pady=10)
        
       
        frame_leyenda = tk.Frame(frame_inst, bg="#f9f9f9", bd=2, relief="groove", padx=20, pady=10)
        frame_leyenda.pack(pady=10, fill="x")

        tk.Label(frame_leyenda, text="🟢 NIVEL LEVE (1-2 Objetos):", font=("Helvetica", 12, "bold"), fg="#2E7D32", bg="#f9f9f9").pack(anchor="w")
        tk.Label(frame_leyenda, text="   Indica contaminación mínima. Se sugiere campaña preventiva.", font=("Helvetica", 11), bg="#f9f9f9").pack(anchor="w", pady=(0,5))

        tk.Label(frame_leyenda, text="🟡 ALERTA (3-5 Objetos):", font=("Helvetica", 12, "bold"), fg="#F9A825", bg="#f9f9f9").pack(anchor="w")
        tk.Label(frame_leyenda, text="   Nivel medio de suciedad. Se recomienda programar limpieza.", font=("Helvetica", 11), bg="#f9f9f9").pack(anchor="w", pady=(0,5))

        tk.Label(frame_leyenda, text="🔴 ALERTA MÁXIMA (> 5 Objetos):", font=("Helvetica", 12, "bold"), fg="#C62828", bg="#f9f9f9").pack(anchor="w")
        tk.Label(frame_leyenda, text="   Zona crítica. Se requiere limpieza urgente inmediata.", font=("Helvetica", 11), bg="#f9f9f9").pack(anchor="w")

        btn_volver = tk.Button(frame_inst, text="⬅ Volver al Menú", font=("Helvetica", 12), bg="#777", fg="white", command=self.mostrar_menu_principal)
        btn_volver.pack(pady=20)


    # HISTORIAL DE REPORTES
    def mostrar_reportes(self):
        self.limpiar_ventana()
        
        # Cabecera
        header = tk.Frame(self.root, bg="#eee", height=50)
        header.pack(fill="x")
        tk.Button(header, text="⬅ Menú", command=self.mostrar_menu_principal, bg="#ddd").pack(side="left", padx=10, pady=10)
        tk.Label(header, text="Historial de Reportes Ambientales", font=("Helvetica", 14, "bold"), bg="#eee").pack(side="left", padx=20)

        content = tk.Frame(self.root, bg="white", padx=20, pady=20)
        content.pack(expand=True, fill="both")

        # Lista archivos
        frame_lista = tk.Frame(content, bg="white", width=300)
        frame_lista.pack(side="left", fill="y", padx=(0, 20))

        tk.Label(frame_lista, text="Archivos Disponibles:", font=("Helvetica", 12, "bold"), bg="white").pack(anchor="w")
        
        
        archivos = glob.glob("reporte_ambiental_*.json")
        archivos.sort(reverse=True) 

        scrollbar = tk.Scrollbar(frame_lista)
        scrollbar.pack(side="right", fill="y")
        
        self.lista_reportes = tk.Listbox(frame_lista, width=40, height=25, font=("Courier", 10), yscrollcommand=scrollbar.set)
        self.lista_reportes.pack(side="left", fill="both")
        scrollbar.config(command=self.lista_reportes.yview)


        if not archivos:
            self.lista_reportes.insert(tk.END, "No hay reportes guardados.")
        else:
            for arch in archivos:
                self.lista_reportes.insert(tk.END, arch)
        
        self.lista_reportes.bind('<<ListboxSelect>>', self.cargar_detalle_reporte)

        frame_detalle = tk.Frame(content, bg="#f9f9f9", bd=2, relief="sunken")
        frame_detalle.pack(side="right", expand=True, fill="both")

        tk.Label(frame_detalle, text="Detalle del Informe", font=("Helvetica", 12, "bold"), bg="#f9f9f9").pack(pady=10)
        
        self.txt_detalle = tk.Text(frame_detalle, font=("Helvetica", 11), bg="#f9f9f9", wrap="word", padx=20, pady=20)
        self.txt_detalle.pack(expand=True, fill="both")

    def cargar_detalle_reporte(self, event):
        selection = self.lista_reportes.curselection()
        if not selection: return
        
        archivo_seleccionado = self.lista_reportes.get(selection[0])
        
        try:
            with open(archivo_seleccionado, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            texto_mostrar = (
                f"📅 FECHA: {data.get('fecha_reporte', 'N/A')}\n"
                f"📍 CIUDAD: {data['ubicacion'].get('ciudad', 'N/A')}\n"
                f"🏘️ BARRIO: {data['ubicacion'].get('barrio', 'N/A')}\n"
                f"🌳 LUGAR: {data['ubicacion'].get('lugar_especifico', 'N/A')}\n\n"
                f"{'-'*40}\n"
                f"📊 ESTADO: {data.get('estado_alerta', 'N/A')}\n"
                f"{'-'*40}\n\n"
                f"🔍 HALLAZGOS IA:\n"
            )
            
            detalles_ia = data['analisis_ia'].get('detalle', [])
            if detalles_ia:
                conteo = {x: detalles_ia.count(x) for x in detalles_ia}
                for k, v in conteo.items():
                    texto_mostrar += f"   • {k}: {v}\n"
            else:
                texto_mostrar += "   No se detectaron objetos específicos.\n"

            self.txt_detalle.config(state="normal")
            self.txt_detalle.delete(1.0, tk.END)
            self.txt_detalle.insert(tk.END, texto_mostrar)
            self.txt_detalle.config(state="disabled")
            
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo leer el archivo: {e}")




    # APP PRINCIPAL
    def mostrar_app_principal(self):
        self.limpiar_ventana()

        header = tk.Frame(self.root, bg="#eee", height=50)
        header.pack(fill="x")
        tk.Button(header, text="Inicio", command=self.mostrar_menu_principal, bg="#ddd").pack(side="left", padx=10, pady=10)
        tk.Label(header, text="Análisis de Zona (Imagen/Video)", font=("Helvetica", 14, "bold"), bg="#eee").pack(side="left", padx=20)

        self.content_frame = tk.Frame(self.root, bg="white")
        self.content_frame.pack(expand=True, fill="both", padx=20, pady=10)

        self.btn_subir = tk.Button(self.content_frame, text="📂 Subir Imagen o Video", font=("Helvetica", 14), bg="#2196F3", fg="white", command=self.cargar_archivo)
        self.btn_subir.pack(pady=5)

        self.imgs_container = tk.Frame(self.content_frame, bg="white")
        self.imgs_container.pack(pady=10)

        # Izquierda: Original
        frame_izq = tk.Frame(self.imgs_container, bg="white")
        frame_izq.grid(row=0, column=0, padx=10)
        tk.Label(frame_izq, text="Entrada", font=("Helvetica", 10, "bold"), bg="white").pack()
        self.lbl_img_original = tk.Label(frame_izq, bg="#f0f0f0", width=50, height=20)
        self.lbl_img_original.pack()

        # Derecha: IA
        frame_der = tk.Frame(self.imgs_container, bg="white")
        frame_der.grid(row=0, column=1, padx=10)
        tk.Label(frame_der, text="Detección IA", font=("Helvetica", 10, "bold"), bg="white").pack()
        self.lbl_img_resultado = tk.Label(frame_der, bg="#f0f0f0", width=50, height=20)
        self.lbl_img_resultado.pack()

        # Alertas
        self.frame_alerta = tk.Frame(self.content_frame, bg="white", pady=10)
        self.frame_alerta.pack(fill="x")
        
        self.lbl_estado = tk.Label(self.frame_alerta, text="Esperando archivo...", font=("Helvetica", 18, "bold"), bg="white", fg="#777")
        self.lbl_estado.pack()
        self.lbl_detalle = tk.Label(self.frame_alerta, text="", font=("Helvetica", 12), bg="white", fg="#555")
        self.lbl_detalle.pack()


        self.btn_campana = tk.Button(self.content_frame, text="📢 REPORTE", font=("Helvetica", 12, "bold"), state="disabled", command=self.abrir_formulario_campana)

    def cargar_archivo(self):
        self.video_running = False 
        ruta = filedialog.askopenfilename(filetypes=[("Archivos Media", "*.jpg *.jpeg *.png *.mp4 *.avi")])
        if not ruta: return

        ext = ruta.split('.')[-1].lower()
        
        if ext in ['mp4', 'avi', 'mov']:
   
            self.procesar_video(ruta)
        else:
      
            self.procesar_imagen(ruta)

    # Lógica imagen
    def procesar_imagen(self, ruta):
  
        img_orig = Image.open(ruta)
        img_orig.thumbnail((450, 350))
        photo_orig = ImageTk.PhotoImage(img_orig)
        self.lbl_img_original.config(image=photo_orig, width=0, height=0)
        self.lbl_img_original.image = photo_orig

  
        if self.model:
            results = self.model.predict(source=ruta, conf=0.25)
            self.mostrar_resultado_ia(results[0])

    # Lógica vídeo
    def procesar_video(self, ruta):
        self.cap = cv2.VideoCapture(ruta)
        self.video_running = True
        self.loop_video()

    def loop_video(self):
        if self.video_running and self.cap.isOpened():
            ret, frame = self.cap.read()
            if ret:
           
                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img_pil = Image.fromarray(frame_rgb)
                img_pil.thumbnail((450, 350))
                img_tk = ImageTk.PhotoImage(img_pil)
                self.lbl_img_original.config(image=img_tk, width=0, height=0)
                self.lbl_img_original.image = img_tk

             
                if self.model:
                
                    results = self.model.track(source=frame, conf=0.25, persist=True, verbose=False)
                    res_plotted = results[0].plot()
                    
                    # Convertir para Tkinter
                    res_rgb = cv2.cvtColor(res_plotted, cv2.COLOR_BGR2RGB)
                    res_pil = Image.fromarray(res_rgb)
                    res_pil.thumbnail((450, 350))
                    res_tk = ImageTk.PhotoImage(res_pil)
                    
                    self.lbl_img_resultado.config(image=res_tk, width=0, height=0)
                    self.lbl_img_resultado.image = res_tk
                    
              
                    self.analizar_resultados_base(results[0])

           
                self.root.after(33, self.loop_video)
            else:
                self.video_running = False
                self.cap.release()

    # Alertas
    def mostrar_resultado_ia(self, resultado):
        img_array = resultado.plot()
        img_rgb = cv2.cvtColor(img_array, cv2.COLOR_BGR2RGB)
        img_pil = Image.fromarray(img_rgb)
        img_pil.thumbnail((450, 350))
        img_tk = ImageTk.PhotoImage(img_pil)
        
        self.lbl_img_resultado.config(image=img_tk, width=0, height=0)
        self.lbl_img_resultado.image = img_tk
        self.analizar_resultados_base(resultado)

    def analizar_resultados_base(self, resultado):
        clases_ids = resultado.boxes.cls.cpu().numpy()
        cantidad = len(clases_ids)
        
        # Traducir nombres
        nombres = []
        for cls_id in clases_ids:
            eng = resultado.names[int(cls_id)]
            esp = TRADUCCION.get(eng, eng)
            nombres.append(esp)
        
        # Guardamos para el formulario
        self.ultima_deteccion_info = nombres


        self.btn_campana.pack_forget()
        bg, txt_col, txt_est = "white", "black", ""

        if cantidad == 0:
            txt_est = "🌿 Zona Limpia"
            bg, txt_col = "#E8F5E9", "#2E7D32"
        elif 1 <= cantidad <= 2:
            txt_est = "🟢 CONTAMINACIÓN LEVE"
            bg, txt_col = "#C8E6C9", "#1B5E20"
            self.config_boton_campana("gray", "Campaña Preventiva")
        elif 3 <= cantidad <= 5:
            txt_est = "🟡 ALERTA AMBIENTAL"
            bg, txt_col = "#FFF9C4", "#FBC02D"
            self.config_boton_campana("#FF9800", "⚠️ PROGRAMAR LIMPIEZA")
        else:
            txt_est = "🔴 EMERGENCIA SANITARIA"
            bg, txt_col = "#FFCDD2", "#C62828"
            self.config_boton_campana("#D32F2F", "🚨 REPORTE URGENTE")

        self.lbl_estado.config(text=txt_est, fg=txt_col, bg=bg)
        self.frame_alerta.config(bg=bg)
        

        resumen = ", ".join(set([f"{nombres.count(x)} {x}" for x in nombres]))
        if len(resumen) > 120: resumen = resumen[:120] + "..." 
        self.lbl_detalle.config(text=f"Detectado: {resumen}", bg=bg)

    def config_boton_campana(self, color, texto):
        self.btn_campana.pack(pady=10)
        self.btn_campana.config(bg=color, fg="white", state="normal", text=texto)

    # Formulario
    def abrir_formulario_campana(self):
       
        if self.video_running:
            self.video_running = False

        form = Toplevel(self.root)
        form.title("Reporte Oficial a Autoridades")
        form.geometry("500x600")
        form.configure(bg="white")

        tk.Label(form, text="📝 Reporte de Zona", font=("Helvetica", 16, "bold"), bg="white").pack(pady=10)

 
        tk.Label(form, text="Ciudad / Municipio:", bg="white").pack(anchor="w", padx=20)
        entry_ciudad = tk.Entry(form, width=40)
        entry_ciudad.pack(padx=20, pady=5)

        tk.Label(form, text="Barrio / Localidad:", bg="white").pack(anchor="w", padx=20)
        entry_barrio = tk.Entry(form, width=40)
        entry_barrio.pack(padx=20, pady=5)

        tk.Label(form, text="Ubicación Exacta (Parque/Río):", bg="white").pack(anchor="w", padx=20)
        entry_ubicacion = tk.Entry(form, width=40)
        entry_ubicacion.pack(padx=20, pady=5)


        tk.Label(form, text="Elementos Identificados por IA:", bg="white", font=("Helvetica", 10, "bold")).pack(anchor="w", padx=20, pady=(15,5))
        
        resumen_ia = "No hay datos"
        if self.ultima_deteccion_info:
            conteo = {x: self.ultima_deteccion_info.count(x) for x in self.ultima_deteccion_info}
            resumen_ia = "\n".join([f"- {k}: {v}" for k, v in conteo.items()])
        
        text_ia = tk.Text(form, height=8, width=50, bg="#f0f0f0")
        text_ia.insert("1.0", resumen_ia)
        text_ia.config(state="disabled") 
        text_ia.pack(padx=20)

        def guardar_reporte():
            ciudad = entry_ciudad.get()
            barrio = entry_barrio.get()
            ubicacion = entry_ubicacion.get()

            if not ciudad or not ubicacion:
                messagebox.showwarning("Faltan datos", "Por favor ingrese al menos Ciudad y Ubicación.")
                return

            # Crear estructura JSON
            datos_reporte = {
                "fecha_reporte": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "ubicacion": {
                    "ciudad": ciudad,
                    "barrio": barrio,
                    "lugar_especifico": ubicacion
                },
                "analisis_ia": {
                    "total_objetos": len(self.ultima_deteccion_info),
                    "detalle": self.ultima_deteccion_info
                },
                "estado_alerta": self.lbl_estado.cget("text")
            }

            # Guardar archivo
            nombre_archivo = f"reporte_ambiental_{datetime.now().strftime('%H%M%S')}.json"
            try:
                with open(nombre_archivo, 'w', encoding='utf-8') as f:
                    json.dump(datos_reporte, f, indent=4, ensure_ascii=False)
                
                messagebox.showinfo("Éxito", f"Reporte enviado correctamente.\nArchivo generado: {nombre_archivo}")
                form.destroy()
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo guardar el archivo: {e}")

        tk.Button(form, text="💾 ENVIAR A AUTORIDADES", bg="#2E7D32", fg="white", font=("Helvetica", 12, "bold"), command=guardar_reporte).pack(pady=20)

if __name__ == "__main__":
    root = tk.Tk()
    app = SmartCityApp(root)
    root.mainloop()