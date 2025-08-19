import os
import hashlib
from flask import current_app
from werkzeug.utils import secure_filename


def pre_generate_hashed_file(id: int, file, file_type: str, folder: str) -> tuple[str, str]:
    filename = secure_filename(file.filename)
    ext = os.path.splitext(filename)[1]

    hash_input = f"{id}_{file_type}".encode("utf-8")
    file_hash = hashlib.md5(hash_input).hexdigest()
    new_filename = f"{file_hash}{ext}"

    folder = os.path.join(folder, file_type, str(id))
    os.makedirs(folder, exist_ok=True)

    return new_filename, os.path.join(folder, new_filename)

def save_user_hashed_file(user_id: int, file_storage, file_type: str) -> str | None:
    """
    Сохраняет файл клана в нужную папку и возвращает новое имя файла.
    file_type: 'logo' или 'header'
    """
    if not file_storage:
        return None

    try:
        filename, path = pre_generate_hashed_file(user_id, file_storage, file_type, current_app.config["USER_FOLDER"])
        file_storage.stream.seek(0)
        file_storage.save(path)

        return filename
    except Exception as ex:
        raise ex

def save_clan_hashed_file(clan_id: int, file_storage, file_type: str) -> str | None:
    """
    Сохраняет файл клана в нужную папку и возвращает новое имя файла.
    file_type: 'logo' или 'header'
    """
    if not file_storage:
        return None

    try:
        filename, path = pre_generate_hashed_file(clan_id, file_storage, file_type, current_app.config["CLAN_FOLDER"])
        file_storage.stream.seek(0)
        file_storage.save(path)

        return filename
    except Exception as ex:
        raise ex