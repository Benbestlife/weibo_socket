import json
from enum import (
    Enum,
    auto,
)


class UserRole(Enum):
    guest = auto()
    normal = auto()


class Encoder(json.JSONEncoder):
    prefix = "__enum__"

    def default(self, o):
        if isinstance(o, UserRole):
            return {self.prefix: o.name}
        else:
            return super().default(o)


def weibo_decode(d):
    if Encoder.prefix in d:
        name = d[Encoder.prefix]
        return UserRole[name]
    else:
        return d
