# Proyecto: Fusión de Perspectivas - Registro de Imágenes y Medición del Mundo Real

**Universidad Nacional de Colombia**  
**Curso:** Visión por Computador  
**Profesor:** Juan David Ospina Arango

---

## 📋 Descripción

Este proyecto implementa un pipeline completo de registro de imágenes para fusionar múltiples perspectivas de una escena (comedor) y realizar mediciones del mundo real usando objetos de referencia conocidos.

### Objetivos
1. **Validar** el sistema con imágenes sintéticas
2. **Registrar y fusionar** tres imágenes del comedor tomadas desde diferentes posiciones
3. **Calibrar** el sistema usando dimensiones conocidas de objetos de referencia
4. **Medir** elementos de la escena en unidades del mundo real (centímetros)

### Objetos de Referencia
- **Cuadro de la Virgen de Guadalupe:** Altura = 117 cm
- **Mesa:** Ancho = 161.1 cm

---

## 🗂️ Estructura del Proyecto

```

practica2-vision-por-computador/
├── README.md                    # Este archivo
├── requirements.txt             # Dependencias del proyecto
├── data/
│   ├── original/               # Imágenes originales del comedor
│   └── synthetic/              # Imágenes sintéticas para validación
├── src/
│   ├── feature_detection.py    # Detección de características (SIFT, ORB, AKAZE)
│   ├── matching.py             # Emparejamiento de características
│   ├── registration.py         # Registro y fusión de imágenes
│   ├── measurement.py          # Calibración y medición
│   └── utils.py                # Utilidades generales
├── notebooks/
│   ├── 02_synthetic_validation.ipynb      # Parte 1: Validación sintética
│   ├── 03_main_pipeline.ipynb             # Parte 2: Registro del comedor
│   └── 04_calibration_measurement.ipynb   # Parte 3: Calibración y medición
├── results/
│   ├── figures/                # Visualizaciones y gráficas
│   └── measurements/           # Resultados de mediciones
└── tests/                      # Pruebas unitarias (opcional)
```

---

## 🚀 Instalación y Configuración

### 1. Requisitos Previos
- Python 3.8 o superior
- pip (gestor de paquetes de Python)

### 2. Instalar Dependencias

```powershell
# Navegar al directorio del proyecto
cd practica2-vision-por-computador


# Instalar dependencias
pip install -r requirements.txt
```

### 3. Copiar Imágenes

Copie las imágenes del comedor a la carpeta `data/original/`:
- `cuadro_virgen_guadalupe.jpg`
- `IMG02.jpg`
- `IMG03.jpg`

---

## 📓 Uso del Proyecto

### Opción 1: Notebooks Jupyter (Recomendado)

Ejecute los notebooks en orden:

```powershell
jupyter notebook
```

1. **02_synthetic_validation.ipynb** - Validación con imágenes sintéticas (30%)
   - Crea imágenes sintéticas con transformaciones conocidas
   - Valida el pipeline de registro
   - Compara diferentes detectores (ORB, SIFT, AKAZE)
   - Analiza robustez al ruido

2. **03_main_pipeline.ipynb** - Registro de imágenes reales (40%)
   - Carga las tres imágenes del comedor
   - Detecta características con SIFT
   - Empareja características con ratio test
   - Estima homografías con RANSAC
   - Fusiona las imágenes en un panorama

3. **04_calibration_measurement.ipynb** - Calibración y medición (30%)
   - Calibra usando el cuadro (117 cm)
   - Valida con la mesa (161.1 cm)
   - Mide elementos adicionales
   - Herramienta interactiva de medición
   - Análisis de incertidumbre

### Opción 2: Uso Programático

```python
import sys
sys.path.append('src')

from feature_detection import detectar_caracteristicas
from matching import emparejar_caracteristicas, filtrar_matches_ransac
from registration import registro_con_caracteristicas
from measurement import CalibradorImagen

# Ejemplo de uso
import cv2

# Cargar imágenes
img1 = cv2.imread('data/original/IMG02.jpg', 0)
img2 = cv2.imread('data/original/cuadro_virgen_guadalupe.jpg', 0)

# Registrar
H, img_registrada, info = registro_con_caracteristicas(img1, img2, metodo='sift')

# Calibrar y medir
calibrador = CalibradorImagen(img_registrada)
calibrador.calibrar_con_referencia((x1, y1), (x2, y2), 117)  # Cuadro de 117 cm
distancia = calibrador.medir_distancia((x3, y3), (x4, y4))
```

---

## 🔬 Metodología

