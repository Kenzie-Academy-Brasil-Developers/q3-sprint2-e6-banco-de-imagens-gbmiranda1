# Desenvolva suas rotas aqui
from asyncio import exceptions
from re import T
from flask import Flask, jsonify, request, send_file, safe_join
import os
import zipfile
from app.kenzie.image import getFiles, getFilesExtension, getFileDownload, upload_video


app = Flask(__name__)
maxLenght = os.getenv("MAX_CONTENT_LENGTH")


file = os.getenv("FILES_DIRECTORY")
extensions = os.getenv("ALLOWED_EXTENSIONS")
direc = os.listdir(file)

@app.get("/files")
def getFilesRoute():
    return jsonify({"files": getFiles()}), 200

@app.get("/files/<extension>")
def getFilesExtenstionRoute(extension):
    if extension in extensions.split(","):
        if(len(getFilesExtension(extension)) > 0 ):
            return jsonify({"files": getFilesExtension(extension)}), 200
        return {"message": "No files found in this extension."}, 404
    return {"message": "We don't recognize this extension"}, 404

@app.get("/download/<arquivo>")
def getDownloadFile(arquivo):
    return getFileDownload(arquivo)


@app.get("/download-zip")
def getDownloadZip():
    try:
        extension = request.args["files_extension"]
        compression = request.args["compression_ratio"]
        inputfile = os.path.join(file, extension)
        pathOutput = os.path.join("/tmp", f"{extension}.zip")

        if extension in extensions.split(","):
            if os.path.isfile(pathOutput):
                os.remove(pathOutput)
            if os.listdir(inputfile) == []:
                return {"message": "empty"}, 404
            os.system(f"zip -r -j -{compression} {pathOutput} {inputfile}")
            send_file(pathOutput, as_attachment=True)
            return jsonify({"message": f"zip generated here is your file path {pathOutput}"})
        return {"message": "we don't recognize this extension"}, 404
    except KeyError:
        return {"message": "add query params"}, 404

@app.post("/upload")
def postFile():
    files = request.files
    for filesIN in files.values():
        try:
            return upload_video(filesIN)
        except FileExistsError:
            return {"msg": "File already exists"}, 409
        except FileNotFoundError:
            return {'msg': "We only accept jpg, png and gif extension"}, 415
        except Exception:
            return {'msg': "Very large file"}, 413