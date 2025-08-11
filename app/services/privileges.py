from app.extensions import db
from app.forms.admin_forms import AddPrivilegeGroup
from app.models import PrivilegesGroups


def get_all_privileges():
    return PrivilegesGroups.query.all()

def add_privilege_group(form: AddPrivilegeGroup) -> tuple[bool, str, str]:
    group = PrivilegesGroups(
        name=form.name.data,
        color_class=form.color_class.data,
        privileges=form.privileges_value.data
    )

    try:
        db.session.add(group)
        db.session.commit()
        return True, f"Группа привилегий ({form.name.data}) успешно создана", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при создании группы: {ex}", "danger"