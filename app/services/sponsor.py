from markupsafe import Markup

from app.extensions import db
from app.helpers import add_sponsor_time
from app.models.users import Users
from app.constants.privileges import Privileges
from app.forms.admin_forms import GiveSponsorForm


def give_sponsor(form: GiveSponsorForm, user: Users):
    try:
        user.sponsor_expire = add_sponsor_time(user.sponsor_expire, form.amount.data, form.unit.data)
        user.privileges |= Privileges.USER_SPONSOR
        db.session.commit()
        return True, Markup(
            f"Пользователю {user.username} выдан спонсор до "
            f"<time class=\"js-datetime\" data-utc=\"{user.sponsor_expire}\"></time>"
        ), "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при выдаче спонсорства: {ex}", "danger"