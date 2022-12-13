import logging
import chromedriver_autoinstaller
import geckodriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait

logger = logging.getLogger(__name__)


def init_driver(
    headless: bool = True, proxy=None, show_images=False, option=None, firefox=False
):
    """ Initiate a chromedriver or firefoxdriver instance
        --option : other option to add (str)
    """

    if firefox:
        options = FirefoxOptions()
        driver_path = geckodriver_autoinstaller.install()
    else:
        options = ChromeOptions()
        driver_path = chromedriver_autoinstaller.install()

    if headless is True:
        logger.info("Scraping in headless mode...")
        options.add_argument('--disable-gpu')
        options.headless = True
    else:
        options.headless = False

    # options.add_argument('--no-sandbox')
    # options.add_argument('--disable-dev-shm-usage')
    options.add_experimental_option(
        "excludeSwitches", ["enable-logging"]
    )
    options.add_argument('log-level=3')

    if proxy is not None:
        options.add_argument('--proxy-server=%s' % proxy)
        logger.info("Using proxy : ", proxy)

    if show_images is False and firefox is False:
        prefs = {"profile.managed_default_content_settings.images": 2}
        options.add_experimental_option("prefs", prefs)

    if option is not None:
        options.add_argument(option)

    if firefox:
        driver = webdriver.Firefox(options=options, executable_path=driver_path)
    else:
        driver = webdriver.Chrome(options=options, executable_path=driver_path)

    driver.set_page_load_timeout(100)
    return driver


def check_exists_by_link_text(text, driver):
    try:
        driver.find_element(By.LINK_TEXT, text)
    except NoSuchElementException:
        return False

    return True


def check_exists_by_xpath(xpath, driver):
    # timeout = 3
    try:
        driver.find_element(by=By.XPATH, value=xpath)
    except NoSuchElementException:
        return False

    return True


def close_notification_dialog(driver):
    try:
        WebDriverWait(driver=driver, timeout=3).until(
            lambda x: x.find_element(
                By.XPATH,
                '//div[contains(@data-testid, "app-bar-close")]'
            ).click()
        )
    except Exception:
        logger.info("No need to close notification settings dialog")

    try:
        sheetDialog = WebDriverWait(driver=driver, timeout=1).until(
            lambda x: x.find_element(
                By.XPATH,
                '//div[contains(@data-testid, "sheetDialog")]'
            )
        )
        sheetDialog.find_element(
            By.LINK_TEXT,
            'Not Now'
        ).click()
    except Exception:
        logger.info("No need to close notification settings dialog")
