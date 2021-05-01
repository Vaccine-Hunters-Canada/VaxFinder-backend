from enum import IntEnum


class InputTypeEnum(IntEnum):
    scraper = 1
    admin = 2
    user = 3


class RoleEnum(IntEnum):
    admin = 1
    staff = 2
    location = 3
