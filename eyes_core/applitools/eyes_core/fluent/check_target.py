from abc import ABC

from eyes_core.geometry import Region
from eyes_core.fluent.check_settings import CheckSettings

_all_ = ('CheckTarget',)


class CheckTarget(ABC):
    @staticmethod
    def window() -> CheckSettings:
        return CheckSettings(None)

    @staticmethod
    def region(rect: Region) -> CheckSettings:
        return CheckSettings(rect)
