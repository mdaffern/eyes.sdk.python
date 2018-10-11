import typing as tp
from abc import ABC

import attr
from multimethod import multimethod

from eyes_core import logger
from eyes_core.geometry import Region
from eyes_core.fluent.regions import GetRegion, IgnoreRegionByRectangle, GetFloatingRegion, FloatingRegionByRectangle
from eyes_core.match import MatchLevel, FloatingMatchSettings

__all__ = ('CheckSettings',)


@attr.s
class _CheckSettingsValues:
    """
    Access to values stored in :py:class:`CheckSettings`
    """
    check_settings = attr.ib()  # type: CheckSettings

    @property
    def ignore_caret(self):
        return self.check_settings._ignore_caret

    @property
    def stitch_content(self):
        return self.check_settings._stitch_content

    @property
    def ignore_regions(self):
        return self.check_settings._ignore_regions

    @property
    def strict_regions(self):
        return self.check_settings._strict_regions

    @property
    def content_regions(self):
        return self.check_settings._content_regions

    @property
    def floating_regions(self):
        return self.check_settings._floating_regions

    @property
    def match_level(self):
        return self.check_settings._match_level

    @property
    def timeout(self):
        return self.check_settings._timeout

    @property
    def target_region(self):
        return self.check_settings._target_region

    @property
    def name(self):
        return self.check_settings._name


@attr.s
class CheckSettings(ABC):
    """
    The Match settings object to use in the various Eyes.Check methods.
    """

    _ignore_caret = attr.ib(init=False, default=False)  # type: bool
    _stitch_content = attr.ib(init=False, default=False)  # type: bool
    _ignore_regions = attr.ib(init=False, factory=list)  # type: tp.List[GetRegion]
    _layout_regions = attr.ib(init=False, factory=list)  # type: tp.List[GetRegion]
    _strict_regions = attr.ib(init=False, factory=list)  # type: tp.List[GetRegion]
    _content_regions = attr.ib(init=False, factory=list)  # type: tp.List[GetRegion]
    _floating_regions = attr.ib(init=False, factory=list)  # type: tp.List[GetFloatingRegion]
    _match_level = attr.ib(init=False, default=None)  # type: MatchLevel
    _name = attr.ib(init=False)  # type: str

    _target_region = attr.ib()  # type: tp.Optional[Region]
    _timeout = attr.ib(default=-1)  # type: int

    def values(self):
        return _CheckSettingsValues(self)

    def layout(self) -> 'CheckSettings':
        """ Shortcut to set the match level to :py:attr:`MatchLevel.LAYOUT`. """
        self._match_level = MatchLevel.LAYOUT
        return self

    def exact(self) -> 'CheckSettings':
        """ Shortcut to set the match level to :py:attr:`MatchLevel.EXACT`. """
        self._match_level = MatchLevel.EXACT
        return self

    def strict(self) -> 'CheckSettings':
        """ Shortcut to set the match level to :py:attr:`MatchLevel.STRICT`. """
        self._match_level = MatchLevel.STRICT
        return self

    def content(self) -> 'CheckSettings':
        """ Shortcut to set the match level to :py:attr:`MatchLevel.CONTENT`. """
        self._match_level = MatchLevel.CONTENT
        return self

    def match_level(self, match_level: MatchLevel) -> 'CheckSettings':
        """ """
        self._match_level = match_level
        return self

    def ignore_caret(self, ignore=True) -> 'CheckSettings':
        self._ignore_caret = ignore
        return self

    def fully(self, fully=True) -> 'CheckSettings':
        self._stitch_content = fully
        return self

    def with_name(self, name):
        self._name = name
        return self

    def stitch_content(self, stitch_content=True) -> 'CheckSettings':
        self._stitch_content = stitch_content
        return self

    def timeout(self, timeout_ms: int) -> 'CheckSettings':
        self._timeout = timeout_ms
        return self

    def update_target_region(self, region: Region):
        self._target_region = region

    def ignore_regions(self, *regions) -> 'CheckSettings':
        """ Adds one or more ignore regions. """
        return self.__regions(regions, method_name='ignore_regions')

    def layout_regions(self, *regions) -> 'CheckSettings':
        """ Adds one or more layout regions. """
        return self.__regions(regions, method_name='layout_regions')

    def strict_regions(self, *regions) -> 'CheckSettings':
        """ Adds one or more strict regions. """
        return self.__regions(regions, method_name='strict_regions')

    def content_regions(self, *regions) -> 'CheckSettings':
        """ Adds one or more content regions. """
        return self.__regions(regions, method_name='content_regions')

    def floating(self, *args) -> 'CheckSettings':
        """ Adds a floating region. Details in :py:func:`_floating` """
        region_or_container = _floating(*args)
        self._floating_regions.append(region_or_container)
        return self

    def __regions(self, regions, method_name) -> 'CheckSettings':
        if not regions:
            raise TypeError("{name} method called without arguments!".format(name=method_name))

        regions_list = getattr(self, "_" + method_name)
        for region in regions:
            regions_list.append(_region_to_region_provider(region, method_name))
        return self


def _region_to_region_provider(region: tp.Union[GetRegion, Region], method_name: str):
    if isinstance(region, Region):
        return IgnoreRegionByRectangle(region)

    if isinstance(region, GetRegion):
        return region

    raise TypeError("{name} method called with argument of unsupported type!".format(name=method_name))


@multimethod
def _floating(region_or_container: GetFloatingRegion):
    logger.debug("_floating: GetFloatingRegion")
    return region_or_container


@multimethod
def _floating(region_or_container: FloatingMatchSettings):
    logger.debug("_floating: FloatingMatchSettings")
    return FloatingRegionByRectangle(
        region_or_container.get_region(),
        region_or_container.max_up_offset,
        region_or_container.max_down_offset,
        region_or_container.max_left_offset,
        region_or_container.max_right_offset,
    )


@multimethod
def _floating(region_or_container: Region,
              max_up_offset: int,
              max_down_offset: int,
              max_left_offset: int,
              max_right_offset: int):
    logger.debug("_floating: Region")
    return FloatingRegionByRectangle(
        Region(region_or_container),
        max_up_offset,
        max_down_offset,
        max_left_offset,
        max_right_offset,
    )
