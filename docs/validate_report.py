import os, re, sys
from html.parser import HTMLParser

REPORT_PATH = os.path.join(os.path.dirname(__file__), 'index.html')

class ImgParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.imgs = []
        self.ids = set()
        self.sections = []
    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == 'img':
            self.imgs.append(attrs)
        if 'id' in attrs and tag == 'section':
            self.sections.append(attrs['id'])

with open(REPORT_PATH, 'r', encoding='utf-8') as f:
    html = f.read()

parser = ImgParser()
parser.feed(html)

errors = []
# Check images
for img in parser.imgs:
    src = img.get('src','').strip()
    if not src:
        errors.append('Imagen con src vacío.')
    else:
        # If local path, confirm existence
        if not (src.startswith('http://') or src.startswith('https://')):
            local_path = os.path.join(os.path.dirname(REPORT_PATH), src)
            if not os.path.exists(local_path):
                errors.append(f'Imagen no encontrada: {src}')

# Required sections
required_sections = ['introduccion','marco-teorico','metodologia','experimentos','analisis','conclusiones','referencias','contribucion']
missing = [s for s in required_sections if s not in parser.sections]
if missing:
    errors.append('Faltan secciones: ' + ', '.join(missing))

# Mermaid presence
if 'mermaid' not in html:
    errors.append('No se encontró bloque mermaid (pipeline).')

print('Validación del reporte HTML')
print('Archivo:', REPORT_PATH)
if errors:
    print('\nRESULTADO: FALLA')
    for e in errors:
        print(' -', e)
    sys.exit(1)
else:
    print('\nRESULTADO: OK')
    print('Secciones presentes:', ', '.join(required_sections))
    print('Imágenes totales:', len(parser.imgs))
    print('Mermaid presente.')
