import abc
import typing as tp

import attr

from eyes_core import Point

__all__ = ('PositionProvider', 'InvalidPositionProvider', 'PositionMemento')


@attr.s
class PositionProvider(abc.ABC):
    _states = attr.ib(init=False, factory=list)

    @abc.abstractmethod
    def get_current_position(self) -> tp.Optional[Point]:
        """
        :return: The current position, or `None` if position is not available.
        """

    @abc.abstractmethod
    def set_position(self, location: Point):
        """
        Go to the specified location.

        :param location: The position to set
        """

    @property
    @abc.abstractmethod
    def get_entire_size(self) -> ViewPort:
        """
        :return: The entire size of the container which the position is relative to.
        """

    def push_state(self):
        """
        Adds the current position to the states list.
        """
        self._states.append(self.get_current_position())

    def pop_state(self):
        """
        Sets the position to be the last position added to the states list.
        """
        self.set_position(self._states.pop())


class InvalidPositionProvider(PositionProvider):
    """
    An implementation of :py:class:`PositionProvider` which throws an exception
    for every method. Can be used as a placeholder until an actual
    implementation is set.
    """

    def get_current_position(self):
        raise NotImplementedError("This class does not implement methods!")

    def set_position(self, location: Point):
        raise NotImplementedError("This class does not implement methods!")

    def get_entire_size(self):
        raise NotImplementedError("This class does not implement methods!")


class PositionMemento(abc.ABC):
    """
    A base class for position related memento instances. This is intentionally
    not an interface, since the mementos might vary in their interfaces.
    """
