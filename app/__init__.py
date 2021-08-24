from flask import Flask
from werkzeug.exceptions import NotFound, BadRequestKeyError
from .kenzie.image import post_file, all_files, types_files, download_file, download_zip

app = Flask(__name__)

@app.post('/upload')
def post_form():
    try:
        return post_file()
    except BadRequestKeyError:
        return {'message': 'Nome do arquivo enviado deve ser "file"'}, 400

@app.get('/files')
def get_files():
    return all_files()

@app.get('/files/<string:type>')
def get_types_files(type):
    try:
        return types_files(type)
    except FileNotFoundError:
        return {'message': 'Tipo não encontrado'}, 404

@app.get('/download/<string:file_name>')
def get_download(file_name):
    try:
        return download_file(file_name)
    except NotFound:
        return {'message': 'Arquivo não encontrado'}, 404

@app.get('/download-zip')
def download_zip_file():
    try:
        return download_zip()
    except TypeError:
        return {'message': 'Deve ser passado por query params o "file_type" (JPG/PNG/GIF) e "compression_rate" (de 1 à 9)'}, 406
    except NotFound:
        return {'message': 'Tipo inválido, tente JPG, PNG ou GIF'}, 404