
# redneuronal/probar_modelo.py
import tensorflow as tf
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import os
import matplotlib.pyplot as plt

# Configuración
MODEL_PATH = 'modelo_componentes.h5'
IMG_SIZE = (256, 256)
CLASSES = ['case', 'cpu', 'gpu', 'hdd', 'motherboard', 'ram']

# Cargar el modelo
print("🔄 Cargando modelo...")
model = load_model(MODEL_PATH)
print("✅ Modelo cargado exitosamente")

def probar_imagen(ruta_imagen):
    """Prueba el modelo con una imagen específica"""
    try:
        # Cargar y preprocesar imagen
        img = Image.open(ruta_imagen)
        
        # Mostrar información de la imagen
        print(f"📸 Imagen: {ruta_imagen}")
        print(f"📐 Tamaño original: {img.size}")
        print(f"🎨 Modo: {img.mode}")
        
        # Convertir a RGB si es necesario
        if img.mode != 'RGB':
            img = img.convert('RGB')
            print("🔄 Convertida a RGB")
        
        # Redimensionar
        img_resized = img.resize(IMG_SIZE)
        
        # Convertir a array y normalizar
        img_array = np.array(img_resized) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        
        # Realizar predicción
        print("🔮 Realizando predicción...")
        pred = model.predict(img_array, verbose=0)[0]
        
        # Obtener resultados
        idx = np.argmax(pred)
        clase_predicha = CLASSES[idx]
        confianza = pred[idx] * 100
        
        # Mostrar resultados
        print("\n" + "="*50)
        print("🎯 RESULTADOS DE LA PREDICCIÓN")
        print("="*50)
        print(f"🏷️  Clase predicha: {clase_predicha.upper()}")
        print(f"📊 Confianza: {confianza:.2f}%")
        
        # Mostrar todas las probabilidades
        print("\n📈 Probabilidades por clase:")
        for i, clase in enumerate(CLASSES):
            prob = pred[i] * 100
            bar = "█" * int(prob / 5)  # Barra visual
            print(f"   {clase:12} {prob:6.2f}% {bar}")
        
        # Verificar si la predicción es correcta (si sabemos la clase real)
        nombre_carpeta = os.path.basename(os.path.dirname(ruta_imagen))
        if nombre_carpeta in CLASSES:
            clase_real = nombre_carpeta
            es_correcto = (clase_predicha == clase_real)
            print(f"\n🔍 Clase real: {clase_real.upper()}")
            print(f"✅ PREDICCIÓN CORRECTA" if es_correcto else "❌ PREDICCIÓN INCORRECTA")
        
        return clase_predicha, confianza, pred
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None, None, None

def probar_varias_imagenes():
    """Prueba con varias imágenes del dataset"""
    print("🧪 Probando con imágenes del dataset...")
    
    # Buscar algunas imágenes de prueba en cada carpeta
    for clase in CLASSES:
        clase_path = os.path.join('data', 'pc_parts', clase)
        if os.path.exists(clase_path):
            # Tomar la primera imagen de cada clase
            imagenes = [f for f in os.listdir(clase_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            if imagenes:
                imagen_path = os.path.join(clase_path, imagenes[0])
                print(f"\n{'='*60}")
                print(f"🔍 Probando clase: {clase.upper()}")
                print(f"📁 Imagen: {imagenes[0]}")
                probar_imagen(imagen_path)

if __name__ == "__main__":
    print("🚀 INICIANDO PRUEBA DEL MODELO")
    print(f"📁 Modelo: {MODEL_PATH}")
    print(f"🎯 Clases: {CLASSES}")
    print(f"📐 Tamaño de imagen: {IMG_SIZE}")
    print()
    
    # Opción 1: Probar una imagen específica
    ruta_imagen = input("📁 Ingresa la ruta de una imagen (o presiona Enter para prueba automática): ").strip()
    
    if ruta_imagen and os.path.exists(ruta_imagen):
        probar_imagen(ruta_imagen)
    else:
        if not ruta_imagen:
            print("🔄 Realizando prueba automática con imágenes del dataset...")
        else:
            print(f"❌ No se encuentra: {ruta_imagen}")
            print("🔄 Realizando prueba automática con imágenes del dataset...")
        
        probar_varias_imagenes()
