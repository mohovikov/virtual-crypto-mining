import os
from flask_login import current_user

from app.extensions import db
from app.config import Config
from app.forms.site.settings_form import SettingsForm
import app.helpers.images_helper as images


def change_user_profile(form: SettingsForm):
    try:
        current_user.username_aka = form.username_aka.data
        db.session.commit()

        return "Дополнительный никнейм успешно обновлен!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return f"Ошибка при сохранении:<br>{ex}", "danger"

def change_user_country(form: SettingsForm):
    try:
        current_user.country = form.country.data
        db.session.commit()

        return "Страна успешно обновленна!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return f"Ошибка при сохранении:<br>{ex}", "danger"

def save_user_avatar(form: SettingsForm):
    try:
        filename = images.save_user_file(
            file = form.avatar_file.data,
            user_id = str(current_user.id),
            file_type = "avatar",
            folder = os.path.join(Config.USER_AVATAR_FOLDER, str(current_user.id))
        )
        current_user.avatar_file = filename
        db.session.commit()
        return "Аватарка успешно обновлена!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return f"Ошибка при сохранении:<br>{ex}", "danger"

def save_user_background(form: SettingsForm):
    try:
        filename = images.save_user_file(
            file = form.background_file.data,
            user_id = str(current_user.id),
            file_type = "background",
            folder = os.path.join(Config.USER_BACKGROUND_FOLDER, str(current_user.id))
        )
        current_user.background_file = filename
        db.session.commit()
        return "Задний фон профиля успешно обновлен!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return f"Ошибка при сохранении:<br>{ex}", "danger"