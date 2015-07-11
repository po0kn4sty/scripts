from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
import time
import csv
import sys
import pickle
import re

driver = webdriver.Firefox()
driver.implicitly_wait(10)  
driver.get('https://maps.gis.ca.gov/boe/TaxRates/')
address = driver.find_element_by_id("Textaddress")
city = driver.find_element_by_id("Textcity")
zipcode = driver.find_element_by_id("TextZip")
submit_button = driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/div/div[1]/div[1]/button')
ratefile = open("taxrates.pickle", "r+")
fails = []
# print sys.argv()
# street_address = re.compile(u'\d{1,4}[\w\s]{1,20}(?:street|st|avenue|ave|road|rd|highway|hwy|square|sq|trail|trl|drive|dr|court|ct|parkway|pkwy|circle|cir|boulevard|blvd|lane|ln)\W?(?=\s|$)', re.IGNORECASE)

try:
    taxratemap = pickle.load(ratefile)
except IOError as e:
    taxratemap = {}
except EOFError as e:
    taxratemap = {}

pattern = re.compile('(^[a-z]+\s(?=[0-9]+)|#.+$|(?<= st ).+|(?<= ave ).+|(?<= rd ).+|(?<= blvd ).+|(?<= dr ).+|(?<= boulevard ).+|(?<= drive ).+|(?<= street ).+|(?<= road ).+|(?<= avenue ).+|[^a-zA-Z0-9 ]+)', re.UNICODE)
# new_pattern = re.compile('(^[a-z]+\s(?=[0-9]+)|#.+$|(?<= boulevard ).+|(?<= parkway|highway ).+|(?<= square|circle ).+|(?<= street|avenue ).+|(?<= drive|court ).+|(?<= trail ).+|(?<= blvd|pkwy ).+|(?<= road ).+|(?<= hwy|ave ).+|(?<= trl|cir ).+|(?<= way ).+|(?<= rd|st ).+|(?<= sq|dr ).+|(?<= ct|tr ).+|[^a-zA-Z0-9 ]+)', re.UNICODE)
with open('EtsySoldOrders2015.csv', 'r') as ordercsvfile:
    xclreader = csv.reader(ordercsvfile)
    for row in xclreader:
        if row[12].lower().strip() == 'ca':
            pre_addr = (row[9] + " " + row[10]).lower()
            addr_input = re.sub(new_pattern, '', pre_addr).strip()
            city_input = row[11].lower().strip()
            zip_input = row[13].lower().strip()
            key_ = (addr_input, city_input, zip_input)
            if taxratemap.get(key_) is None:
                address.clear()
                city.clear()
                zipcode.clear()
                address.send_keys(addr_input)
                city.send_keys(city_input)
                zipcode.send_keys(zip_input)
                submit_button.click()
                element = driver.find_element_by_xpath('//*[@id="RateVal"]')
                time.sleep(10)
                rate = element.text.strip('%')
                
                try:
                    taxratemap[key_] = float(rate) / 100.0
                except Exception as e:
                    fails.append(key_)
            else:
                rate = taxratemap[key_]


        # Do the computations YO!


print(fails)
print(len(taxratemap))
pickle.dump(taxratemap, ratefile, 2)
driver.close()
            








