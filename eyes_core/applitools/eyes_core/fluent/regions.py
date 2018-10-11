import abc
import typing as tp

import attr

from eyes_core.match import FloatingMatchSettings
from eyes_core.geometry import Region
from eyes_core.eyes_base import EyesBase
from eyes_core.capture.eyes_screenshot import EyesScreenshot

__all__ = ('GetFloatingRegion', 'GetRegion',
           'IgnoreRegionByRectangle', 'FloatingRegionByRectangle')


class GetFloatingRegion(abc.ABC):
    @abc.abstractmethod
    def get_region(self, eyes: EyesBase,
                   screenshot: EyesScreenshot) -> tp.List[FloatingMatchSettings]:
        ...


class GetRegion(abc.ABC):
    @abc.abstractmethod
    def get_region(self, eyes: EyesBase,
                   screenshot: EyesScreenshot) -> tp.List[Region]:
        ...


@attr.s
class IgnoreRegionByRectangle(GetRegion):
    _region = attr.ib()  # type: Region

    def get_region(self, eyes, screenshot):
        return [self._region]


@attr.s
class FloatingRegionByRectangle(GetFloatingRegion):
    _rect = attr.ib()  # type: Region
    _max_up_offset = attr.ib()
    _max_down_offset = attr.ib()
    _max_left_offset = attr.ib()
    _max_right_offset = attr.ib()

    def get_region(self, eyes: EyesBase,
                   screenshot: EyesScreenshot):
        return FloatingMatchSettings(
            self._rect.left,
            self._rect.top,
            self._rect.width,
            self._rect.height,

            self._max_up_offset,
            self._max_down_offset,
            self._max_left_offset,
            self._max_right_offset,
        )
