from flask_login import current_user

from app.extensions import db
from app.forms.site_forms import SettingsForm
from app.helpers.file_helper import save_user_hashed_file


def update_avatar(form: SettingsForm):
    try:
        if hasattr(form, "avatar_file") and form.avatar_file.data:
            current_user.avatar_file = save_user_hashed_file(current_user.id, form.avatar_file.data, "avatar")
        db.session.commit()

        return f"Аватар успешно обновлен!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return f"Ошибка при сохранении аватарки:<br>{ex}", "danger"