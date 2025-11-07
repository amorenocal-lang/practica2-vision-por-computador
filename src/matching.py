"""
Módulo para emparejamiento de características entre imágenes.
Basado en los notebooks guía del curso de Visión por Computador.
"""

import cv2
import numpy as np


def emparejar_caracteristicas(des1, des2, metodo='orb', ratio_test=0.75):
    """
    Empareja descriptores entre dos imágenes usando el ratio test de Lowe.
    
    Args:
        des1: descriptores de la primera imagen
        des2: descriptores de la segunda imagen
        metodo: 'orb', 'sift', 'akaze' (determina el tipo de distancia)
        ratio_test: umbral para el ratio test (típicamente 0.75)
    
    Returns:
        lista de buenos matches
    """
    if des1 is None or des2 is None:
        return []
    
    # Seleccionar matcher según el tipo de descriptor
    if metodo in ['orb', 'akaze']:
        matcher = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    else:
        matcher = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    
    # Emparejar usando KNN (k=2 para ratio test)
    matches = matcher.knnMatch(des1, des2, k=2)
    
    # Aplicar ratio test de Lowe
    buenos_matches = []
    for m_n in matches:
        if len(m_n) == 2:
            m, n = m_n
            if m.distance < ratio_test * n.distance:
                buenos_matches.append(m)
    
    return buenos_matches


def filtrar_matches_ransac(kp1, kp2, matches, reproj_thresh=5.0):
    """
    Filtra matches usando RANSAC para encontrar homografía.
    
    Args:
        kp1: keypoints de la primera imagen
        kp2: keypoints de la segunda imagen
        matches: lista de matches
        reproj_thresh: umbral de error de reproyección para RANSAC
    
    Returns:
        (homografía, mask de inliers)
    """
    if len(matches) < 4:
        return None, None
    
    # Extraer puntos correspondientes
    pts1 = np.float32([kp1[m.queryIdx].pt for m in matches])
    pts2 = np.float32([kp2[m.trainIdx].pt for m in matches])
    
    # Calcular homografía con RANSAC
    H, mask = cv2.findHomography(pts2, pts1, cv2.RANSAC, reproj_thresh)
    
    return H, mask


def visualizar_matches(img1, kp1, img2, kp2, matches, mask=None, titulo='Matches'):
    """
    Visualiza los matches entre dos imágenes.
    
    Args:
        img1: primera imagen
        kp1: keypoints de la primera imagen
        img2: segunda imagen
        kp2: keypoints de la segunda imagen
        matches: lista de matches
        mask: máscara de inliers (opcional)
        titulo: título de la visualización
    
    Returns:
        imagen con matches dibujados
    """
    if mask is not None:
        matchesMask = mask.ravel().tolist()
    else:
        matchesMask = None
    
    img_matches = cv2.drawMatches(
        img1, kp1, img2, kp2, matches, None,
        matchesMask=matchesMask,
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )
    
    return img_matches


def calcular_estadisticas_matches(matches, mask=None):
    """
    Calcula estadísticas sobre los matches.
    
    Args:
        matches: lista de matches
        mask: máscara de inliers (opcional)
    
    Returns:
        diccionario con estadísticas
    """
    num_matches = len(matches)
    
    if mask is not None:
        inliers = mask.ravel().tolist()
        num_inliers = sum(inliers)
        porcentaje_inliers = (num_inliers / num_matches * 100) if num_matches > 0 else 0
    else:
        num_inliers = num_matches
        porcentaje_inliers = 100.0
    
    # Calcular distancias de los matches
    distancias = [m.distance for m in matches]
    
    return {
        'num_matches': num_matches,
        'num_inliers': num_inliers,
        'porcentaje_inliers': porcentaje_inliers,
        'distancia_media': np.mean(distancias) if distancias else 0,
        'distancia_std': np.std(distancias) if distancias else 0
    }
