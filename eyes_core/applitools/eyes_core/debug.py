from abc import ABC


class DebugScreenshotsProvider(ABC):
    ...


class FileDebugScreenshotsProvider(DebugScreenshotsProvider):
    ...


class NullDebugScreenshotProvider(DebugScreenshotsProvider):
    ...
