#! /usr/local/bin/python

import csv
import operator
import sys
import json
import re

input_name = sys.argv[1]
output_name = sys.argv[2]
start_date = sys.argv[3]
end_date = sys.argv[4]

f = open(input_name, 'r')
with open('receipts.json') as datafile:
    data = json.load(datafile)['results']

data = { entry['receipt_id'] : entry['message_from_buyer'] for entry in data
        if (entry.has_key('message_from_buyer') and entry['message_from_buyer'] != 'None' and entry['message_from_buyer'] != 'nul' and entry['message_from_buyer'] != None)}

csvreader = csv.reader(f)
orders = {}
skipped = 0
counted = 0
glossycount = 0
mattecount = 0
customcount = 0
csvreader.next()
customs = []
matteorders = {}
glossyorders = {}
stripper = re.compile('(?= \| set of).*', re.IGNORECASE)
for line in csvreader:
    order_date = line[0]
    if order_date < start_date or order_date > end_date:
        continue
    order_id = int(line[23])
    material = str("Glossy" if "gloss" in line[24].lower() else "Matte")
    order_item_name = re.sub(stripper, "", line[1])
    order_item_name += ", Options: "
    inner_message =  str((data[order_id] if data.has_key(order_id) else ""))
    message = line[24]
    if inner_message:
        message += "\n#BeginNote\n" + inner_message + "\n#EndNote\n"
    else:
        pass
    order_item_name += message
    count = line[3]
    if 'custom' in order_item_name:
        customcount += 1
        if not inner_message:
            customs.append(line)
    counted += 1
    if material == "Glossy":
        glossycount += 1
        if glossyorders.has_key(order_item_name):
            glossyorders[order_item_name] += int(count)
        else:
            glossyorders[order_item_name] = int(count)
    else:
        mattecount += 1
        if matteorders.has_key(order_item_name):
            matteorders[order_item_name] += int(count)
        else:
            matteorders[order_item_name] = int(count)

    if orders.has_key(order_item_name):
        orders[order_item_name] += int(count)
    else:
        orders[order_item_name] = int(count)

f.close()
output_file = open(output_name, 'w')
total = 0
orderssorted = sorted(orders.items(), key=lambda x: -x[1])
mattesort = sorted(matteorders.items(), key=lambda x: -x[1])
glossysort = sorted(glossyorders.items(), key=lambda x: -x[1])
for k, v in mattesort:
    total += v
    output_file.write(str(v) + " " + k + "\n")
output_file.flush()
for k, v in glossysort:
    total += v
    output_file.write(str(v) + " " + k + "\n")

output_file.close()

print "glossy = " + str(len(glossysort))
print "matte = " + str(len(mattesort))
print "Total items: " + str(total)
print "counted" + " " + str(counted)
print "skipped" + " " + str(skipped)
print "Glossy count = " + str(glossycount)
print "Matte count = " + str(mattecount)
print customs
print customcount

