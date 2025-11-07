"""
Módulo para registro de imágenes usando diferentes métodos.
Basado en los notebooks guía del curso de Visión por Computador.
"""

import cv2
import numpy as np
from feature_detection import detectar_caracteristicas
from matching import emparejar_caracteristicas, filtrar_matches_ransac


def registro_con_caracteristicas(img_fija, img_movil, metodo='orb', max_features=500):
    """
    Registra dos imágenes usando detección y emparejamiento de características.
    
    Args:
        img_fija: imagen de referencia
        img_movil: imagen a registrar
        metodo: 'orb', 'sift', 'akaze'
        max_features: número máximo de características
    
    Returns:
        (homografía, imagen_registrada, info)
    """
    # Detectar características
    kp1, des1 = detectar_caracteristicas(img_fija, metodo, max_features)
    kp2, des2 = detectar_caracteristicas(img_movil, metodo, max_features)
    
    if des1 is None or des2 is None:
        print("⚠️ No se detectaron suficientes características")
        return None, None, None
    
    print(f"✓ Características detectadas: {len(kp1)} en img1, {len(kp2)} en img2")
    
    # Emparejar características
    matches = emparejar_caracteristicas(des1, des2, metodo)
    print(f"✓ Matches encontrados: {len(matches)}")
    
    if len(matches) < 4:
        print("⚠️ Insuficientes matches para calcular homografía")
        return None, None, None
    
    # Filtrar con RANSAC
    H, mask = filtrar_matches_ransac(kp1, kp2, matches)
    
    if H is None:
        print("⚠️ No se pudo calcular la homografía")
        return None, None, None
    
    inliers = mask.ravel().tolist()
    print(f"✓ Inliers (RANSAC): {sum(inliers)}/{len(inliers)}")
    
    # Aplicar transformación
    h, w = img_fija.shape[:2]
    img_registrada = cv2.warpPerspective(img_movil, H, (w, h))
    
    info = {
        'keypoints1': kp1,
        'keypoints2': kp2,
        'matches': matches,
        'mask': mask,
        'num_inliers': sum(inliers)
    }
    
    return H, img_registrada, info


def registro_busqueda_exhaustiva(img_fija, img_movil, 
                                 rango_tx=(-20, 20), 
                                 rango_ty=(-20, 20),
                                 paso=1,
                                 metrica='mse'):
    """
    Registro por búsqueda exhaustiva de traslación.
    
    Args:
        img_fija: imagen de referencia
        img_movil: imagen a registrar
        rango_tx: rango de traslación en x
        rango_ty: rango de traslación en y
        paso: paso de búsqueda
        metrica: métrica de similitud ('mse', 'ncc')
    
    Returns:
        (matriz_transformacion, similitud, historial)
    """
    from utils import aplicar_transformacion, calcular_similitud
    
    mejor_similitud = float('inf') if metrica == 'mse' else float('-inf')
    mejor_tx, mejor_ty = 0, 0
    historia = []
    
    for tx in range(rango_tx[0], rango_tx[1] + 1, paso):
        for ty in range(rango_ty[0], rango_ty[1] + 1, paso):
            img_trans, _ = aplicar_transformacion(img_movil, 'traslacion', {'tx': tx, 'ty': ty})
            sim = calcular_similitud(img_fija, img_trans, metrica)
            historia.append((tx, ty, sim))
            
            if metrica == 'mse':
                if sim < mejor_similitud:
                    mejor_similitud = sim
                    mejor_tx, mejor_ty = tx, ty
            else:
                if sim > mejor_similitud:
                    mejor_similitud = sim
                    mejor_tx, mejor_ty = tx, ty
    
    M_optima = np.float32([[1, 0, mejor_tx], [0, 1, mejor_ty]])
    return M_optima, mejor_similitud, historia


def fusionar_imagenes(imagenes, homografias):
    """
    Fusiona múltiples imágenes usando las homografías calculadas.
    
    Args:
        imagenes: lista de imágenes a fusionar
        homografias: lista de homografías (desde cada imagen a la referencia)
    
    Returns:
        imagen fusionada
    """
    if len(imagenes) == 0:
        return None
    
    # Usar la primera imagen como referencia
    img_ref = imagenes[0]
    h, w = img_ref.shape[:2]
    
    # Calcular dimensiones del canvas final
    # Para simplicidad, usamos un canvas más grande
    canvas_h = h * 2
    canvas_w = w * 3
    offset_x = w // 2
    offset_y = h // 2
    
    # Crear canvas
    canvas = np.zeros((canvas_h, canvas_w), dtype=img_ref.dtype)
    
    # Colocar imagen de referencia en el centro
    canvas[offset_y:offset_y+h, offset_x:offset_x+w] = img_ref
    
    # Transformar y fusionar otras imágenes
    for i, (img, H) in enumerate(zip(imagenes[1:], homografias)):
        if H is not None:
            # Ajustar homografía para el offset
            H_offset = H.copy()
            H_offset[0, 2] += offset_x
            H_offset[1, 2] += offset_y
            
            # Transformar imagen
            img_warped = cv2.warpPerspective(img, H_offset, (canvas_w, canvas_h))
            
            # Fusionar (promedio simple donde ambas tienen contenido)
            mask = img_warped > 0
            canvas[mask] = (canvas[mask].astype(float) + img_warped[mask].astype(float)) / 2
    
    return canvas


def aplicar_blending(img1, img2, alpha=0.5):
    """
    Aplica blending simple entre dos imágenes.
    
    Args:
        img1: primera imagen
        img2: segunda imagen
        alpha: peso de la primera imagen (0-1)
    
    Returns:
        imagen blended
    """
    return cv2.addWeighted(img1, alpha, img2, 1-alpha, 0)
