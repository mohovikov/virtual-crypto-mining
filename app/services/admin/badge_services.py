from app.extensions import db
from app.forms.admin import BadgeForm, UserBadgesForm
from app.models import Badge, User, UserBadge


def get_all_badges_by_page(page: int = 1, per_page: int = 25):
    badges_query = Badge.query.order_by(Badge.id)
    badges_paginated = badges_query.paginate(page=page, per_page=per_page, error_out=False)
    return badges_paginated

def get_all_badges():
    return Badge.query.all()

def get_badge_by_id(id) -> Badge | None:
    return Badge.query.get(id)

def create_badge(form: BadgeForm) -> tuple[bool, str, str]:
    if not form.name.data or not form.icon.data:
        return False, f"Все поля обязательны к заполнению!", "warning"

    badge = Badge(
        name = form.name.data,
        description = form.description.data,
        icon = form.icon.data,
        color = form.color.data
    )
    try:
        db.session.add(badge)
        db.session.commit()
        return True, f"Бейджик «{form.name.data}» успешно добавлен!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при создании бейджика:<br>{ex}", "danger"

def update_badge(form: BadgeForm, badge: Badge) -> tuple[bool, str, str]:
    if not form.name.data or not form.icon.data:
        return False, "Все поля обязательны к заполнению!", "warning"
    
    badge.name = form.name.data
    badge.description = form.description.data
    badge.icon = form.icon.data
    badge.color = form.color.data

    try:
        db.session.commit()
        return True, f"Бейджик «{form.name.data}» успешно изменен", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при изменении бейджика:<br>{ex}", "danger"

def delete_badge(id: int):
    badge = get_badge_by_id(id)

    if not badge:
        return False, "Такого бейджика не существует!", "danger"
    
    try:
        db.session.delete(badge)
        db.session.commit()
        return True, f"Бейджик «{badge.name}» успешн удален!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при удалении:<br>{ex}", "danger"

def update_user_badges(form: UserBadgesForm, user: User):
    try:
        selected_badges = form.badges.data or []

        UserBadge.query.filter_by(user_id = user.id).delete()

        for badge_id in selected_badges:
            db.session.add(UserBadge(
                user_id = user.id,
                badge_id=int(badge_id))
            )

        db.session.commit()
        return True, f"Бейджики пользователя {user.username} успешно обновленны!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при изменении бейджиков:<br>{ex}", "danger"
