# redneuronal/entrenar_modelo.py
import tensorflow as tf 
from tensorflow.keras.models import Sequential 
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout 
from tensorflow.keras.preprocessing.image import ImageDataGenerator 
import os 
import numpy as np
import sys
import django

# Configurar Django (para poder usar modelos Django si es necesario)
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

def entrenar_y_guardar_modelo():
    # === Configuración con rutas relativas dentro de la app === 
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    TRAIN_DIR = os.path.join(BASE_DIR, 'data', 'pc_parts')
    MODEL_SAVE_PATH = os.path.join(BASE_DIR, 'modelo_componentes.h5')
    
    IMG_SIZE = (256, 256)
    BATCH_SIZE = 32
    EPOCHS = 10
    CLASSES = ['case', 'cpu', 'gpu', 'hdd', 'motherboard', 'ram']

    print(f"🔍 Buscando datos en: {TRAIN_DIR}")
    print(f"📁 Directorio actual: {BASE_DIR}")

    # Verificar que existe la carpeta de datos
    if not os.path.exists(TRAIN_DIR):
        print(f"❌ No se encuentra la carpeta: {TRAIN_DIR}")
        print("📂 Carpetas encontradas en el directorio actual:")
        for item in os.listdir(BASE_DIR):
            print(f"   - {item}")
        raise FileNotFoundError(f"❌ No se encuentra la carpeta de datos: {TRAIN_DIR}")

    # Verificar que las subcarpetas de clases existen
    print("📂 Verificando subcarpetas de clases...")
    for clase in CLASSES:
        clase_path = os.path.join(TRAIN_DIR, clase)
        if os.path.exists(clase_path):
            imagenes = [f for f in os.listdir(clase_path) if f.lower().endswith(('.jpg', '.jpeg', '.png'))]
            num_imagenes = len(imagenes)
            print(f"   ✅ {clase}: {num_imagenes} imágenes")
            if num_imagenes == 0:
                print(f"   ⚠️  La carpeta {clase} está vacía")
        else:
            print(f"   ❌ {clase}: NO ENCONTRADA")

    # === Preparar datos === 
    train_datagen = ImageDataGenerator( 
        rescale=1./255,
        validation_split=0.25
    )

    print("🔄 Creando generadores de datos...")
    train_generator = train_datagen.flow_from_directory( 
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='training'
    )

    validation_generator = train_datagen.flow_from_directory( 
        TRAIN_DIR,
        target_size=IMG_SIZE,
        batch_size=BATCH_SIZE,
        class_mode='categorical',
        subset='validation',
        shuffle=False
    )

    print(f"🎯 Clases detectadas: {list(train_generator.class_indices.keys())}")
    print(f"📊 Imágenes de entrenamiento: {train_generator.samples}")
    print(f"📊 Imágenes de validación: {validation_generator.samples}")

    # Verificar que hay suficientes imágenes
    if train_generator.samples == 0:
        raise ValueError("❌ No se encontraron imágenes para entrenamiento")

    # === Crear y entrenar modelo === 
    model = Sequential([ 
        Conv2D(32, (3,3), activation='relu', input_shape=(IMG_SIZE[0], IMG_SIZE[1], 3)),
        MaxPooling2D(2,2),
        Conv2D(64, (3,3), activation='relu'),
        MaxPooling2D(2,2),
        Flatten(),
        Dense(128, activation='relu'),
        Dense(len(CLASSES), activation='softmax')
    ])

    model.compile( 
        optimizer='adam',
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )

    print("🚀 Comenzando entrenamiento...")
    history = model.fit( 
        train_generator,
        validation_data=validation_generator,
        epochs=EPOCHS,
        verbose=1
    )

    # === Guardar modelo entrenado === 
    model.save(MODEL_SAVE_PATH)
    print(f"✅ Modelo entrenado y guardado como: {MODEL_SAVE_PATH}")
    
    # Mostrar métricas finales
    final_loss, final_accuracy = model.evaluate(validation_generator)
    print(f"📈 Precisión final en validación: {final_accuracy:.2%}")
    
    return model

if __name__ == "__main__":
    entrenar_y_guardar_modelo()