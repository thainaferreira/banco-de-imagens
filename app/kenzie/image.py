from flask import request, safe_join, jsonify, send_from_directory, Response
from environs import Env
import os
from werkzeug.utils import secure_filename
import ipdb
from time import sleep

env = Env()
env.read_env()

valid_extention = ('png', 'jpg', 'gif')
file_path = env('FILES_DIRECTORY')

max_length = env('MAX_CONTENT_LENGTH')
max_length = int(max_length.split('M')[0]) * 1024 * 1024 



def verify_exists(file: str) -> bool:
    """
    Função que faz a verificação da existencia de um arquivo

    Args:
        file (str): nome do arquivo que deseja verificar

    Returns:
        bool: retorna True caso o arquivo exista e False caso o contrario
    """
    files_list = []

    for _, _, filenames in os.walk(file_path):
        for files in filenames:
            files_list.append(files)

    if file in files_list:
        return True
    
    return False


def post_file() -> dict:
    """
    Recebe um arquivo de um formulario HTML e se atender à todas as condições é salvo em uma pasta do seu determinado tipo

    Returns:
        dict: retorna se o upload do arquivo foi feito com sucesso
    """
    file = request.files['file']

    if len(request.files) == 0:
        return {'message': 'Envie um arquivo'}, 406

    file_name = secure_filename(file.filename)
    file_extention = file_name.split('.')[-1]

    if verify_exists(file_name):
        return {'message': 'Arquivo já existente'}, 409

    if not file_extention in valid_extention:
        return {'message': f'{file_name} não contém uma extensão valida'}, 415

    path = safe_join(file_path, file_extention, file_name)
    
    file.save(path)

    return {'message': f'Upload do arquivo {file_name} realizado com sucesso!'}, 201


def all_files() -> dict:
    """
    Percorre todas as pastas e salva os nomes dos arquivos em uma lista.

    Returns:
        dict: retorna o nome de todos os arquivos.
    """
    files_list = []

    for _, _, filenames in os.walk(file_path):
        for file in filenames:
            files_list.append(file)
    
    return jsonify({'files_name': files_list}), 200


def types_files(type: str) -> dict:
    """
    Mostras os arquivos existentes do mesmo tipo

    Args:
        type (str): nome do tipo de arquivo que deseja fazer a busca, pode ser 'gif', 'jpg' ou 'png'.

    Returns:
        dict: retorna o nome dos arquivos daquele tipo
    """
    path = safe_join(file_path, type)
    files_type = os.listdir(path)
    
    return jsonify({'files': files_type}), 200


def download_file(file: str) -> Response:
    """
    Busca através do nome do arquivo recebido a pasta com o tipo e retorna o donwload deste arquivo.

    Args:
        file (str): nome do arquivo que deseja baixar

    Returns:
        Response: retorna o objeto do tipo Response com os status da requisição
    """
    extention = file.split('.')[-1]
    path = safe_join(file_path, extention)

    print(send_from_directory(directory=path, path=file, as_attachment=True))

    return send_from_directory(directory=path, path=file, as_attachment=True), 200


def download_zip() -> Response:
    """
    Faz o download de um zip do tipo de arquivo e a taxa de compressão escolhidos pelo usuário através do query params.

    Returns:
        Response: retorna o objeto do tipo Response com os status da requisição
    """
    file_type = request.args.get('file_type')
    compression_rate = request.args.get('compression_rate', 6)

    path = safe_join(file_path, file_type)
    
    os.system(f'cd {path} && zip -{str(compression_rate)} /tmp/files_{file_type}.zip *')

    return send_from_directory(directory='/tmp', path=f'files_{file_type}.zip', as_attachment=True), 200
