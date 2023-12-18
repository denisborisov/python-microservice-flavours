"""Class to fetch data from controllers."""

import types
import typing
import typing_extensions

from pydantic import HttpUrl
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait

from ..settings import AppSettings
from ..domain.exceptions import WebScraperError

if typing.TYPE_CHECKING:
    from selenium.webdriver.remote.webdriver import WebDriver


class AbstractWebScraper(typing.Protocol):
    def __enter__(self) -> typing_extensions.Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool | None:
        return None

    def load_web_page(self, url: HttpUrl) -> None:
        try:
            self._load_web_page(url)
        except Exception as ex:  # noqa: BLE001
            raise WebScraperError from ex

    def check_dictionary_availability(self) -> bool:
        return self._check_dictionary_availability()

    def extract_text_from_elements(self, css_selector: str) -> list[str]:
        elements = self.find_all_elements_by_css_selector(css_selector)
        return self._extract_text_from_elements(elements)

    def find_all_elements_by_css_selector(self, css_selector: str) -> list:
        try:
            return self._find_all_elements_by_css_selector(css_selector)
        except Exception as ex:  # noqa: BLE001
            raise WebScraperError from ex

    def press_a_button(self, button: typing.Any) -> None:
        try:
            self._press_a_button(button)
        except Exception as ex:  # noqa: BLE001
            raise WebScraperError from ex

    def _load_web_page(self, url: HttpUrl) -> None:
        raise NotImplementedError

    def _check_dictionary_availability(self) -> bool:
        raise NotImplementedError

    def _find_all_elements_by_css_selector(self, css_selector: str) -> list:
        raise NotImplementedError

    def _press_a_button(self, button: typing.Any) -> None:
        raise NotImplementedError

    def _extract_text_from_elements(self, elements: list) -> list[str]:
        raise NotImplementedError


class SeleniumWebScraper(AbstractWebScraper):
    def __init__(self) -> None:
        self.timeout = AppSettings.web_scraper_timeout

    def __enter__(self) -> typing_extensions.Self:
        super().__enter__()
        chrome_options: Options = Options()
        chrome_options.add_argument("--headless")
        self.driver: WebDriver = webdriver.Chrome(options=chrome_options)
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: types.TracebackType | None,
    ) -> bool | None:
        super().__exit__(exc_type, exc_val, exc_tb)
        self.driver.quit()
        return None

    def _load_web_page(self, url: HttpUrl) -> None:
        self.driver.get(url.unicode_string())

    def _check_dictionary_availability(self) -> bool:
        try:
            WebDriverWait(self.driver, self.timeout).until(
                expected_conditions.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, AppSettings.dictionary_link_css_selector),
                ),
            )
        except TimeoutException:
            return False
        return True

    def _find_all_elements_by_css_selector(self, css_selector: str) -> list:
        WebDriverWait(self.driver, self.timeout).until(
            expected_conditions.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, css_selector),
            ),
        )
        return self.driver.find_elements(By.CSS_SELECTOR, css_selector)

    def _press_a_button(self, button: typing.Any) -> None:
        self.driver.execute_script("arguments[0].scrollIntoView(true);", button)
        self.driver.execute_script("arguments[0].click();", button)

    def _extract_text_from_elements(self, elements: list[WebElement]) -> list[str]:
        return [element.text for element in elements]
