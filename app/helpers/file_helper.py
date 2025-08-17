import os
import hashlib
from flask import current_app
from werkzeug.utils import secure_filename


def save_clan_hashed_file(clan_id: int, file_storage, file_type: str) -> str | None:
    """
    Сохраняет файл клана в нужную папку и возвращает новое имя файла.
    file_type: 'logo' или 'header'
    """
    if not file_storage:
        return None

    try:
        # Берём безопасное имя исходного файла
        filename = secure_filename(file_storage.filename)
        ext = os.path.splitext(filename)[1]  # расширение, включая точку

        # Генерируем мини-хеш: например md5(id+file_type)
        hash_input = f"{clan_id}_{file_type}".encode("utf-8")
        file_hash = hashlib.md5(hash_input).hexdigest()  # можно взять первые 8 символов, если хочется
        new_filename = f"{file_hash}{ext}"

        # Папка назначения
        folder = os.path.join(current_app.config["CLAN_FOLDER"], file_type, str(clan_id))
        os.makedirs(folder, exist_ok=True)

        # Полный путь
        file_path = os.path.join(folder, new_filename)

        # Сохраняем
        file_storage.stream.seek(0)
        file_storage.save(file_path)

        return new_filename
    except Exception as ex:
        raise ex