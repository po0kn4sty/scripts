#! /usr/local/bin/python

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from subprocess import call
import time
import csv
import sys
import pickle
import re
import os

# Filenames
rate_file_name = "../resources/tax_rates/taxrates.pickle"
order_file_name = "../resources/tax_rates/EtsySoldOrders2015.csv"
shipping_file_name = "../resources/tax_rates/EtsyShippingLabels-2015.csv"
output_file_name = "EtsyTaxes.csv"

# Option to reset the taxrate mapping 
if (len(sys.argv) > 1):
    if (sys.argv[1].lower() == 'reset'):
        rate_abs_path = os.path.abspath(rate_file_name)
        try:
            os.remove(rate_abs_path)
        except OSError as e:
            pass
        with open(rate_abs_path, 'w') as _:
            pass 
    else:
        print("Error: invalid argument")
        sys.exit(-1)

# Selenium Setup
driver = webdriver.Firefox()
driver.implicitly_wait(10)  
driver.get('https://maps.gis.ca.gov/boe/TaxRates/')
address = driver.find_element_by_id("Textaddress")
city = driver.find_element_by_id("Textcity")
zipcode = driver.find_element_by_id("TextZip")
submit_button = driver.find_element_by_xpath('/html/body/form/div[3]/div[2]/div/div[1]/div[1]/button')

# I / O Files
rate_file = open(rate_file_name, "r+")
output_file = open(output_file_name, 'w')
xclwriter = csv.writer(output_file)

# Data Structures
fails = []
output_vectors = {}

# Attempt to load taxratemap from file
try:
    taxratemap = pickle.load(rate_file)
except IOError as e:
    taxratemap = {}
except EOFError as e:
    taxratemap = {}

def rate_val_present(driver):
  element = driver.find_element_by_xpath('//*[@id="RateVal"]')
  return bool(element.text)

# Lookup Taxrates 
pattern = re.compile('(^[a-z]+\s(?=[0-9]+)|#.+$|(?<= st ).+|(?<= ave ).+|(?<= rd ).+|(?<= blvd ).+|(?<= dr ).+|(?<= boulevard ).+|(?<= drive ).+|(?<= street ).+|(?<= road ).+|(?<= avenue ).+|[^a-zA-Z0-9 ]+)', re.UNICODE)
with open(order_file_name, 'r') as ordercsvfile:
    xclreader = csv.reader(ordercsvfile)
    EtsyFormat = xclreader.next()
    for row in xclreader:
        output_vectors[row[1]] = [0 for _ in range(42)]
        vector = output_vectors[row[1]]
        vector[0] = row[1]
        vector[2] = row[0]
        vector[5] = row[2]
        vector[6] = row[3]
        vector[7] = row[4]
        vector[8] = row[5]
        vector[9] = row[6]
        vector[10] = row[7]
        vector[11] = row[9]
        vector[12] = row[10]
        vector[13] = row[11]
        vector[14] = row[12]
        vector[15] = row[13]
        vector[16] = row[14]
        vector[17] = row[15]
        vector[19] = row[16]
        vector[20] = row[17]
        vector[21] = row[18]
        vector[22] = row[21]
        vector[23] = row[22]
        vector[26] = row[19]
        vector[32] = row[23]
        vector[33] = row[24]
        vector[34] = row[25]
        vector[35] = row[26]
        vector[36] = row[27]
        vector[37] = row[28]
        vector[38] = row[29]
        vector[39] = row[30]
        vector[40] = row[31]
        vector[41] = row[32]
        vector[24] = float(row[21]) - float(row[19])

        if row[12].lower().strip() == 'ca':
            pre_addr = (row[9] + " " + row[10]).lower()
            addr_input = re.sub(pattern, '', pre_addr).strip()
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
                # time.sleep(1)
                try:
                    unused = WebDriverWait(driver, 20).until(rate_val_present)
                    element = driver.find_element_by_xpath('//*[@id="RateVal"]')
                    rate = element.text.strip('%').strip()
                    taxratemap[key_] = float(rate) / 100.0
                    vector[18] = float(rate) / 100.0
                    # sys.stdout.write(rate + "\n")
                except TimeoutException as e:
                    fails.append(key_)
                    element = driver.find_element_by_xpath('//*[@id="RateVal"]')
                    rate = None
            else:
                rate = taxratemap[key_]
                vector[18] = rate
        else:
            vector[18] = 0.0

        # Taxed Order Value
        if vector[18] is not None:
            vector[25] = float(vector[24]) * float(vector[18])
        else:
            vector[25] = None

        # Add fields to output vector

# Save Taxrate Mapping 
driver.close()
pickle.dump(taxratemap, rate_file, 2)
rate_file.close

       # Remaining s_row :: 1, 3, 4, 27
        # computation :: 28, 29, 30, 31



with open(shipping_file_name, 'r') as shipcsvfile:    
    xclreader = csv.reader(shipcsvfile)
    isfirstline = True
    for s_row in xclreader:
        if isfirstline:
            isfirstline = False
            continue        
        vector = output_vectors[s_row[0]]
        vector[1] = s_row[12]
        vector[3] = s_row[2]
        vector[4] = s_row[24]
        vector[27] = s_row[20].strip("$").strip("USD").strip()
        vector[28] = max(float(vector[26]) - float(vector[27]), 0.0)
        if vector[18] is not None:
            vector[29] = float(vector[18]) * float(vector[28])
            vector[31] = float(vector[25]) + float(vector[29])
        else:
            vector[29] = 0.0
        vector[30] = float(vector[28]) + float(vector[24])




# Write output to file
xclwriter.writerows(output_vectors.values())
output_file.close()

# Display Debugging Output
print("Failed to find Tax information For:")
print(fails)
print("Number of orders = " + str(len(output_vectors.keys())))
            






