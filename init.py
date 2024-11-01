import subprocess
import sys

# Lista de bibliotecas que você quer instalar
libraries = [
    'tkcalendar',
    'reportlab',
    'customtkinter',
    'requests',
    'cryptography',
    'python-barcode',
    'pyinstaller',
    'cairosvg',
    'pyautogui',
    'keyboard'
]

# Função para instalar uma biblioteca
def install(package):
    subprocess.check_call([sys.executable, "-m", "pip", "install", package])

# Instalar todas as bibliotecas da lista
for library in libraries:
    install(library)