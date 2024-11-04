from tkinter import messagebox
import requests
import zipfile
import os
from io import BytesIO
from databaseConnection import DataBase

def obter_ultima_release():
    url = f"https://api.github.com/repos/KAHISS/LM_PRO/releases/latest"
    response = requests.get(url)
    if response.status_code == 200:
        dados = response.json()
        ultima_versao = dados["tag_name"]
        url_download = None
        # Procura apenas ativos que terminam em .zip
        for asset in dados["assets"]:
            if asset["name"].endswith(".zip"):
                url_download = asset["browser_download_url"]
                break
        return ultima_versao, url_download
    else:
        messagebox.showerror(title="Erro", message="Erro ao verificar a última release.")
        return None, None

def baixar_e_extrair_zip(url_download, destino):
    response = requests.get(url_download)
    if response.status_code == 200:
        with zipfile.ZipFile(BytesIO(response.content)) as zip_file:
            zip_file.extractall(destino)
        messagebox.showinfo(title="Atualização", message="Atualização baixada e extraída com sucesso!")

    else:
        messagebox.showerror(title="Erro", message="Erro ao baixar o arquivo .zip.")

def atualizar_sistema():
    VERSAO_LOCAL = DataBase('resources/backup.db').searchDatabase('SELECT * FROM system')[0][0]
    ultima_versao, url_arquivo_zip = obter_ultima_release()
    if ultima_versao and url_arquivo_zip:
        if ultima_versao > VERSAO_LOCAL:  # Verifica se a versão remota é mais recente
            messagebox.showinfo(title="Atualização", message=f"Nova versão disponível: {ultima_versao}. Atualizando...")
            if not os.path.exists(os.getcwd()):
                os.makedirs(os.getcwd())
            baixar_e_extrair_zip(url_arquivo_zip, os.getcwd())
            # Atualiza a versão local (aqui você pode salvar a nova versão em um arquivo
            DataBase('resources/backup.db').crud(f'UPDATE system SET version = "{ultima_versao}"')
        else:
            messagebox.showinfo(title="Atualização", message="O sistema já está na versão mais recente.")
    else:
        messagebox.showwarning(title="Atualização", message="Nenhuma atualização disponível.")


# Executa o processo de atualização
atualizar_sistema()
