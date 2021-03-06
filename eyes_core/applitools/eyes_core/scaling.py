from __future__ import absolute_import

from applitools.core.utils import ABC
from . import logger

__all__ = ('FixedScaleProvider', 'NullScaleProvider', 'ContextBasedScaleProvider')


class ScaleProvider(ABC):
    _UNKNOWN_SCALE_RATIO = 0.0

    def __init__(self, *args, **kwargs):
        self._scale_ratio = self._UNKNOWN_SCALE_RATIO
        self.device_pixel_ratio = 1

    @property
    def scale_ratio(self):
        return self._scale_ratio

    def update_scale_ratio(self, image_to_scale_width):
        pass


class FixedScaleProvider(ScaleProvider):
    def __init__(self, scale_ratio):
        super(FixedScaleProvider, self).__init__(scale_ratio)
        self._scale_ratio = scale_ratio


class NullScaleProvider(FixedScaleProvider):
    _UNKNOWN_SCALE_RATIO = 1.0


class ContextBasedScaleProvider(ScaleProvider):
    _ALLOWED_VS_DEVIATION = 1
    _ALLOWED_DCES_DEVIATION = 10

    def __init__(self, top_level_context_entire_size, viewport_size,
                 device_pixel_ratio, is_mobile_device):
        super(ContextBasedScaleProvider, self).__init__()
        self.top_level_context_entire_size = top_level_context_entire_size
        self.viewport_size = viewport_size
        self.device_pixel_ratio = device_pixel_ratio
        self.is_mobile_device = is_mobile_device

    @property
    def scale_ratio(self):
        return self._scale_ratio

    @staticmethod
    def get_scale_ratio_to_viewport(viewport_width, image_to_scale_width, current_scale_ratio):
        scaled_image_width = round(image_to_scale_width * viewport_width)
        from_scaled_to_viewport_ratio = viewport_width / scaled_image_width
        return current_scale_ratio * from_scaled_to_viewport_ratio

    def update_scale_ratio(self, image_to_scale_width):
        viewport_width = self.viewport_size['width']
        dces_width = self.top_level_context_entire_size['width']

        # If the image's width is the same as the viewport's width or the
        # top level context's width, no scaling is necessary.
        allowed_vs_deviation = (viewport_width - self._ALLOWED_VS_DEVIATION <= image_to_scale_width
                                <= viewport_width + self._ALLOWED_VS_DEVIATION)
        allowed_dces_deviation = (dces_width - self._ALLOWED_DCES_DEVIATION <= image_to_scale_width
                                  <= dces_width + self._ALLOWED_DCES_DEVIATION)
        if allowed_dces_deviation or allowed_vs_deviation:
            logger.info('Image is already scaled correctly.')
            self._scale_ratio = 1.0
        else:
            logger.info('Calculating the scale ratio..')
            self._scale_ratio = 1.0 / self.device_pixel_ratio
            if self.is_mobile_device:
                logger.info('Mobile device, so using 2 step calculation for scale ration...')
                logger.info('Scale ratio based on DRP: ' + self._scale_ratio)
                self._scale_ratio = self.get_scale_ratio_to_viewport(viewport_width,
                                                                     image_to_scale_width,
                                                                     self._scale_ratio)
            logger.info("Final scale ratio: {}".format(self.scale_ratio))
