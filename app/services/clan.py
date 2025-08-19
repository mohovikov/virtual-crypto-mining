from typing import List, Optional, Tuple
from flask_login import current_user

from app.extensions import db
from app.helpers import save_clan_hashed_file
from app.models import Clan, ClanMember, User
from app.forms.site_forms import ClanCreateForm, ClanSettingsForm


def create_clan(form: ClanCreateForm, creator_id: int) -> tuple[bool, str, str]:
    if db.session.query(Clan).filter((Clan.name == form.name.data) | (Clan.short_name == form.short_name.data)).first():
        return False, "Клан с таким именем или тегом уже существует", "warning"

    try:
        clan = Clan(
            name=str(form.name.data),
            short_name=str(form.short_name.data),
            is_open=form.is_open.data,
            leader_id=creator_id
        )
        db.session.add(clan)
        db.session.flush()

        member = ClanMember(
            user_id=creator_id,
            clan_id=clan.id
        )
        db.session.add(member)

        db.session.commit()
        return True, f"Клан «{form.name.data}» успешно создан!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при создании клана:<br>{ex}", "danger"

def get_clan_info(clan_id: int):
    return Clan.query.get(clan_id)

def get_clan_profile(clan_id: int) -> Tuple[Optional[Clan], Optional[User], List[ClanMember]]:
    """
    Получает данные профиля клана.
    Возвращает (clan, leader, members).
    """
    clan: Clan | None = db.session.get(Clan, clan_id)
    if not clan:
        return None, None, []

    leader: User = clan.leader

    # извлекаем список участников (User), сортируем по дате вступления
    members: List[ClanMember] = sorted(clan.members, key=lambda x: x.created_at)

    return clan, leader, members

def join_clan(user_id: int, clan_id: int) -> tuple[bool, str, str]:
    # Проверка — уже лидер?
    if Clan.query.filter_by(leader_id=user_id).first():
        return False, "Вы уже являетесь лидером клана и не можете вступить в другой.", "warning"

    # Проверка — уже участник?
    if ClanMember.query.filter_by(user_id=user_id).first():
        return False, "Вы уже состоите в клане.", "warning"

    clan = Clan.query.get(clan_id)
    if not clan:
        return False, "Клан не найден.", "info"

    if not clan.is_open:
        return False, "Вступление в этот клан закрыто.", "info"

    try:
        new_member = ClanMember(
            user_id=user_id,
            clan_id=clan.id
        )
        db.session.add(new_member)
        db.session.commit()
        return True, f"Вы успешно вступили в клан «{clan.name}»!", "success"
    except Exception as ex:
        db.session.rollback()
        return False, f"Ошибка при вступлении:<br>{ex}", "danger"

def leave_clan(user_id: int, clan_id: int) -> tuple[bool, str, str]:
    clan = Clan.query.get_or_404(clan_id)

    # Если лидер
    if clan.leader_id == user_id:
        # Проверяем, есть ли ещё участники
        members_count = ClanMember.query.filter_by(clan_id=clan.id).count()
        if members_count > 0:
            return False, "Перед выходом передайте лидерство другому участнику или распустите клан.", "warning"

        db.session.delete(clan)
        db.session.commit()
        return True, f"Клан «{clan.name}» распущен.", "success"

    # Если обычный участник
    membership = ClanMember.query.filter_by(clan_id=clan.id, user_id=current_user.id).first()
    if membership:
        db.session.delete(membership)
        db.session.commit()
        return False, f"Вы покинули клан «{clan.name}».", "success"
    else:
        return True, "Вы не состоите в этом клане.", "danger"

def save_clan_settings(clan: Clan, form: ClanSettingsForm) -> Tuple[bool, str, str]:
    clan.name = str(form.name.data)
    clan.short_name = str(form.short_name.data)
    clan.url = str(form.url.data)
    clan.description = str(form.description.data)
    clan.is_open = bool(int(form.is_open.data))

    if hasattr(form, "logo_file") and form.logo_file.data:
        clan.logo_file = save_clan_hashed_file(clan.id, form.logo_file.data, "logo")
    if hasattr(form, "banner_file") and form.banner_file.data:
        clan.header_file = save_clan_hashed_file(clan.id, form.banner_file.data, "banner")

    try:
        db.session.commit()
        return True, f"Настройки клана успешно сохранены!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при сохранении:<br>{ex}", "danger"