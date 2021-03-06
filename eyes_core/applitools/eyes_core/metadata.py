import os
import uuid
from datetime import datetime

from enum import Enum

from eyes_core import EyesError
from eyes_core.utils import general_utils


class StartInfo:
    ...


class SessionResults:
    ...


class ImageMatchSettings:
    ...


class ExpectedAppOutput:
    ...


class Branch:
    ...


class ActualAppOutput:
    ...


class BatchInfo(object):
    """
    A batch of tests.
    """

    def __init__(self, name=None, started_at=None):
        # type: (tp.Optional[str], tp.Optional[datetime]) -> None
        if started_at is None:
            started_at = datetime.now(general_utils.UTC)

        self.name = name if name else os.environ.get('APPLITOOLS_BATCH_NAME', None)
        self.started_at = started_at
        self.id_ = os.environ.get('APPLITOOLS_BATCH_ID', str(uuid.uuid4()))

    def __getstate__(self):
        return dict(name=self.name, startedAt=self.started_at.isoformat(), id=self.id_)

    # Required is required in order for jsonpickle to work on this object.
    # noinspection PyMethodMayBeStatic
    def __setstate__(self, state):
        raise EyesError('Cannot create BatchInfo instance from dict!')

    def __str__(self):
        return "%s - %s - %s" % (self.name, self.started_at, self.id_)


class CoordinatesType(Enum):
    """
     Encapsulates the type of coordinates used by the region provider.
    """

    # The coordinates should be used "as is" on the screenshot image.
    # Regardless of the current context.
    SCREENSHOT_AS_IS = 0

    # The coordinates should be used "as is" within the current context. For
    # example, if we're inside a frame, the coordinates are "as is",
    # but within the current frame's viewport.
    CONTEXT_AS_IS = 1

    # Coordinates are relative to the context. For example, if we are in
    # a context of a frame in a web page, then the coordinates are relative to
    # the  frame. In this case, if we want to crop an image region based on
    # an element's region, we will need to calculate their respective "as
    # is" coordinates.
    CONTEXT_RELATIVE = 2
