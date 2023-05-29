from enum import Enum


class UserStatus(str, Enum):
    ACTIVE: str = "ACTIVE"
    BANNED: str = "BANNED"


class UserRole(str, Enum):
    ADMIN: str = "ADMIN"
    USER: str = "USER"