### Parte 1: Validación Sintética
- **Objetivo:** Verificar que el pipeline funciona correctamente
- **Métodos:** Imágenes sintéticas con transformaciones conocidas
- **Métricas:** RMSE, error angular, error de traslación

### Parte 2: Registro de Imágenes Reales
- **Detector:** SIFT (2000 características)
- **Matcher:** Brute Force + Ratio Test (0.75)
- **Estimación:** RANSAC con `findHomography`
- **Fusión:** Blending por promedio en zonas de overlap

### Parte 3: Calibración y Medición
- **Calibración:** Cuadro de la Virgen (altura 117 cm)
- **Validación:** Mesa (ancho 161.1 cm)
- **Mediciones:** Ventanas, sillas, plantas, etc.
- **Incertidumbre:** Análisis estadístico con mediciones repetidas

---

## 📊 Resultados Esperados

### Visualizaciones Generadas
- `imagenes_sinteticas.png` - Imágenes sintéticas de validación
- `comparacion_detectores.png` - Comparación ORB vs SIFT vs AKAZE
- `robustez_ruido.png` - Análisis de robustez
- `imagenes_originales.png` - Las tres imágenes del comedor
- `matches_img2_img1.png` - Matches entre imágenes 2 y 1
- `matches_img2_img3.png` - Matches entre imágenes 2 y 3
- `panorama_fusionado.jpg` - Panorama final del comedor
- `todas_mediciones.png` - Todas las mediciones visualizadas
- `incertidumbre.png` - Análisis de incertidumbre

### Archivos de Datos
- `mediciones.csv` - Mediciones en formato CSV
- `tabla_mediciones.html` - Tabla de mediciones en HTML

---

## 🛠️ Técnicas Implementadas

### Detección de Características
- **SIFT:** Scale-Invariant Feature Transform
- **ORB:** Oriented FAST and Rotated BRIEF
- **AKAZE:** Accelerated-KAZE

### Emparejamiento
- Ratio Test de Lowe (umbral 0.75)
- RANSAC para filtrado de outliers

### Transformaciones
- Homografías (transformación proyectiva)
- Matriz 3x3 con 8 grados de libertad

### Fusión
- Blending por promedio ponderado
- Recorte automático de bordes negros

---

## 📚 Referencias

1. Lowe, D.G. (2004). "Distinctive Image Features from Scale-Invariant Keypoints". *International Journal of Computer Vision*.

2. Rublee, E., et al. (2011). "ORB: An efficient alternative to SIFT or SURF". *IEEE International Conference on Computer Vision*.

3. Fischler, M.A. & Bolles, R.C. (1981). "Random Sample Consensus: A Paradigm for Model Fitting". *Communications of the ACM*.

4. Szeliski, R. (2010). "Computer Vision: Algorithms and Applications". Springer.

5. Hartley, R. & Zisserman, A. (2004). "Multiple View Geometry in Computer Vision". Cambridge University Press.

---

## 👥 Autores

- Andres Felipe Moreno Calle
- David Giraldo Valencia
- Juan Pablo Palacio Perez
- Victor Manuel Velasquez Cabeza

Universidad Nacional de Colombia  
Visión por Computador 2025-02

---

## 📝 Notas Importantes

### ⚠️ Ajuste de Coordenadas
Los notebooks incluyen coordenadas de ejemplo que **DEBEN SER AJUSTADAS** manualmente según las imágenes reales:
- Coordenadas del cuadro (parte superior e inferior)
- Coordenadas de la mesa (extremos izquierdo y derecho)
- Coordenadas de elementos adicionales a medir

### 🎯 Mejores Prácticas
1. Ejecutar los notebooks en orden
2. Verificar visualmente cada paso
3. Ajustar parámetros si es necesario (número de características, umbral RANSAC)
4. Guardar resultados intermedios

### 🐛 Solución de Problemas

**Problema:** No se detectan suficientes características
- **Solución:** Aumentar `max_features` a 3000-5000

**Problema:** Muchos outliers en los matches
- **Solución:** Ajustar `ratio_test` a 0.65-0.70

**Problema:** El panorama tiene costuras visibles
- **Solución:** Implementar blending más sofisticado (Laplacian blending)

**Problema:** Errores de calibración grandes
- **Solución:** Verificar que las coordenadas sean correctas y precisas

---

## 🎓 Licencia

Este proyecto es para fines educativos en el curso de Visión por Computador de la Universidad Nacional de Colombia.

---

## 🙏 Agradecimientos

- Profesor Juan David Ospina Arango
- Monitor Andrés Mauricio Zapata
- Recursos del curso de Visión por Computador
- Comunidad de OpenCV
