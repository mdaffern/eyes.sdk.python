from abc import ABC


class CutProvider(ABC):
    ...


class FixedCutProvider(CutProvider):
    ...


class NullCutProvider(CutProvider):
    ...


class UnscaledFixedCutProvider(CutProvider):
    ...
