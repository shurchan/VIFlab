#!/usr/bin/env python
#Pass the input.json file as first argument on command line.

import csv, json, sys

input = open(sys.argv[1])
data = json.load(input)
input.close()

output = csv.writer(sys.stdout)

output.writerow(data[0].keys())  # header row

for row in data:
    output.writerow(row.values())




##### 2nd example
import json
import csv 

f = open('test.json')
data = json.load(f)
f.close()

f=csv.writer(open('test.csv','wb+'))

for item in data:
  f.writerow([item['pk'], item['model']] + item['fields'].values())