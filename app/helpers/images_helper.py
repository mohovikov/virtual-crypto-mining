import os
import hashlib
import shutil
from werkzeug.utils import secure_filename


def hashed_filename(file, user_id, file_type) -> str:
    ext = os.path.splitext(secure_filename(file.filename))[1].lower()

    raw_name = f"{user_id}_{file_type}"
    hash_name = hashlib.md5(raw_name.encode()).hexdigest()
    return f"{hash_name}{ext}"

def save_user_file(file, user_id: str, file_type: str, folder: str) -> str:
    """
    Сохраняет файл с фиксированным хэш-именем.
    :param file: объект file (например, request.files['avatar'])
    :param user_id: ID пользователя
    :param file_type: тип файла (например 'avatar' или 'background')
    :return: новое имя файла (для записи в БД)
    """

    filename = hashed_filename(file, user_id, file_type)

    if os.path.exists(folder):
        shutil.rmtree(folder)

    os.makedirs(folder, exist_ok=True)

    file.stream.seek(0)

    filepath = os.path.join(folder, filename)

    file.save(filepath)

    return filename