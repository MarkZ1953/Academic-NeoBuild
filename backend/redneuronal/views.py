# redneuronal/views.py
import tensorflow as tf
from tensorflow.keras.models import load_model
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import numpy as np
import json
from PIL import Image
import io
import base64
import os
import logging

logger = logging.getLogger(__name__)

# Configuración del modelo
MODEL_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'modelo_componentes.h5')
CLASSES = ['case', 'cpu', 'gpu', 'hdd', 'motherboard', 'ram']
IMG_SIZE = (256, 256)

# Cargar el modelo
try:
    if os.path.exists(MODEL_PATH):
        MODEL = load_model(MODEL_PATH)
        logger.info("✅ Modelo cargado exitosamente")
    else:
        MODEL = None
        logger.warning("⚠️ No se encontró el modelo entrenado")
except Exception as e:
    MODEL = None
    logger.error(f"❌ Error cargando el modelo: {str(e)}")

DETALLES = {
    'cpu': "es el cerebro principal de la computadora",
    'gpu': "se encarga del procesamiento gráfico", 
    'ram': "almacena datos temporales para acelerar el acceso",
    'motherboard': "conecta y permite la comunicación entre componentes",
    'hdd': "almacena datos de forma permanente",
    'case': "protege y organiza todos los componentes"
}

def preprocesar_imagen(image):
    """Preprocesa la imagen para la predicción"""
    # Convertir a RGB si es necesario
    if image.mode != 'RGB':
        image = image.convert('RGB')
        logger.info("🔄 Imagen convertida a RGB")
    
    # Redimensionar
    image = image.resize(IMG_SIZE)
    
    # Convertir a array y normalizar
    img_array = np.array(image) / 255.0
    
    # Expandir dimensiones para el batch
    img_array = np.expand_dims(img_array, axis=0)
    
    return img_array

@csrf_exempt
def predecir_componente(request):
    """
    Endpoint principal para predicciones desde el frontend
    Recibe la imagen directamente (FormData o Base64)
    """
    if MODEL is None:
        return JsonResponse({
            'error': 'Modelo no disponible. Ejecute el entrenamiento primero.',
            'status': 'error'
        }, status=503)
    
    if request.method == 'POST':
        try:
            image = None
            fuente_imagen = "desconocida"
            
            # Manejar imagen desde FormData (archivo)
            if 'imagen' in request.FILES:
                image_file = request.FILES['imagen']
                image = Image.open(image_file)
                fuente_imagen = f"archivo: {image_file.name}"
                logger.info(f"📸 Imagen recibida via FormData: {image_file.name}")
                logger.info(f"📏 Tamaño de archivo: {image_file.size} bytes")
            
            # Manejar imagen desde JSON (base64)
            elif request.content_type == 'application/json':
                data = json.loads(request.body)
                
                if 'imagen' in data and data['imagen']:
                    image_data = data['imagen']
                    
                    # Remover el prefijo data:image/...;base64, si está presente
                    if 'base64,' in image_data:
                        image_data = image_data.split('base64,')[1]
                    
                    image_bytes = base64.b64decode(image_data)
                    image = Image.open(io.BytesIO(image_bytes))
                    fuente_imagen = "base64"
                    logger.info("📸 Imagen recibida via Base64")
                
                else:
                    return JsonResponse({
                        'error': 'Se requiere el campo "imagen" en el JSON',
                        'status': 'error'
                    }, status=400)
            
            else:
                return JsonResponse({
                    'error': 'Content-Type no soportado. Use application/json o multipart/form-data',
                    'status': 'error'
                }, status=400)
            
            # Verificar que tenemos una imagen válida
            if image is None:
                return JsonResponse({
                    'error': 'No se pudo procesar la imagen',
                    'status': 'error'
                }, status=400)
            
            # Información de la imagen recibida
            logger.info(f"📐 Dimensiones imagen original: {image.size}")
            logger.info(f"🎨 Modo de color: {image.mode}")
            
            # Preprocesar imagen
            img_array = preprocesar_imagen(image)
            
            # Realizar predicción
            logger.info("🔮 Realizando predicción...")
            pred = MODEL.predict(img_array, verbose=0)[0]
            idx = np.argmax(pred)
            clase = CLASSES[idx]
            confianza = float(pred[idx] * 100)
            
            # Obtener top 3 predicciones
            top3_indices = np.argsort(pred)[-3:][::-1]
            top3_predicciones = {
                CLASSES[i]: round(float(pred[i] * 100), 2)
                for i in top3_indices
            }
            
            # Calcular confianza de la predicción
            if confianza > 80:
                nivel_confianza = "alta"
            elif confianza > 60:
                nivel_confianza = "media"
            else:
                nivel_confianza = "baja"
            
            # Preparar respuesta
            respuesta = {
                'clase_predicha': clase,
                'confianza': round(confianza, 2),
                'nivel_confianza': nivel_confianza,
                'descripcion': DETALLES.get(clase, ""),
                'top_3_predicciones': top3_predicciones,
                'todas_las_clases': {
                    cls: round(float(prob * 100), 2) 
                    for cls, prob in zip(CLASSES, pred)
                },
                'fuente_imagen': fuente_imagen,
                'dimensiones_originales': f"{image.size[0]}x{image.size[1]}",
                'status': 'success'
            }
            
            logger.info(f"🎯 Predicción exitosa: {clase} ({confianza:.2f}%) - Confianza: {nivel_confianza}")
            
            return JsonResponse(respuesta)
            
        except Exception as e:
            logger.error(f"❌ Error en predicción: {str(e)}")
            return JsonResponse({
                'error': f'Error procesando la imagen: {str(e)}',
                'status': 'error'
            }, status=400)
    
    return JsonResponse({'error': 'Método no permitido'}, status=405)

def health_check(request):
    """Endpoint para verificar que el modelo está cargado"""
    status_info = {
        'status': 'healthy' if MODEL is not None else 'model_not_loaded',
        'modelo_cargado': MODEL is not None,
        'clases': CLASSES if MODEL is not None else [],
        'tamaño_entrada': f"{IMG_SIZE[0]}x{IMG_SIZE[1]}",
        'formato_entrada': 'RGB',
        'endpoints_disponibles': [
            'POST /api/redneuronal/prediccion/ (FormData o Base64)'
        ]
    }
    
    return JsonResponse(status_info)

def info_modelo(request):
    """Endpoint para obtener información del modelo"""
    if MODEL is None:
        return JsonResponse({'error': 'Modelo no cargado'}, status=503)
    
    info = {
        'clases': CLASSES,
        'input_shape': MODEL.input_shape,
        'output_shape': MODEL.output_shape,
        'numero_parametros': MODEL.count_params(),
        'descripciones': DETALLES,
        'tamaño_imagen_entrada': IMG_SIZE,
        'formato_imagen': 'RGB'
    }
    
    return JsonResponse(info)