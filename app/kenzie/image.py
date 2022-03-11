from posixpath import abspath
from flask import jsonify,send_file, safe_join
import os
from pathlib import Path 

if(not os.path.isdir("img")):
        os.system(f"mkdir img")
        
files_direc = os.getenv("FILES_DIRECTORY")
direc = os.listdir(files_direc)
extensions = os.getenv("ALLOWED_EXTENSIONS") 

def getFiles():
    files = []
    for f in direc:
        if os.listdir(f"img/{f}") != []:
            files.append(os.listdir(f"img/{f}"))
    return files

def getFilesExtension(ext):
    files = []
    for f in direc:
        if f.split(".")[-1] == ext:
            files.append(os.listdir(f"img/{f}"))
    return files

def getFileDownload(arquivo):
    
    for dire in direc:
        path = os.listdir(f"img/{dire}")
        abspath = os.path.abspath(files_direc)
        for files in path:
            if files == arquivo:
                return send_file(safe_join(f"{abspath}/{dire}/{arquivo}"), as_attachment=True), 200
    return {"message": "No files found"}, 404

def upload_video(file):
    extension = file.filename.split(".")[-1]
    if not(extension in direc) and extension in extensions.split(","):
        os.system(f"mkdir img/{extension}")

    filepath = get_file_path(f"{extension}/{file.filename}")

    if fileExists(file.filename, extension):
        raise FileExistsError
    if not (extensionSuport(extension)):
        raise FileNotFoundError
    
    file.save(filepath)
    if Path(filepath).stat().st_size > 1048576:
        os.system(f"rm img/{extension}/{file.filename}")
        raise Exception
    return {"msg": "videos uploaded"}, 201



def get_file_path(filename: str):
    abs_path = os.path.abspath(files_direc)
    filepath = safe_join(abs_path, filename)

    return filepath

def fileExists(filename, extension):
    return filename in os.listdir(os.path.join(files_direc, extension))

def extensionSuport(extension):
    return extension in extensions.split(",")
