import os
import logging
import datetime
import argparse
from time import sleep
import random
import pandas as pd

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from .utils import init_driver, pop_up2_parent_level, reattach_gblb, get_bulei_list_of_btns, \
    open_sidebar, download

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
    # Store the ID of the original window
    original_window = driver.current_window_handle
    sleep(random.uniform(wait - 1.5, wait + 0.5))
    # logger.info(driver.page_source)

    # Setup wait for later
    dwait = WebDriverWait(driver, 10)

    try:
        open_sidebar(driver)

        sleep(random.uniform(wait - 0.5, wait + 0.5))
        # logger.info(card_by_bulei.get_attribute('innerHTML'))
        l1_bulei_list_of_btns = get_bulei_list_of_btns(driver)

        # These are all the `bulei`` at level 1 (23, in total)
        logger.info(f"len(l1_bulei_list_of_btns): {len(l1_bulei_list_of_btns)}")
        need_reopen_sidebar: bool = False

        for l1_idx, l1_btn in enumerate(l1_bulei_list_of_btns):
            try:
                logger.info(f"Now at l1, idx: {l1_idx}")

                # Reattach to l1 WebElement
                sleep(random.uniform(wait + 1.5, wait + 2.5))
                l1_bulei_list_of_btns = reattach_gblb(driver)
                sleep(random.uniform(wait + 1.5, wait + 2.5))
                l1_btn = l1_bulei_list_of_btns[l1_idx]

                l1_btn.click()

                sleep(random.uniform(wait + 1.5, wait + 2.5))
                l2_bulei_list_of_btns = get_bulei_list_of_btns(driver)

                # if `glyphicon glyphicon-folder-open` -> go to next level
                # elif `glyphicon glyphicon-file` -> download
                #   if not end -> next one
                #   elif end -> pop up to parent level
                for l2_idx, l2_btn in enumerate(l2_bulei_list_of_btns):
                    try:
                        logger.info(f"Now at l2, idx: {l2_idx}")

                        if need_reopen_sidebar:
                            open_sidebar(driver)
                            need_reopen_sidebar = False

                        # Reattach to l1 WebElement
                        sleep(random.uniform(wait + 1.5, wait + 2.5))
                        l2_bulei_list_of_btns = reattach_gblb(driver)
                        sleep(random.uniform(wait + 1.5, wait + 2.5))
                        l2_btn = l2_bulei_list_of_btns[l2_idx]

                        l2_span = l2_btn.find_element(
                            by=By.TAG_NAME,
                            value='span'
                        )
                        sleep(random.uniform(wait - 2.5, wait))
                        l2_btn_type = l2_span.get_attribute("class")
                        logger.info(f"l2_btn_type: {l2_btn_type}")

                        if "folder" in str(l2_btn_type):
                            logger.info("Going to next level from l2...")

                            l2_btn.click()

                            sleep(random.uniform(wait + 1.5, wait + 2.5))
                            l3_bulei_list_of_btns = get_bulei_list_of_btns(driver)

                            for l3_idx, l3_btn in enumerate(l3_bulei_list_of_btns):
                                try:
                                    logger.info(f"Now at l3, idx: {l3_idx}")

                                    if need_reopen_sidebar:
                                        open_sidebar(driver)
                                        need_reopen_sidebar = False

                                    # Reattach to l1 WebElement
                                    sleep(random.uniform(wait + 1.5, wait + 2.5))
                                    l3_bulei_list_of_btns = reattach_gblb(driver)
                                    sleep(random.uniform(wait + 1.5, wait + 2.5))
                                    l3_btn = l3_bulei_list_of_btns[l3_idx]

                                    l3_span = l3_btn.find_element(
                                        by=By.TAG_NAME,
                                        value='span'
                                    )
                                    sleep(random.uniform(wait - 2.5, wait))
                                    l3_btn_type = l3_span.get_attribute("class")
                                    logger.info(f"l3_btn_type: {l3_btn_type}")

                                    if "folder" in str(l3_btn_type):
                                        logger.info("Going to next level from l3...")

                                        l3_btn.click()

                                        sleep(random.uniform(wait + 1.5, wait + 2.5))
                                        l4_bulei_list_of_btns = get_bulei_list_of_btns(driver)

                                        for l4_idx, l4_btn in enumerate(l4_bulei_list_of_btns):
                                            try:
                                                logger.info(f"Now at l4, idx: {l4_idx}")

                                                if need_reopen_sidebar:
                                                    open_sidebar(driver)
                                                    need_reopen_sidebar = False

                                                # Reattach to l4 WebElement
                                                sleep(random.uniform(wait + 1.5, wait + 2.5))
                                                l4_bulei_list_of_btns = reattach_gblb(driver)
                                                sleep(random.uniform(wait + 1.5, wait + 2.5))
                                                l4_btn = l4_bulei_list_of_btns[l4_idx]

                                                l4_span = l4_btn.find_element(
                                                    by=By.TAG_NAME,
                                                    value='span'
                                                )
                                                sleep(random.uniform(wait - 2.5, wait))
                                                l4_btn_type = l4_span.get_attribute("class")
                                                logger.info(f"l4_btn_type: {l4_btn_type}")

                                                if "file" in str(l4_btn_type):
                                                    logger.info("Going to a new page to download...")
                                                    need_reopen_sidebar = True
                                                    l4_btn.click()

                                                    dwait.until(EC.number_of_windows_to_be(2))
                                                    download(driver, original_window)

                                                if l4_idx == 0:
                                                    logger.info("l4 finished, pop up to parent level...\n")

                                                    if need_reopen_sidebar:
                                                        open_sidebar(driver)
                                                        need_reopen_sidebar = False

                                                    pop_up2_parent_level(driver)
                                            except Exception:
                                                continue
                                    else:
                                        logger.info("Going to a new page to download...")
                                        need_reopen_sidebar = True
                                        l3_btn.click()

                                        dwait.until(EC.number_of_windows_to_be(2))
                                        download(driver, original_window)

                                    if l3_idx == len(l3_bulei_list_of_btns) - 1:
                                        logger.info("l3 finished, pop up to parent level...\n")

                                        if need_reopen_sidebar:
                                            open_sidebar(driver)
                                            need_reopen_sidebar = False

                                        pop_up2_parent_level(driver)
                                except Exception:
                                    continue
                        else:
                            logger.info("Going to a new page to download...")
                            need_reopen_sidebar = True
                            l2_btn.click()

                            dwait.until(EC.number_of_windows_to_be(2))
                            download(driver, original_window)

                        if l2_idx == len(l2_bulei_list_of_btns) - 1:
                            logger.info("l2 finished, pop up to parent level...\n")

                            if need_reopen_sidebar:
                                open_sidebar(driver)
                                need_reopen_sidebar = False

                            pop_up2_parent_level(driver)
                    except Exception:
                        continue
            except Exception:
                continue
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
