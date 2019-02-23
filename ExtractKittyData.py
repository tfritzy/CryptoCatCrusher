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

def writeBasicCatRow(cat, file):
    with open(file, mode='a') as csv_file:
        r = csv.writer(csv_file, delimiter=',',lineterminator='\n')
        row = catDictToArray(cat)
        r.writerow(row)
        print("Wrote cat: " + str(cat))
        csv_file.close()

def waitForBidPageToOpen():
    kittyBidWaitCount = 0
    while(len(driver.find_elements_by_class_name("KittyBid")) == 0):
        time.sleep(1)
        kittyBidWaitCount += 1
        if (kittyBidWaitCount == 10):
            return False
    return True

def catDictToArray(cat):
    print(cat.__class__)
    row = []
    row.append(cat['price'])
    row.append(cat['id'])
    row.append(cat['eye colour'])
    row.append(cat['fur'])
    row.append(cat['pattern'])
    row.append(cat['eye shape'])
    row.append(cat['accent colour'])
    row.append(cat['highlight colour'])
    row.append(cat['mouth'])
    row.append(cat['base colour'])
    if ("wild element" in cat):
        row.append(cat['wild element'])
    else:
        row.append("")
    row.append(cat['likes'])
    row.append(cat['cooldown'])
    row.append(cat['generation'])
    return row
    
def getCatFromID(catID):
    cat = {}
    cat['id'] = catID

    driver.get("https://www.cryptokitties.co/kitty/" + catID)

    waitForBidPageToOpen()

    
    specialBadge = driver.find_elements_by_class_name("SpecialBadge-title")
    if (len(specialBadge) > 0):
        return None
    
    cattributes = driver.find_elements_by_class_name("Cattribute-content")
    for cattribute in cattributes:
        children = cattribute.find_elements_by_css_selector("*")
        cattributeType = ""
        cattributeTitle = ""
        for child in children:
            if (child.get_attribute("class") == "Cattribute-type"):
                cattributeType = child.text
            elif (child.get_attribute("class") == "Cattribute-title"):
                cattributeTitle = child.text
            if (cattributeTitle == "" or cattributeType == ""):
                continue
            cat[cattributeType] = cattributeTitle
    generationBox = driver.find_element_by_class_name("KittyHeader-details-generation")
    genText = generationBox.text
    cat['generation'] = genText.split(" ")[1]
    likeBox = driver.find_element_by_class_name("PurrButton-count")
    cat['likes'] = likeBox.text
    priceBox = driver.find_elements_by_class_name("KittyBid-box-subtitle")
    if (len(priceBox) > 0):
        cat['price'] = float(priceBox[0].text.split(" ")[1])
    else:
        cat['price'] = str(-1)
    reproduceSpeedBox = driver.find_element_by_class_name("KittyHeader-details-condition")
    cat['cooldown'] = reproduceSpeedBox.text
            
    #writeBasicCatRow(cat)
    #print ("wrote cat: " + str(cat))
    return cat
    #time.sleep(2)
    


if __name__ == "__main__":

    alreadyWritten = set()
    with open('cats.csv', mode='r') as csv_file:
        r = csv.reader(csv_file, delimiter=',',lineterminator='\n')
        for row in r:
            alreadyWritten.add(row[1])
    links = set()

    with open('links.txt', mode='r') as csv_file:
        r = csv.reader(csv_file, delimiter=',')
        for row in r:
            if (len(row) > 0):
                links.add(row[0])

        csv_file.close()

    linkCounter = 0;


    for link in links:
        splitLink = link.split("/")
        catID = splitLink[len(splitLink)-1]
        if (catID in alreadyWritten):
            print("already wrote cat with id: " + str(catID))
            continue
        else:
            alreadyWritten.add(catID)
            
        cat = getCatFromID(catID)
        print(cat)
        if (cat == None):
            continue
        writeBasicCatRow(cat)


        

    
