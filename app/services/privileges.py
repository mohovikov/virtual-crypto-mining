from typing import Any

from app.extensions import db
from app.constants import Privileges
from app.forms.admin_forms import AddPrivilegeGroup
from app.models import PrivilegesGroups


def get_all_privileges(privileges: int = -1, to_dict = False) -> list[Any] | list[dict[str, str,]]:
    if to_dict and privileges != -1:
        groups = []
        for group in PrivilegesGroups.query.all():
            groups.append({
                "name": group.name,
                "privileges": group.privileges,
                "selected": True if privileges == group.privileges or privileges == (group.privileges | Privileges.USER_SPONSOR) else False
            })
        return groups
    return PrivilegesGroups.query.all()

def get_privilege_group(by_privileges: int = -1) -> dict[str, str] | None:
    if by_privileges != 1:
        group = PrivilegesGroups.query.filter_by(privileges=by_privileges).first()
        if group:
            return {
                "name": group.name,
                "color_class": group.color_class
            }
    return None

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