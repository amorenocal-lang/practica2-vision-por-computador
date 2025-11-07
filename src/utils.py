"""
Utilidades generales para el proyecto de registro de imágenes.
Basado en los notebooks guía del curso de Visión por Computador.
"""

import numpy as np
import cv2
import matplotlib.pyplot as plt


def crear_imagen_sintetica(size=256, tipo='patron'):
    """
    Crea imágenes sintéticas para validación.
    
    Args:
        size: tamaño de la imagen (size x size)
        tipo: 'patron', 'cuadros', 'circulo', 'texto'
    
    Returns:
        imagen en escala de grises
    """
    imagen = np.zeros((size, size), dtype=np.uint8)
    
    if tipo == 'patron':
        # Patrón de tablero de ajedrez
        square_size = size // 8
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    imagen[i*square_size:(i+1)*square_size, 
                          j*square_size:(j+1)*square_size] = 255
        
        cv2.circle(imagen, (size//2, size//2), size//6, 128, -1)
        cv2.rectangle(imagen, (size//4, size//4), (3*size//4, size//3), 200, 3)
        
    elif tipo == 'cuadros':
        cv2.rectangle(imagen, (20, 20), (100, 100), 255, -1)
        cv2.rectangle(imagen, (size-120, 40), (size-40, 120), 180, -1)
        cv2.rectangle(imagen, (size//2-30, size-80), (size//2+30, size-20), 220, -1)
        
    elif tipo == 'circulo':
        cv2.circle(imagen, (size//2, size//2), size//3, 255, -1)
        cv2.circle(imagen, (size//2, size//2), size//4, 0, -1)
        cv2.circle(imagen, (size//2, size//2), size//6, 200, -1)
        
    elif tipo == 'texto':
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(imagen, 'CV', (size//4, size//2), font, 3, 255, 5)
        cv2.circle(imagen, (3*size//4, size//4), 30, 255, -1)
        cv2.circle(imagen, (3*size//4, 3*size//4), 40, 200, -1)
    
    return imagen


def aplicar_transformacion(imagen, tipo, params):
    """
    Aplica una transformación geométrica a una imagen.
    
    Args:
        imagen: imagen de entrada
        tipo: 'traslacion', 'rotacion', 'rigida', 'afin'
        params: diccionario con parámetros de la transformación
    
    Returns:
        (imagen_transformada, matriz_transformacion)
    """
    h, w = imagen.shape[:2]
    center = (w / 2, h / 2)
    
    if tipo == 'traslacion':
        tx = params.get('tx', 0)
        ty = params.get('ty', 0)
        M = np.float32([[1, 0, tx], [0, 1, ty]])
        imagen_trans = cv2.warpAffine(imagen, M, (w, h))
        
    elif tipo == 'rotacion':
        angulo = params.get('angulo', 0)
        M = cv2.getRotationMatrix2D(center, angulo, 1.0)
        imagen_trans = cv2.warpAffine(imagen, M, (w, h))
        
    elif tipo == 'rigida':
        angulo = params.get('angulo', 0)
        tx = params.get('tx', 0)
        ty = params.get('ty', 0)
        M = cv2.getRotationMatrix2D(center, angulo, 1.0)
        M[0, 2] += tx
        M[1, 2] += ty
        imagen_trans = cv2.warpAffine(imagen, M, (w, h))
        
    elif tipo == 'afin':
        angulo = params.get('angulo', 0)
        escala = params.get('escala', 1.0)
        tx = params.get('tx', 0)
        ty = params.get('ty', 0)
        shear = params.get('shear', 0)
        
        M = cv2.getRotationMatrix2D(center, angulo, escala)
        M[0, 2] += tx
        M[1, 2] += ty
        M[0, 1] += shear
        imagen_trans = cv2.warpAffine(imagen, M, (w, h))
    
    else:
        raise ValueError(f"Tipo '{tipo}' no reconocido")
    
    return imagen_trans, M


def calcular_similitud(img1, img2, metrica='mse'):
    """
    Calcula una métrica de similitud entre dos imágenes.
    
    Args:
        img1: primera imagen
        img2: segunda imagen
        metrica: 'mse', 'ncc', 'mi'
    
    Returns:
        valor de similitud
    """
    if metrica == 'mse':
        mse = np.mean((img1.astype(float) - img2.astype(float)) ** 2)
        return mse
    
    elif metrica == 'ncc':
        img1_norm = (img1 - np.mean(img1)) / (np.std(img1) + 1e-8)
        img2_norm = (img2 - np.mean(img2)) / (np.std(img2) + 1e-8)
        ncc = np.mean(img1_norm * img2_norm)
        return ncc
    
    elif metrica == 'mi':
        hist_2d, _, _ = np.histogram2d(img1.ravel(), img2.ravel(), bins=20)
        pxy = hist_2d / float(np.sum(hist_2d))
        px = np.sum(pxy, axis=1)
        py = np.sum(pxy, axis=0)
        px_py = px[:, None] * py[None, :]
        nzs = pxy > 0
        mi = np.sum(pxy[nzs] * np.log(pxy[nzs] / px_py[nzs]))
        return mi
    
    else:
        raise ValueError(f"Métrica '{metrica}' no reconocida")


def visualizar_resultados(img_fija, img_movil, img_registrada, titulo='Registro de Imágenes'):
    """
    Visualiza el proceso de registro paso a paso.
    
    Args:
        img_fija: imagen de referencia
        img_movil: imagen a registrar (original)
        img_registrada: imagen después del registro
        titulo: título de la figura
    """
    fig, axes = plt.subplots(2, 3, figsize=(15, 10))
    
    # Primera fila: imágenes
    axes[0, 0].imshow(img_fija, cmap='gray')
    axes[0, 0].set_title('Imagen Fija', fontsize=12)
    axes[0, 0].axis('off')
    
    axes[0, 1].imshow(img_movil, cmap='gray')
    axes[0, 1].set_title('Imagen Móvil (Original)', fontsize=12)
    axes[0, 1].axis('off')
    
    axes[0, 2].imshow(img_registrada, cmap='gray')
    axes[0, 2].set_title('Imagen Registrada', fontsize=12)
    axes[0, 2].axis('off')
    
    # Segunda fila: superposiciones y diferencias
    superposicion_antes = np.zeros((*img_fija.shape, 3), dtype=np.uint8)
    superposicion_antes[:, :, 0] = img_fija
    superposicion_antes[:, :, 1] = img_movil
    axes[1, 0].imshow(superposicion_antes)
    axes[1, 0].set_title('Antes: Rojo=fija, Verde=móvil', fontsize=12)
    axes[1, 0].axis('off')
    
    superposicion_despues = np.zeros((*img_fija.shape, 3), dtype=np.uint8)
    superposicion_despues[:, :, 0] = img_fija
    superposicion_despues[:, :, 1] = img_registrada
    axes[1, 1].imshow(superposicion_despues)
    axes[1, 1].set_title('Después: Rojo=fija, Verde=registrada', fontsize=12)
    axes[1, 1].axis('off')
    
    diferencia = cv2.absdiff(img_fija, img_registrada)
    axes[1, 2].imshow(diferencia, cmap='hot')
    axes[1, 2].set_title('Diferencia Absoluta', fontsize=12)
    axes[1, 2].axis('off')
    
    plt.suptitle(titulo, fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.show()


def calcular_error_transformacion(M_real, M_estimada):
    """
    Calcula el error entre la transformación real y la estimada.
    
    Args:
        M_real: matriz de transformación real
        M_estimada: matriz de transformación estimada
    
    Returns:
        diccionario con métricas de error
    """
    # Error en traslación
    tx_error = abs(M_real[0, 2] - M_estimada[0, 2])
    ty_error = abs(M_real[1, 2] - M_estimada[1, 2])
    
    # RMSE de la matriz
    rmse = np.sqrt(np.mean((M_real - M_estimada) ** 2))
    
    return {
        'tx_error': tx_error,
        'ty_error': ty_error,
        'rmse': rmse
    }


def anadir_ruido_gaussiano(imagen, sigma=10):
    """
    Añade ruido gaussiano a una imagen.
    
    Args:
        imagen: imagen de entrada
        sigma: desviación estándar del ruido
    
    Returns:
        imagen con ruido
    """
    ruido = np.random.normal(0, sigma, imagen.shape)
    imagen_ruidosa = np.clip(imagen + ruido, 0, 255).astype(np.uint8)
    return imagen_ruidosa
