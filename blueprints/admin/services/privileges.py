from core.models import PrivilegesGroups


def get_all_privileges_groups(to_dict: bool = False):
    if to_dict:
        return {group.privileges: group for group in PrivilegesGroups.query.all()}
    return PrivilegesGroups.query.all()