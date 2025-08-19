from datetime import datetime, timezone
from flask import render_template
from flask_mailman import EmailMessage
from markupsafe import Markup

from app.extensions import db
from app.helpers import add_sponsor_time
from app.models.users import User
from app.constants.privileges import Privileges
from app.forms.admin_forms import GiveSponsorForm


def give_sponsor(form: GiveSponsorForm, user: User):
    try:
        user.sponsor_expire = add_sponsor_time(user.sponsor_expire, form.amount.data, form.unit.data)
        user.privileges |= Privileges.USER_SPONSOR
        db.session.commit()

        expire = user.sponsor_expire
        if expire.tzinfo is None:  # если naive, делаем aware
            expire = expire.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        months_expire = round((expire - now).days / 30)

        # выбираем текст "TheMoreYouKnow"
        if months_expire >= 20:
            the_more_you_know = "Знаете ли вы, что ваша поддержка почти приравнивается к содержанию целой виртуальной фермы для майнинга на протяжении месяца? Это огромный вклад в стабильность проекта. Спасибо вам огромное!"
        elif 15 <= months_expire < 20:
            the_more_you_know = "Ваша помощь покрывает значительную часть расходов на виртуальные мощности для добычи криптовалюты — почти три четверти от месячного цикла. Это очень серьёзный вклад, и мы благодарны за поддержку!"
        elif 10 <= months_expire < 15:
            the_more_you_know = "С вашей поддержкой мы можем продлить аренду виртуальных серверов для майнинга почти на целый год. Это помогает нам держать проект на плаву. Спасибо!"
        elif 4 <= months_expire < 10:
            the_more_you_know = "Благодаря вашему вкладу мы сможем обеспечить работу одного из виртуальных узлов для добычи криптовалюты на целый месяц. Это очень важно для стабильности системы!"
        elif 1 <= months_expire < 4:
            the_more_you_know = "Даже небольшая поддержка позволяет нам содержать дополнительные мощности для мониторинга и логирования виртуальной добычи. Такие вклады тоже очень ценны!"
        else:
            the_more_you_know = False

        # рендерим HTML-шаблон письма
        html_body = render_template(
            "email/sponsor.html",
            username=user.username,
            months_expire=months_expire,
            the_more_you_know=the_more_you_know
        )

        # формируем письмо
        email = EmailMessage(
            subject="Спасибо за поддержку!",
            body=html_body,
            to=[user.email]
        )
        email.content_subtype = "html"
        email.send()
    
        return True, Markup(
            f"Пользователю {user.username} выдан спонсор до "
            f"<time class=\"js-datetime\" data-utc=\"{user.sponsor_expire}\"></time>"
        ), "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при выдаче спонсорства: {ex}", "danger"