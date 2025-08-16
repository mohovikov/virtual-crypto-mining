from enum import IntEnum, unique


@unique
class ClanPrivileges(IntEnum):
    MEMBER     = 1 << 0
    ADMIN      = 2 << 0
    CREATOR    = 2 << 1