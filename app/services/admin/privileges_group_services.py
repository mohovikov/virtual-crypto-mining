from app.extensions import db
from app.forms.admin import PrivilegeForm
from app.models import PrivilegesGroup


def get_all_privileges_group() -> list[PrivilegesGroup]:
    return PrivilegesGroup.query.all()

def get_privileges_group_by_id(id: int) -> PrivilegesGroup | None:
    return PrivilegesGroup.query.get(id)

def create_privileges_group(form: PrivilegeForm) -> tuple[bool, str, str]:
    if not form.name.data or not form.privileges_value.data or not form.color.data:
        return False, "Все поля обязательны к заполнению!", "danger"

    group = PrivilegesGroup(
        name = form.name.data,
        privileges = form.privileges_value.data,
        color = form.color.data
    )
    try:
        db.session.add(group)
        db.session.commit()
        return True, f"Группа «{ form.name.data }» успешно создана!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при создании:<br>{ex}", "danger"

def save_privileges_group(group: PrivilegesGroup | None, form: PrivilegeForm) -> tuple[bool, str, str]:
    if not group:
        return False, "Такой группы не существует!", "danger"

    if not form.name.data or not form.privileges_value.data:
        return False, "Все поля обязательны к заполнению!", "danger"

    try:
        group.name = form.name.data
        group.privileges = form.privileges_value.data
        group.color = form.color.data

        db.session.commit()
        return True, f"Группа «{ form.name.data }» успешно изменена!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при сохранении:<br>{ex}", "danger"

def delete_privileges_group(id: int):
    group = get_privileges_group_by_id(id)

    if not group:
        return False, "Такой группы не существует!", "danger"
    
    try:
        db.session.delete(group)
        db.session.commit()
        return True, f"Группа «{group.name}» успешно удалена!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при удалении:<br>{ex}", "danger"

# Template function
def get_privileges_group_by_privileges(privileges: int) -> tuple[str, str]:
    group = PrivilegesGroup.query.filter_by(privileges = privileges).first()
    if not group:
        return f"Неизвестно ({privileges})", "danger"
    return group.name, group.color