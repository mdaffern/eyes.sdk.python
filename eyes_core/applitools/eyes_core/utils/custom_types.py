from __future__ import absolute_import

import typing as tp

if tp.TYPE_CHECKING:
    from eyes_selenium.webdriver.remote.webdriver import WebDriver
    from eyes_selenium.webdriver.remote.webelement import WebElement

    from applitools.core.geometry import Region
    from applitools.selenium.webdriver import EyesWebDriver
    from applitools.selenium.webelement import EyesWebElement

    RunningSession = tp.Dict[str, tp.Any]
    ViewPort = tp.Dict[str, int]
    AppOutput = tp.Dict[str, tp.Any]
    MatchResult = tp.Dict[str, tp.Any]
    AppEnvironment = tp.Dict[str, tp.Any]
    SessionStartInfo = tp.Dict[str, tp.Any]
    Num = tp.Union[int, float]

    AnyWebDriver = tp.Union[EyesWebDriver, WebDriver]
    AnyWebElement = tp.Union[EyesWebElement, WebElement]
    FrameReference = tp.Union[str, int, EyesWebElement, WebElement]

    # could contain MouseTrigger, TextTrigger
    UserInputs = tp.List
    RegionOrElement = tp.Union[EyesWebElement, Region]
