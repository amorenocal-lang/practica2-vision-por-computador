"""
Módulo para detección de características en imágenes.
Basado en los notebooks guía del curso de Visión por Computador.
"""

import cv2
import numpy as np


def detectar_caracteristicas(imagen, metodo='orb', max_features=500):
    """
    Detecta características (keypoints) y sus descriptores en una imagen.
    
    Args:
        imagen: imagen en escala de grises
        metodo: 'orb', 'sift', 'akaze'
        max_features: número máximo de características a detectar
    
    Returns:
        (keypoints, descriptores)
    """
    if metodo == 'orb':
        detector = cv2.ORB_create(max_features)
    elif metodo == 'sift':
        detector = cv2.SIFT_create(max_features)
    elif metodo == 'akaze':
        detector = cv2.AKAZE_create()
    else:
        raise ValueError(f"Método '{metodo}' no reconocido")
    
    keypoints, descriptores = detector.detectAndCompute(imagen, None)
    
    return keypoints, descriptores


def visualizar_keypoints(imagen, keypoints, titulo='Keypoints Detectados'):
    """
    Visualiza los keypoints detectados sobre la imagen.
    
    Args:
        imagen: imagen original
        keypoints: lista de keypoints detectados
        titulo: título de la figura
    
    Returns:
        imagen con keypoints dibujados
    """
    img_keypoints = cv2.drawKeypoints(
        imagen, keypoints, None, 
        color=(0, 255, 0), 
        flags=cv2.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS
    )
    
    return img_keypoints


def comparar_detectores(imagen, detectores=['orb', 'sift', 'akaze']):
    """
    Compara diferentes detectores de características en la misma imagen.
    
    Args:
        imagen: imagen en escala de grises
        detectores: lista de detectores a comparar
    
    Returns:
        diccionario con resultados para cada detector
    """
    resultados = {}
    
    for metodo in detectores:
        try:
            kp, des = detectar_caracteristicas(imagen, metodo)
            resultados[metodo] = {
                'keypoints': kp,
                'descriptores': des,
                'num_keypoints': len(kp) if kp else 0
            }
            print(f"✓ {metodo.upper()}: {len(kp) if kp else 0} características detectadas")
        except Exception as e:
            print(f"✗ {metodo.upper()}: Error - {str(e)}")
            resultados[metodo] = None
    
    return resultados
