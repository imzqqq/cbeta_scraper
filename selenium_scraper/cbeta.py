import os
import logging
import datetime
import argparse
from time import sleep
import random
import pandas as pd

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .utils import init_driver, pop_up2_parent_level, reattach_to_l1, get_bulei_list_of_btns

logger = logging.getLogger(__name__)


def scrape(
    wait: int = 3, headless: bool = False, resume: bool = True, save_dir: str = "outputs"
):
    """
    Scrape data from CBETA using requests

    return:
    """

    write_mode = 'w'

    # Create the <save_dir>
    if not os.path.exists(save_dir):
        os.makedirs(save_dir)

    # Initiate the driver
    driver = init_driver(headless=False, show_images=True)

    driver.get("https://cbetaonline.cn/zh/")
    sleep(random.uniform(wait - 1.5, wait + 0.5))
    # logger.info(driver.page_source)

    try:
        btn_choose_scripture = WebDriverWait(driver=driver, timeout=5).until(
            lambda x: x.find_element(
                by=By.XPATH,
                value='//img[contains(@id, "open_jing_selector_btn")]'
            )
        )
        btn_choose_scripture.click()
        sleep(random.uniform(wait - 0.5, wait + 0.5))

        l1_bulei_list_of_btns = get_bulei_list_of_btns(driver)

        # These are all the `bulei`` at level 1 (23, in total)
        logger.info(f"len(l1_bulei_list_of_btns): {len(l1_bulei_list_of_btns)}")
        # l1_bulei_cur_pos = 1
        # l1_bulei_counts = len(l1_bulei_list_of_btns)

        for l1_idx, l1_btn in enumerate(l1_bulei_list_of_btns):
            logger.info(f"Now at l1, idx: {l1_idx}")

            # Reattach to l1 WebElement
            l1_bulei_list_of_btns = reattach_to_l1(driver)
            sleep(random.uniform(wait - 1.5, wait + 0.5))
            l1_btn = l1_bulei_list_of_btns[l1_idx]

            l1_btn.click()

            l2_bulei_list_of_btns = get_bulei_list_of_btns(driver)

            # if `glyphicon glyphicon-folder-open` -> go to next level
            # elif `glyphicon glyphicon-file` -> download
            #   if not end -> next one
            #   elif end -> pop up to parent level
            for l2_idx, l2_btn in enumerate(l2_bulei_list_of_btns):
                logger.info(f"Now at l2, idx: {l2_idx}")
                l2_span = l2_btn.find_element(
                    by=By.TAG_NAME,
                    value='span'
                )
                sleep(random.uniform(wait - 2.5, wait))
                l2_btn_type = l2_span.get_attribute("class")
                logger.info(f"l2_btn_type: {l2_btn_type}")

                if "folder" in str(l2_btn_type):
                    logger.info("Going to next level from l2...")
                    # l2_btn.click()
                else:
                    logger.info("Going to a new page to download...")

                if l2_idx == len(l2_bulei_list_of_btns) - 1:
                    logger.info("l2 finished, pop up to parent level...\n")
                    pop_up2_parent_level(driver)

    except Exception as e:
        logger.info(e)

    # Resume scraping from previous work
    if resume:
        write_mode = 'a'  # noqa

    sleep(random.uniform(wait - 0.5, wait + 0.5))
    # Close the web driver
    driver.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Scraper for CBETA.')

    parser.add_argument(
        '--headless',
        type=bool,
        help='Headless webdrivers or not. True or False',
        default=False
    )
    parser.add_argument(
        '--resume',
        type=bool,
        help='Resume at the last scraping, specify the csv file path.',
        default=False
    )

    args = parser.parse_args()

    headless = args.headless
    resume = args.resume

    data = scrape(headless=headless, resume=resume)
