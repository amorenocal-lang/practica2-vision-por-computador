"""
Módulo para calibración y medición en imágenes registradas.
Basado en los notebooks guía del curso de Visión por Computador.
"""

import cv2
import numpy as np
import matplotlib.pyplot as plt


class CalibradorImagen:
    """
    Clase para calibrar imágenes y realizar mediciones.
    """
    
    def __init__(self, imagen):
        """
        Inicializa el calibrador con una imagen.
        
        Args:
            imagen: imagen calibrada (puede ser en color o escala de grises)
        """
        self.imagen = imagen
        self.escala_pixel_a_cm = None
        self.referencias = []
    
    def calibrar_con_referencia(self, punto1, punto2, distancia_real_cm):
        """
        Calibra la escala usando una distancia de referencia conocida.
        
        Args:
            punto1: (x, y) primer punto de referencia
            punto2: (x, y) segundo punto de referencia
            distancia_real_cm: distancia real en cm entre los puntos
        """
        # Calcular distancia en píxeles
        distancia_pixeles = np.sqrt(
            (punto2[0] - punto1[0])**2 + 
            (punto2[1] - punto1[1])**2
        )
        
        # Calcular escala
        self.escala_pixel_a_cm = distancia_real_cm / distancia_pixeles
        
        # Guardar referencia
        self.referencias.append({
            'punto1': punto1,
            'punto2': punto2,
            'distancia_real_cm': distancia_real_cm,
            'distancia_pixeles': distancia_pixeles
        })
        
        print(f"✓ Calibración exitosa:")
        print(f"  Distancia en píxeles: {distancia_pixeles:.2f} px")
        print(f"  Distancia real: {distancia_real_cm} cm")
        print(f"  Escala: {self.escala_pixel_a_cm:.4f} cm/px")
    
    def medir_distancia(self, punto1, punto2):
        """
        Mide la distancia entre dos puntos en centímetros.
        
        Args:
            punto1: (x, y) primer punto
            punto2: (x, y) segundo punto
        
        Returns:
            distancia en centímetros
        """
        if self.escala_pixel_a_cm is None:
            raise ValueError("Debe calibrar primero usando calibrar_con_referencia()")
        
        # Calcular distancia en píxeles
        distancia_pixeles = np.sqrt(
            (punto2[0] - punto1[0])**2 + 
            (punto2[1] - punto1[1])**2
        )
        
        # Convertir a centímetros
        distancia_cm = distancia_pixeles * self.escala_pixel_a_cm
        
        return distancia_cm
    
    def visualizar_medicion(self, punto1, punto2, label=""):
        """
        Visualiza una medición en la imagen.
        
        Args:
            punto1: (x, y) primer punto
            punto2: (x, y) segundo punto
            label: etiqueta para la medición
        
        Returns:
            imagen con la medición dibujada
        """
        img_vis = self.imagen.copy()
        if len(img_vis.shape) == 2:
            img_vis = cv2.cvtColor(img_vis, cv2.COLOR_GRAY2BGR)
        
        # Dibujar línea
        cv2.line(img_vis, punto1, punto2, (0, 255, 0), 2)
        
        # Dibujar puntos
        cv2.circle(img_vis, punto1, 5, (255, 0, 0), -1)
        cv2.circle(img_vis, punto2, 5, (255, 0, 0), -1)
        
        # Calcular distancia
        distancia_cm = self.medir_distancia(punto1, punto2)
        
        # Dibujar texto
        punto_medio = (
            (punto1[0] + punto2[0]) // 2,
            (punto1[1] + punto2[1]) // 2
        )
        texto = f"{label}: {distancia_cm:.1f} cm"
        cv2.putText(img_vis, texto, punto_medio, 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
        
        return img_vis


class HerramientaMedicionInteractiva:
    """
    Herramienta interactiva para medir distancias en una imagen.
    """
    
    def __init__(self, imagen, escala_pixel_a_cm):
        """
        Inicializa la herramienta de medición.
        
        Args:
            imagen: imagen sobre la que medir
            escala_pixel_a_cm: escala de conversión pixel a cm
        """
        self.imagen = imagen.copy()
        if len(self.imagen.shape) == 2:
            self.imagen = cv2.cvtColor(self.imagen, cv2.COLOR_GRAY2BGR)
        
        self.escala = escala_pixel_a_cm
        self.puntos = []
        self.mediciones = []
    
    def onclick(self, event):
        """
        Manejador de clicks del mouse.
        """
        if event.xdata is not None and event.ydata is not None:
            x, y = int(event.xdata), int(event.ydata)
            self.puntos.append((x, y))
            
            # Dibujar punto
            plt.plot(x, y, 'ro', markersize=8)
            
            # Si tenemos dos puntos, calcular distancia
            if len(self.puntos) == 2:
                p1, p2 = self.puntos
                
                # Calcular distancia
                dist_px = np.sqrt((p2[0]-p1[0])**2 + (p2[1]-p1[1])**2)
                dist_cm = dist_px * self.escala
                
                # Dibujar línea
                plt.plot([p1[0], p2[0]], [p1[1], p2[1]], 'g-', linewidth=2)
                
                # Añadir texto
                punto_medio = ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)
                plt.text(punto_medio[0], punto_medio[1], 
                        f'{dist_cm:.1f} cm',
                        color='red', fontsize=12, fontweight='bold',
                        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
                
                self.mediciones.append({
                    'punto1': p1,
                    'punto2': p2,
                    'distancia_cm': dist_cm
                })
                
                print(f"✓ Medición: {dist_cm:.1f} cm")
                
                # Reiniciar puntos
                self.puntos = []
            
            plt.draw()
    
    def iniciar(self):
        """
        Inicia la interfaz interactiva de medición.
        """
        fig, ax = plt.subplots(figsize=(12, 8))
        ax.imshow(cv2.cvtColor(self.imagen, cv2.COLOR_BGR2RGB))
        ax.set_title('Click en dos puntos para medir distancia\n(Cierre la ventana cuando termine)', 
                    fontsize=12, fontweight='bold')
        ax.axis('off')
        
        # Conectar evento de click
        fig.canvas.mpl_connect('button_press_event', self.onclick)
        
        plt.tight_layout()
        plt.show()
        
        return self.mediciones


def estimar_incertidumbre(mediciones_repetidas):
    """
    Estima la incertidumbre en las mediciones.
    
    Args:
        mediciones_repetidas: lista de mediciones del mismo objeto
    
    Returns:
        diccionario con estadísticas de incertidumbre
    """
    mediciones = np.array(mediciones_repetidas)
    
    return {
        'media': np.mean(mediciones),
        'std': np.std(mediciones),
        'error_relativo': (np.std(mediciones) / np.mean(mediciones)) * 100,
        'min': np.min(mediciones),
        'max': np.max(mediciones)
    }
