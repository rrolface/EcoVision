🌱EcoVision  
Sistema de Visión por Computador para la Detección, Clasificación y Segmentación de Residuos

EcoVision es un proyecto que permite identificar diferentes tipos de residuos presentes en imágenes capturadas en calles, parques y espacios urbanos.  
El sistema integra un modelo entrenado en Google Colab y una aplicación de escritorio desarrollada en Python/Tkinter para que cualquier persona pueda cargar imágenes y obtener resultados de detección de forma intuitiva.


# 🟦Guía de usuario

## 🖥️Interfaz principal

Al ejecutar la aplicación verás:

- **Botón “Cargar imagen”** → Permite seleccionar una imagen desde el PC.  
- **Botón “Detectar residuos”** → Ejecuta el modelo sobre la imagen cargada.  
- **Área de visualización** → Muestra imagen original y procesada.  
- **Panel de resultados** → Indica clase detectada, segmentación y nivel de alerta sanitaria para crear campaña anti residuos.

## 🧪Cómo analizar una imagen

1. Clic en **Cargar imagen**.  
2. Selecciona un archivo `.jpg` o `.png`.  
3. Clic en **Detectar residuos**.  
4. La imagen será analizada por el modelo.  
5. La ventana mostrará:  
   - El residuo detectado  
   - La clase predicha  



# 🟧Instalación y ejecución

## 📌 Prerrequisitos

- Python 3.8+
- pip actualizado
- Windows / Linux
  
## 🟦Autores

Santiago Osorio
Kevin Aristizabal
Julian Montoya

##🟦Enlace a DataSet utilizado
https://universe.roboflow.com/taco-t7kkz/taco-dataset-ql1ng

## 📥Clonar el repositorio
```bash
git clone https://github.com/tu_usuario/EcoVision.git








