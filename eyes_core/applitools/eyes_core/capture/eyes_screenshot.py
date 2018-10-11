import abc

from PIL import Image

from eyes_core.geometry import Location, Region
from eyes_core import argument_guard
from eyes_core.metadata import CoordinatesType

__all__ = ('EyesScreenshot',)


class EyesScreenshot(abc.ABC):
    def __init__(self, image):
        # type: (Image.Image) -> None
        argument_guard.is_a(image, Image.Image)
        self._image = image

    @abc.abstractmethod
    def sub_screenshot(self, region: Region,
                       _coordinate_type: CoordinatesType,
                       throw_if_clipped=False,
                       force_none_if_clipped=False) -> Region:
        pass

    @abc.abstractmethod
    def convert_location(self, location: Location,
                         from_: CoordinatesType,
                         to: CoordinatesType) -> Region:
        ...

    @abc.abstractmethod
    def location_in_screenshot(self, location: Location,
                               coordinates_type: CoordinatesType) -> Region:
        ...

    @abc.abstractmethod
    def intersected_region(self, region: Region,
                           original_coordinate_types: CoordinatesType,
                           result_coordinate_types: CoordinatesType) -> Region:
        ...

    def convert_region_location(self, region:Region,
                                from_:CoordinatesType,
                                to:CoordinatesType)->Region:
        argument_guard.not_none(region)
        argument_guard.is_a(region, Region)
        if region.is_empty:
            return Region.create_empty_region()
        argument_guard.not_none(from_)
        argument_guard.not_none(to)

        updated_location = self.convert_location(region.location, from_, to)
        return Region(updated_location.x, updated_location.y, region.width, region.height)

    @property
    def image_region(self) -> Region:
        return Region(0, 0, self._image.width, self._image.height, CoordinatesType.SCREENSHOT_AS_IS)

    @staticmethod
    def from_region(region: Region) -> Image.Image:
        return Image.new('RGBA', (region.width, region.height))
