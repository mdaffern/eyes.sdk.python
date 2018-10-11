import attr


@attr.s
class RectangleSize:
    width = attr.ib()
    height = attr.ib()

    def scale_it(self, scale_factor):
        self.width *= scale_factor
        self.height *= scale_factor

    @property
    def square(self):
        return self.width * self.height
