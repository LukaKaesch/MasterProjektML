import urllib.request
import csv
import time
import os

from resources import ManufacturerGanter, ManufacturerKipp
from resources import DIR_PATH
from selenium import webdriver
from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Globals
SEARCH_TERM = 'Griff'
MANUFACTURER = ManufacturerKipp
MAX_RESULTS_PER_SEARCH_TERM = 30
ITERATION_MAX_FOR_SCROLLING = 100


def start_search(driver):
    driver.get('https://www.traceparts.com/de')
    driver.maximize_window()

    cookie_button = driver.find_element(By.ID, 'didomi-notice-agree-button')
    input_field = driver.find_element(By.ID, 'searchBox')
    search_button = driver.find_element(By.ID, 'search-button')

    cookie_button.click()
    input_field.send_keys(SEARCH_TERM)
    search_button.click()
    mechanical_components_button = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.ID,
                                                                                                   'TRACEPARTS:TP01')))
    driver.execute_script("arguments[0].click();", mechanical_components_button)


def scroll_to_bottom(driver):
    SCROLL_PAUSE_TIME = 1
    ITERATION_COUNTER = 0

    # Get scroll height
    last_height = driver.execute_script("return document.body.scrollHeight")

    while True:
        ITERATION_COUNTER += 1
        if (ITERATION_COUNTER == ITERATION_MAX_FOR_SCROLLING): break
        print('Log: Scrolling ', ITERATION_COUNTER, ' of ', ITERATION_MAX_FOR_SCROLLING)
        try:
            button = driver.find_element(By.ID, 'searchresult-more')
            driver.execute_script("arguments[0].click();", button)

            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(SCROLL_PAUSE_TIME)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                try:
                    button = driver.find_element(By.ID, 'searchresult-more')
                    if not button.is_displayed(): break
                    driver.execute_script("arguments[0].scrollIntoView();", button)
                except NoSuchElementException:
                    break
                driver.execute_script("arguments[0].click();", button)
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            last_height = new_height
        except Exception as e:
            print('Log: Scrolling exception, ' + str(e))
            continue


def select_manufacturers(driver):
    time.sleep(3)
    manufacturer_div = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.XPATH, '//ul[@id="refine'
                                                                                                 '-list"]//li[2]/ul')))
    # Click on selected manufacturer
    checkbox = manufacturer_div.find_element(By.XPATH,
                                             '//label[contains(text(),"' + MANUFACTURER.Name + '")]/preceding::input[1]')
    driver.execute_script("arguments[0].click();", checkbox)


def get_images_and_tables(driver):
    all_results = driver.find_element(By.ID, 'search-results-items').find_elements(By.XPATH, './*')
    iterator = 0

    filtered_results = MANUFACTURER.filter_all_results(MANUFACTURER, all_results)

    for result in filtered_results:
        print('Log: Processing ', iterator, ' of ', len(filtered_results))

        driver.get(result.link)
        # Timer to avoid IP Ban
        time.sleep(3)
        try:
            save_image(driver, str(result.title))
            if check_table_footer(driver):
                select_all_in_table(driver)
            save_table(driver, str(result.title))
        except Exception:
            continue
        if iterator == MAX_RESULTS_PER_SEARCH_TERM:
            break
        iterator += 1


def save_image(driver, title_to_save):
    try:
        image_link = driver.find_element(By.XPATH, '//img[@title="' + MANUFACTURER.Image_Title + '"]').get_attribute('src')
    except NoSuchElementException:
        print('Log: No image found for "' + title_to_save + '" for title: ' + MANUFACTURER.Image_Title)
        return

    # Create folder for technical drawing
    if create_folder(title_to_save):
        urllib.request.urlretrieve(image_link,
                                   'images/' + title_to_save + '/' + title_to_save + '.jpg')


def check_table_footer(driver):
    try:
        check = driver.find_element(By.ID, 'table-1-footer').is_displayed()
    except NoSuchElementException:
        return False
    return check


def create_folder(title):
    try:
        path_search_term = os.path.join(DIR_PATH, 'images/' + title)
        os.mkdir(path_search_term)
        return True
    except Exception:
        print('Log: Folder "' + title + '" already exists.')
        return False


# Save table as csv file
def save_table(driver, title_to_save):
    try:
        table = driver.find_element(By.XPATH, '//div[@id="configuratorSteps"]//div[1]/table')
        path = 'images/' + title_to_save + '/' + title_to_save + '.csv'
        with open(path, 'w', newline='') as csvfile:
            wr = csv.writer(csvfile)
            first_row = table.find_element(By.CSS_SELECTOR, 'tr')
            wr.writerow([d.text for d in first_row.find_elements(By.CSS_SELECTOR, 'th')])
            for row in table.find_elements(By.CSS_SELECTOR, 'tr'):
                wr.writerow([d.text for d in row.find_elements(By.CSS_SELECTOR, 'td')])
    except NoSuchElementException:
        print('Log: No table found for - ' + title_to_save)


# Selects all entries for table on product page
def select_all_in_table(driver):
    try:
        select = driver.find_element(By.XPATH, '//div[@id="table-1-footer"]//div[1]/div[2]/div[1]/div[1]/button')
        driver.execute_script("arguments[0].click();", select)

        WebDriverWait(driver, 10).until(
            EC.visibility_of_element_located((By.XPATH, '//div[@id="table-1-footer"]//div[1]/div[2]/div[1]/div['
                                                        '1]/ul')))
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight/3);")
        time.sleep(1)

        WebDriverWait(driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, '//div[@id="table-1-footer"]//div[1]/div[2]/div[1]/div['
                                                  '1]/ul/li[4]'))).click()
    except (TimeoutException, NoSuchElementException):
        return


# Configuration
DRIVER_PATH = 'geckodriver'
options = Options()
options.headless = False
options.binary_location = r'C:\Program Files\Mozilla Firefox\firefox.exe'
caps = webdriver.DesiredCapabilities().FIREFOX
caps["marionette"] = True
driver = webdriver.Firefox(options=options, capabilities=caps, executable_path=DRIVER_PATH)

# Main flow
start_search(driver)
select_manufacturers(driver)
scroll_to_bottom(driver)
get_images_and_tables(driver)
