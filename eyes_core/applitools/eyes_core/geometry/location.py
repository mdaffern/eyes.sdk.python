import attr

from eyes_core.errors import EyesIllegalArgument


@attr.s
class Location:
    x = attr.ib()
    y = attr.ib()

    @classmethod
    def create_top_left(cls):
        return cls(0, 0)

    @property
    def values(self):
        return self.x, self.y

    def offset(self, other):
        self.x += other.x
        self.y += other.y
        return self

    def offset_negative(self, other):
        self.x -= other.x
        self.y -= other.y
        return self

    def scale_it(self, scale_factor):
        if not isinstance(scale_factor, int):
            raise EyesIllegalArgument('scale_factor must be an integer')
        self.x *= scale_factor
        self.y *= scale_factor
        return self


EMPTY_LOCATION = Location.create_top_left()
