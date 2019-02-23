from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
import random
import csv
import time
opts = Options()
ua = UserAgent()
userAgent = ua.random
opts.add_argument(f'user-agent={userAgent}')
driver = Chrome(options=opts)

#driver.quit()
cats = set()
page = 1

while (True):
    driver.get("https://www.cryptokitties.co/search/" + str(page) + "?include=sale&orderBy=purr_count")
    while (len(driver.find_elements_by_class_name("KittyCard-main-container")) == 0):
        time.sleep(1)
    kittyGridItems = driver.find_elements_by_class_name("KittiesGrid-item")
    cats = set()
    for kitty in kittyGridItems:
        children = kitty.find_elements_by_css_selector("*")
        print(children[0].get_attribute("href"))
        cats.add(children[0].get_attribute("href"))
        
    with open('catLinks.txt', mode='a') as csv_file:
        w = csv.writer(csv_file, delimiter=',')
        for link in cats:
            w.writerow([link])
        csv_file.close()
    time.sleep(random.randint(5, 10))
    page += 1
    
    
               
