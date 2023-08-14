import json
import re
from time import sleep

import logging


# https://realpython.com/python-logging/#the-logging-module
logging.basicConfig(level=logging.INFO, filename='output/extract_link_script.log', filemode='w', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')


from selenium.webdriver import Firefox, Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options as FireFoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
from tqdm import tqdm


def make_driver(type='firefox'):
    """Creates headless Firefox WebDriver instance."""
    if type == 'chrome':
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')
        return Chrome(options=chrome_options)
    elif type == 'firefox':
        firefox_options = FireFoxOptions()
        firefox_options.add_argument('-headless')
        return Firefox(options=firefox_options)
    else:
        raise ValueError(f"Invalid driver type: {type}")

browser = 'firefox'
#browser = 'chrome'

driver = make_driver(browser) # create driver instance
page = "https://www.ycombinator.com/companies" # page to scrape


def compile_batches():
    """Returns elements of checkboxes from all batches."""
    pattern = re.compile(r'^(W|S|IK)[012]')
    bx = driver.find_elements(By.XPATH, '//label')
    for element in bx:
        if pattern.match(element.text):
            yield element


def scroll_to_bottom():
    """Scrolls to the bottom of the page."""

    # get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        # scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")

        # wait to load page
        sleep(3)

        # calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height


def fetch_url_paths():
    """Returns a generator with url paths for all companies."""
    # contains 'companies' but not 'founders'
    elements = driver.find_elements(
        By.XPATH, ('//a[contains(@href,"/companies/") and not(contains(@href,"founders"))]'))
    for url in elements:
        yield url.get_attribute('href')


def write_urls_to_file(ul: list):
    """Appends a list of company urls to a file."""
    with open('output/start_urls.txt', 'w') as f:
        json.dump(ul, f)


def yc_links_extractor():
    """Run the main script to write all start urls to a file."""
    logging.info("Starting yc_links_extractor.py")
    logging.info(f"Using {browser} driver.")
    logging.info(f"Attempting to scrape links from {page}.")

    # Selenium code: https://www.selenium.dev/documentation/webdriver/getting_started/first_script/

    logging.info(f"Navigating to {page}...")
    driver.get(page)

    logging.info("Waiting for page to load...")
    driver.implicitly_wait(0.5)
    
    # Finders documentation: https://www.selenium.dev/documentation/webdriver/elements/finders/

    logging.info("Finding 'select_all_options' for 'Batch'...")
    see_all_options = driver.find_element(By.CLASS_NAME, "wFMmHIyWKCYOnrsVb3Yq")
    
    logging.info("Clicking 'select_all_options' for 'Batch'...")
    see_all_options.click()

    logging.info("Compiling batches...")        
    batches = list(compile_batches()) # Since compile_batches() is a generator, we need to convert it to a list

    
    logging.info(f"Found {len(batches)} batches.")
           
    ulist = [] # list of list of urls for all batches

    # TQDM Progress Bar: https://github.com/tqdm/tqdm

    for b in tqdm(list(batches)):
        logging.info(f"Checking batch: {b.text}")
        b.click()
        
        logging.info("Scrolling to bottom of page...")
        scroll_to_bottom()

        logging.info("Fetching links and appending to ulist")
        urls = [u for u in fetch_url_paths()] # list of urls for current batch
        ulist.extend(urls)

        logging.info("Unchecking batch: {b.text}")
        b.click()
    
    logging.info("Writing urls to file...")
    write_urls_to_file(ulist)
    logging.info(f"Done. Wrote {len(ulist)} urls to file.")
    logging.info("Done.")

    logging.info("Closing driver...")
    driver.quit()


if __name__ == '__main__':
    yc_links_extractor()
