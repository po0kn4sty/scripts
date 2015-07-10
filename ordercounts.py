#! /usr/local/bin/python

import csv
import operator
import sys
import json

input_name = sys.argv[1]
output_name = sys.argv[2]
#date = sys.argv[3]
# add date filtering

f = open(input_name, 'r')
with open('receipts.json') as datafile:
    data = json.load(datafile)['results']

data = { entry['order_id'] : entry['message_from_buyer'] for entry in data }# if entry.has_key('message_from_buyer')}

#print len(data.items())
#for key, value in data.items():
#    print str(key) + ": " + (value if value else "None = " + str(value))



csvreader = csv.reader(f)
orders = {}
skipped = 0
counted = 0
glossycount = 0
mattecount = 0
csvreader.next()
for line in csvreader:
    if line[0] < '07/02/15' or line[0] > '07/06/15':
        continue
    order_id = int(line[23])
    if (data.has_key(order_id)):
        print "\n\n\n OMG OMG OMG \n\n\n"
    message = "\n - Customer Note: " + (data[order_id] if data.has_key(order_id) else "NoKey")
    counted += 1
    if "gloss" in line[24].lower():
        glossycount += 1
    else:
        mattecount += 1

    name = line[1] + ": " + str("Glossy" if "gloss" in line[24].lower() else "Matte")
    #name = name + str("\n - Customer Note: " + data[int(line[12])] if data.has_key(int(line[12])) else "")
    name += message
    count = line[3]
    if orders.has_key(name):
        orders[name] += int(count)
    else:
        orders[name] = int(count)

f.close()
output_file = open(output_name, 'w')
total = 0
sorted = sorted(orders.items(), key=lambda x: -x[1])
for k, v in sorted:
    total += v
    output_file.write(str(v) + " " + k + "\n")
output_file.close()
print "Total items: " + str(total)
print "counted" + " " + str(counted)
print "skipped" + " " + str(skipped)
print "Glossy count = " + str(glossycount)
print "Matte count = " + str(mattecount)
