import os
import datetime
import argparse
from time import sleep
import random
import pandas as pd
from selenium.webdriver.support.ui import WebDriverWait

from .utils import init_driver, log_search_page, keep_scrolling


def scrape(
    headless: bool = True, resume: bool = True, save_dir: str = "outputs"
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
    driver = init_driver(headless)

    driver.get("https://cbetaonline.cn/zh/")

    # Resume scraping from previous work
    if resume:
        write_mode = 'a'

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
