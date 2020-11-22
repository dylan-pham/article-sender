from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
from bs4 import BeautifulSoup
import os
import plistlib

# getting urls in ios reading list
INPUT_FILE  = os.path.join(os.environ['HOME'], 'Library/Safari/Bookmarks.plist')

# Load and parse the Bookmarks file
with open(INPUT_FILE, 'rb') as plist_file:
    plist = plistlib.load(plist_file)

# Look for the child node which contains the Reading List data.
# There should only be one Reading List item
children = plist['Children']
for child in children:
    if child.get('Title', None) == 'com.apple.ReadingList':
        reading_list = child

# Extract the bookmarks
bookmarks = reading_list['Children']

# For each bookmark in the bookmark list, grab the URL
rl_urls = [bookmark['URLString'] for bookmark in bookmarks]

# --------------------------------------------------------------------------------

# getting articles purportedly on kindle cloud library (kept track of locally)

kindle_urls = []
with open("/Users/dpham/Development/Applications/article-sender/kindle_urls.txt", "r") as f:
    for line in f:
        kindle_urls.append(line.strip())

print(kindle_urls)
print(rl_urls)

# --------------------------------------------------------------------------------

# sending new articles to kindle
options = Options()
options.headless = True
browser = webdriver.Chrome(options=options)

base_url = "https://pushtokindle.fivefilters.org/send.php?src=safari-app&url="
browser.get(base_url + "https://google.com")
time.sleep(2)
browser.find_element_by_xpath(r'//*[@id="contentIdForA11y3"]/div/div[4]/div/input').send_keys("khoikindle@kindle.com")
time.sleep(2)
browser.find_element_by_xpath(r'//*[@id="contentIdForA11y3"]/div/div[5]/div/input').send_keys("43.dpham@gmail.com")

for url in rl_urls:
    if url not in kindle_urls:
        with open("/Users/dpham/Development/Applications/article-sender/kindle_urls.txt", "a") as f:
            f.write(url + "\n")
        print(url)
        browser.get(base_url + url)
        time.sleep(5)
        send_button = browser.find_element_by_xpath(r'//*[@id="app"]/div[1]/div[2]/div[2]/button')
        browser.execute_script("arguments[0].click();", send_button)
        time.sleep(5)

browser.quit()
