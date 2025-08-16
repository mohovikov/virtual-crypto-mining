from flask_login import current_user
import sqlalchemy.orm as so

from app.constants import Privileges, ClanPrivileges
from app.extensions import db
from app.models import Clan, ClanMember
from app.forms.site_forms import ClanCreateForm


def create_clan(form: ClanCreateForm, creator_id: int) -> tuple[bool, str, str]:
    clan = Clan(
        name=str(form.name.data),
        short_name=str(form.short_name.data),
        is_open=form.is_open.data
    )
    try:
        db.session.add(clan)
        db.session.flush()

        member = ClanMember(
            user_id=creator_id,
            clan_id=clan.id,
            privileges=ClanPrivileges.MEMBER | ClanPrivileges.ADMIN | ClanPrivileges.CREATOR
        )
        db.session.add(member)
        db.session.commit()
        return True, f"Клан «{form.name.data}» успешно создан!", "success"
    except Exception as ex:
        db.session.rollback()
        print(ex)
        return False, f"Ошибка при создании клана:<br>{ex}", "danger"

def get_clan_info(clan_id: int):
    clan = (
        db.session.query(Clan)
        .options(
            so.joinedload(Clan.members).joinedload(ClanMember.user)  # подгрузка user внутри members
        )
        .filter(Clan.id == clan_id)
        .first()
    )
    if clan is None:
        return False

    # Создатель клана (по идее, всегда 1)
    creator = next((m for m in clan.members if Privileges.has_privilege(ClanPrivileges.CREATOR, m.privileges)), None)

    # Остальные участники (без создателя)
    members = [m for m in clan.members if m != creator]

    return {
        "clan": clan,
        "creator": creator,
        "members": members,
        "members_count": len(members)
    }

def get_user_clan_roles(clan_id: int, user_id: int) -> dict:
    """
    Возвращает словарь с флагами ролей пользователя в клане.
    :param clan_id: ID клана
    :param user_id: ID пользователя
    :return: dict с ключами is_member, is_admin, is_creator
    """
    member = db.session.query(ClanMember).filter_by(
        clan_id=clan_id,
        user_id=user_id
    ).first()

    if not member:
        return {
            "is_member": False,
            "is_admin": False,
            "is_creator": False
        }

    return {
        "is_member": True,
        "is_admin": Privileges.has_privilege(ClanPrivileges.ADMIN, member.privileges),
        "is_creator": Privileges.has_privilege(ClanPrivileges.CREATOR, member.privileges)
    }

def join_clan(user_id: int, clan_id: int) -> tuple[bool, str, str]:
    # Проверка — уже лидер?
    if ClanMember.query.filter_by(user_id=current_user.id, privileges=ClanPrivileges.CREATOR).first():
        return False, "Вы уже являетесь лидером клана и не можете вступить в другой.", "warning"

    # Проверка — уже участник?
    if ClanMember.query.filter_by(user_id=current_user.id).first():
        return False, "Вы уже состоите в клане.", "warning"

    clan = Clan.query.get(clan_id)
    if not clan:
        return False, "Клан не найден.", "danger"

    if not clan.is_open:
        return False, "Вступление в этот клан закрыто.", "danger"

    try:
        new_member = ClanMember(
            user_id=current_user.id,
            clan_id=clan.id,
            privileges=ClanPrivileges.MEMBER
        )
        db.session.add(new_member)
        db.session.commit()
        return True, f"Вы успешно вступили в клан «{clan.name}»!", "success"
    except Exception as ex:
        db.session.rollback()
        return False, f"Ошибка при вступлении:<br>{ex}", "danger"

def leave_clan(clan_id) -> tuple[bool, str, str]:
    clan = Clan.query.get_or_404(clan_id)

    # Если лидер
    if clan.leader_id == current_user.id:
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