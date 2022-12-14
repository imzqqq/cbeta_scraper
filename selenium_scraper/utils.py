import os
import yaml
import logging
import logging.config
from time import sleep
import random
import chromedriver_autoinstaller
import geckodriver_autoinstaller
from selenium.common.exceptions import NoSuchElementException
from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

logger = logging.getLogger(__name__)


def init_driver(
    *, headless: bool = True, proxy=None, show_images=False, option=None, firefox=False
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


def pop_up2_parent_level(driver):
    sleep(random.uniform(3 - 0.5, 3 + 0.5))
    pop_up_btn = WebDriverWait(driver=driver, timeout=5).until(
        lambda x: x.find_element(
            by=By.ID,
            value='selector-levels-back-btn'
        )
    )
    pop_up_btn.click()
    logger.info("Popped up to parent level\n")
    sleep(random.uniform(3 - 0.5, 3 + 0.5))


def get_bulei_list_of_btns(driver):
    l_card_by_bulei = WebDriverWait(driver=driver, timeout=10).until(
        lambda x: x.find_element(
            by=By.ID,
            value='selector-levels'
        )
    )
    sleep(random.uniform(3 - 1.5, 3))
    l_bulei_list_of_btns = WebDriverWait(driver=l_card_by_bulei, timeout=10).until(
        lambda x: x.find_elements(
            by=By.TAG_NAME,
            value='button'
        )
    )
    sleep(random.uniform(3 - 1.5, 3 + 0.5))
    return l_bulei_list_of_btns


def reattach_gblb(driver):
    l_card_by_bulei = WebDriverWait(driver=driver, timeout=20).until(
        lambda x: x.find_element(
            by=By.ID,
            value='selector-levels'
        )
    )
    sleep(random.uniform(3 + 1.5, 3 + 2.5))
    # logger.info(card_by_bulei.get_attribute('innerHTML'))
    l_bulei_list_of_btns = WebDriverWait(driver=l_card_by_bulei, timeout=20).until(
        lambda x: x.find_elements(
            by=By.TAG_NAME,
            value='button'
        )
    )
    return l_bulei_list_of_btns


def download(driver, original_window):
    # Loop through until we find a new window handle
    for window_handle in driver.window_handles:
        if window_handle != original_window:
            driver.switch_to.window(window_handle)

    sleep(random.uniform(3 + 1.5, 3 + 2.5))
    download_btn = driver.find_element(
        by=By.ID,
        value='jing_export_modal_btn'
    )
    # print(download_btn)
    download_btn.click()
    sleep(random.uniform(3 + 1.5, 3 + 2.5))

    driver.find_element(
        by=By.XPATH,
        value='//input[@value="txt"]'
    ).click()
    driver.find_element(
        by=By.XPATH,
        value='//input[@value="all"]'
    ).click()
    driver.find_element(
        by=By.ID,
        value='jing_export_btn'
    ).click()
    sleep(random.uniform(0.5, 0.6))
    driver.close()
    driver.switch_to.window(original_window)


def open_sidebar(driver):
    btn_choose_scripture = WebDriverWait(driver=driver, timeout=5).until(
        lambda x: x.find_element(
            by=By.XPATH,
            value='//img[contains(@id, "open_jing_selector_btn")]'
        )
    )
    btn_choose_scripture.click()


def setup_logging(
    config_path: str = 'logging.yml',
    default_level=logging.INFO
) -> None:
    if os.path.exists(config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            logging.info("Successfully loaded logging.yml configurations")
            log_config = yaml.safe_load(f)
    else:
        log_config = False
        logging.basicConfig(level=default_level)

    if not log_config:
        logging.warning("Loaded a blank logging config?")

    logging.config.dictConfig(log_config)
