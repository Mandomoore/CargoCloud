from selenium import webdriver
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from selenium.webdriver.chrome.options import Options as ChromeOptions
import time

def find_zip_codes(zipcode, miles):
    try:
        # Try Chrome as a fallback
        chrome_options = ChromeOptions()
        chrome_options.add_argument('--headless')
        driver = webdriver.Chrome(options=chrome_options)

        print("Chrome is the default browser.")
    except Exception as chrome_exception:
        print(f"Error with Chrome: {str(chrome_exception)}")

        try:
            # Try Firefox
            firefox_options = FirefoxOptions()
            firefox_options.headless = True
            driver = webdriver.Firefox(options=firefox_options)
            print("Firefox is the fallback browser.")

        except Exception as chrome_exception:
            print(f"Error with Chrome: {str(chrome_exception)}")
            raise Exception("Failed to initialize Firefox and Chrome")

    try:
        # Rest of your script...
        driver.get('https://www.freemaptools.com/find-zip-codes-inside-radius.htm#google_vignette')
        time.sleep(1)

        # Identify Elements
        input_miles = driver.find_element("xpath", "/html/body/div[2]/div[2]/div[5]/p[1]/input[2]")
        input_zip = driver.find_element("xpath", "/html/body/div[2]/div[2]/div[5]/div[1]/center/div/input")
        searchbutton = driver.find_element("id", "locationSearchButton")
        textarea_element = driver.find_element("xpath", "/html/body/div[2]/div[2]/div[5]/center[3]/textarea")
        time.sleep(1)

        # Input Data & Search
        input_miles.clear()
        input_miles.send_keys(miles)
        input_zip.send_keys(zipcode)
        searchbutton.click()
        time.sleep(1)

        # Retrieve data from textarea
        returned_zips = textarea_element.get_attribute("value")
        return returned_zips

    finally:
        if 'driver' in locals():
            driver.quit()

print(find_zip_codes(90210, 15))


