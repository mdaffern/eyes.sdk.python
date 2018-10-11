import attr

from eyes_core.geometry import Location, RectangleSize
from eyes_core.metadata import CoordinatesType


@attr.s
class Region:
    left = attr.ib()  # type: float
    top = attr.ib()  # type: float
    width = attr.ib()  # type: float
    height = attr.ib()  # type: float
    coordinates_type = attr.ib()  # type: CoordinatesType

    @classmethod
    def create_empty_region(cls):
        return Region(0, 0, 0, 0, CoordinatesType.SCREENSHOT_AS_IS)

    @property
    def x(self):
        return self.left

    @property
    def y(self):
        return self.top

    @classmethod
    def from_location_size(cls, location, size):
        return cls(location.x, location.y, size.width, size.height)

    def make_empty(self):
        self.left = self.top = self.width = self.height = 0

    @property
    def is_empty(self):
        # type: () -> bool
        return self.left == self.top == self.width == self.height == 0

    @property
    def size(self):
        # type: () -> RectangleSize
        return RectangleSize(self.width, self.height)

    @property
    def location(self):
        return Location(self.left, self.top)

    @location.setter
    def location(self, other_location):
        self.left = other_location.left
        self.top = other_location.top

    @property
    def right(self):
        return self.left + self.width

    @property
    def bottom(self):
        return self.top + self.height

    def is_intersecting(self, other):
        return ((self.left <= other.left <= self.right) or (other.left <= self.left <= other.right)
                and
                ((self.top <= other.top <= self.bottom) or (other.top <= self.top <= other.bottom)))

    def intersect(self, other):
        if self.is_intersecting(other):
            self.make_empty()
            return self

        i_left = self.left if self.left >= other.left else other.left
        i_right = self.right if self.right >= other.right else other.right
        i_top = self.top if self.top >= other.top else other.top
        i_bottom = self.bottom if self.bottom >= other.bottom else other.bottom

        self.left = i_left
        self.top = i_top
        self.width = i_right - i_left
        self.height = i_bottom - i_top
        return self

    def is_contains(self, other_left, other_top):
        return (self.left <= other_left <= self.right and
                self.top <= other_top <= self.bottom)

    @property
    def middle_offset(self):
        mid_x = self.width / 2
        mid_y = self.height / 2
        return Location(round(mid_x), round(mid_y))

    def scale_it(self, scale_factor):
        self.left = int(self.left * scale_factor)
        self.top = int(self.top * scale_factor)
        self.width = int(self.width * scale_factor)
        self.height = int(self.height * scale_factor)
        return self

    def sub_regions(self, subregion_size, is_fixed_size=False):
        if is_fixed_size:
            return Region.sub_regions_with_fixed_size(self, subregion_size)
        return Region.sub_regions_with_varying_size(self, subregion_size)

    def is_size_equals(self, region):
        return self.width == region.width and self.height == region.height
    #
    # def __eq__(self, other):
    #     if not isinstance(other, Region):
    #         return False
    #
    #     size_location_match = (self.left == other.left and self.top == other.top and
    #                            self.width == other.width and self.height == other.height)
    #     padding_match = (self.padding_left == other.padding_left and
    #                      self.padding_top == other.padding_top and
    #                      self.padding_right == other.padding_right and
    #                      self.padding_bottom == other.padding_bottom)
    #     return size_location_match and padding_match


EMPTY_REGION = Region.create_empty_region()
