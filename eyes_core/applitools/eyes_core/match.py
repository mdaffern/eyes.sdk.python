import typing as tp

import attr
from enum import Enum

from eyes_core import Region
from .errors import EyesError


class MatchLevel(Enum):
    """
    The extent in which two images match (or are expected to match).
    """
    # Images do not necessarily match.
    NONE = 0
    # Images have the same layout (legacy algorithm).
    LEGACY_LAYOUT = 1
    # Images have the same layout.
    LAYOUT = 2
    # Images have the same layout.
    LAYOUT2 = 3
    # Images have the same content.
    CONTENT = 4
    # Images are nearly identical.
    STRICT = 5
    # Images are identical.
    EXACT = 6


@attr.s
class ExactMatchSettings(object):
    """
    Encapsulates settings for the :py:class:`MatchLevel.EXACT`.
    """

    min_diff_intensity = attr.ib()  # type: int
    min_diff_width = attr.ib()  # type: int
    min_diff_height = attr.ib()  # type: int
    match_threshold = attr.ib()  # type: float


class ImageMatchSettings:
    """
    Encapsulates match settings for the a session.
    """

    match_level = attr.ib(default=MatchLevel.STRICT, converter=lambda x: x.name)
    exact_settings = attr.ib(default=None)


@attr.s
class FloatingMatchSettings:
    left = attr.ib()
    top = attr.ib()
    width = attr.ib()
    height = attr.ib()
    max_up_offset = attr.ib()
    max_down_offset = attr.ib()
    max_left_offset = attr.ib()
    max_right_offset = attr.ib()

    def get_region(self):
        return Region(left=self.left, top=self.top,
                      width=self.width, height=self.height)
