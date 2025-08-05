from blueprints.admin import forms
from core import db, models


def get_all_privileges_groups(to_dict: bool = False):
    if to_dict:
        return {group.privileges: group for group in models.PrivilegesGroups.query.all()}
    return models.PrivilegesGroups.query.all()

def get_privileges_groups_by_id(id):
    privilege_group = models.PrivilegesGroups.query.get(id)
    if not privilege_group:
        return False, "Группа привилегий с таким ID не найдена", "warning"
    return True, privilege_group

def add_privileges_groups(form: forms.PrivilegesGroupsForm):
    privilege_group = models.PrivilegesGroups(
        name=str(form.name.data),
        privileges=int(str(form.privileges.data)),
        color_class=form.color_class.data
    )

    try:
        db.session.add(privilege_group)
        db.session.commit()
        return True, f"Группа привилегий {form.name.data} успешно добавлена!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return True, f"Ошибка при добавлении группа привилегий: {ex}", "danger"

def update_privileges_groups(privileges_groups: models.PrivilegesGroups, form: forms.PrivilegesGroupsForm):
    try:
        privileges_groups.name = str(form.name.data)
        privileges_groups.privileges = int(str(form.privileges.data))
        privileges_groups.color_class = form.color_class.data

        db.session.commit()
        return True, f"Группа привилегий {form.name.data} успешно изменена!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при изменении группы привилегий: {ex}", "danger"

def delete_privileges_groups(id: int):
    success, result, *rest = get_privileges_groups_by_id(id)

    if not success:
        return success, result, rest[0] if rest else "danger"

    try:
        db.session.delete(result)
        db.session.commit()

        return True, f"Группа привилегий {result.name} успешно удалена!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при удалении группы привилегий: {ex}", "danger"