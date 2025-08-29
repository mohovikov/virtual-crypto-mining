from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
import wtforms as forms
import wtforms.validators as validators
from PIL import Image
from io import BytesIO
from werkzeug.datastructures import FileStorage

from app.helpers.template_helper import get_country_choices


class SettingsForm(FlaskForm):
    username = forms.StringField(
        label = "Имя пользователя",
        validators = [
            validators.Optional()
        ],
        render_kw = {
            "class": "form-control"
        }
    )
    username_aka = forms.StringField(
        label = "Дополнительное никнейм (не используется для входа)",
        validators = [
            validators.Optional()
        ],
        render_kw = {
            "class": "form-control"
        }
    )
    email = forms.EmailField(
        label = "Email",
        validators = [
            validators.Optional(),
            validators.Email()
        ],
        render_kw = {
            "class": "form-control"
        }
    )
    country = forms.SelectField(
        label = "Страна",
        validators = [
            validators.Optional()
        ],
        choices = get_country_choices,
        render_kw = {
            "class": "form-select"
        },
        validate_choice = False
    )

    userpage = forms.TextAreaField(
        label = "Страница пользователя",
        validators = [
            validators.Optional()
        ],
        render_kw = {
            "class": "form-select"
        }
    )

    old_password = forms.PasswordField(
        label = "Старый пароль",
        validators = [
            validators.Optional(),
            validators.Length(min = 8)
        ],
        render_kw = {
            "class": "form-control"
        }
    )
    new_password = forms.PasswordField(
        label = "Новый пароль",
        validators = [
            validators.Optional(),
            validators.Length(min = 8)
        ],
        render_kw = {
            "class": "form-control"
        }
    )
    confirm_new_password = forms.PasswordField(
        label = "Подтверждение нового пароля",
        validators = [
            validators.Optional(),
            validators.DataRequired(),
            validators.EqualTo("new_password")
        ],
        render_kw = {
            "class": "form-control"
        }
    )

    avatar_file = forms.FileField(
        label = "Аватарка",
        validators = [
            validators.Optional(),
            FileAllowed(["jpg", "jpeg", "png", "gif"], "Только изображения!")
        ],
        render_kw = {
            "class": "form-control w-50 mx-auto"
        }
    )
    background_file = forms.FileField(
        label = "Фон профиля",
        validators = [
            validators.Optional()
        ],
        render_kw = {
            "class": "form-control w-50 mx-auto"
        }
    )

    submit = forms.SubmitField(
        label="Сохранить изменения",
        render_kw = {
            "class": "btn btn-sm btn-primary"
        }
    )

    def validate_avatar_file(self, field):
        if not field.data:
            return
        image = Image.open(field.data)

        if image.width != image.height:
            raise validators.ValidationError("Аватар должен быть с соотношением 1:1")

        if image.width > 256:
            image = image.resize((256, 256), Image.Resampling.LANCZOS)

            buffer = BytesIO()
            image_format = 'PNG' if image.mode in ('RGBA', 'LA') else 'JPEG'
            image.save(buffer, format=image_format)
            buffer.seek(0)

            field.data = FileStorage(
                stream=buffer,
                filename=field.data.filename,
                content_type=field.data.content_type
            )

    def validate_background_file(self, field):
        if not field.data:
            return

        image = Image.open(field.data)
        if image.width / image.height != 16/9:
            raise validators.ValidationError("Фон должен быть с соотношением 16:9")

        if image.width > 2048 or image.height > 1152:
            raise validators.ValidationError("Максимальное разрешение баннера: 2048x1152")