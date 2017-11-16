from google import search
import time
import string
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import youtube_dl

SOURCE= "site:www.youtube.com "
RESULTS_LOCATOR = "//div/h3/a"
printable = set(string.printable)

ydl_opts = {'preferredcodec': 'mp3',
            'extractaudio': True,
            'format': 'bestaudio/best',
            'noplaylist': True}

driver = webdriver.Chrome('C:/Users/Oriel/Downloads/chromedriver.exe')

with open('playlist.txt') as f:
    lines = f.readlines()
for line in lines:
    query = SOURCE + ''.join(filter(lambda x: x in string.printable, line[:-1]))
    print(query)
   # for url in search(query, tld='com', lang='en', start=0, stop=1, num=0):
    print("downloading " + line)

    #retrieving url
    driver.get("http://www.google.com")
    input_element = driver.find_element_by_name("q")
    input_element.send_keys(query)
    input_element.submit()
    WebDriverWait(driver, 10).until(
        EC.visibility_of_element_located((By.XPATH, RESULTS_LOCATOR)))
    page1_results = driver.find_elements(By.XPATH, RESULTS_LOCATOR)
    shouldSkip = False
    for item in page1_results:
        if(shouldSkip):
            break
        url = item.get_attribute("href")
        print("attempting to download from " + url)
        if not('youtube' in url):
            print("url isn't youtube url, skipping")
            continue
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            try:
                ydl.download([url])
                shouldSkip = True
                break
            except ValueError:
                shouldSkip = False
                print("issue with the URL, trying from a different location...")

driver.close()