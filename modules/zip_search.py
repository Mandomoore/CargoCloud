from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time



def find_zip_codes(zipcode, miles):
    #Browser Options
    driver_options = Options()
    driver_options.add_argument('--headless')
    driver = webdriver.Chrome(options=driver_options)
    # Initialize Browser
    driver.get('https://www.freemaptools.com/find-zip-codes-inside-radius.htm#google_vignette')
    time.sleep(5)

    # Identify Elements
    input_miles = driver.find_element("xpath", "/html/body/div[2]/div[2]/div[5]/p[1]/input[2]")
    input_zip = driver.find_element("xpath", "/html/body/div[2]/div[2]/div[5]/div[1]/center/div/input")
    search_button = driver.find_element("id", "locationSearchButton")
    textarea_element = driver.find_element("xpath", "/html/body/div[2]/div[2]/div[5]/center[3]/textarea")
    time.sleep(1)

    # Input Data & Search
    input_miles.clear()
    input_miles.send_keys(miles)
    input_zip.send_keys(zipcode)
    search_button.click()
    time.sleep(5)

    # Retrieve data from textarea
    returned_zips = textarea_element.get_attribute("value")
    return returned_zips
