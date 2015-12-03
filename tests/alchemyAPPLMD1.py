#!/usr/bin/env python

from __future__ import print_function

import sys
sys.path.insert(0, r'/Users/misc/code/viflab/utils')

from alchemyapi import AlchemyAPI
import json


#demo_text = 'Yesterday dumb Bob destroyed my fancy iPhone in beautiful Denver, Colorado. I guess I will have to head over to the Apple Store and buy a new one.'
readfile = open('APPL_Test1.txt', 'r')
demo_text=readfile.read()

#demo_url = 'http://www.npr.org/2013/11/26/247336038/dont-stuff-the-turkey-and-other-tips-from-americas-test-kitchen'
# demo_html = '<html><head><title>Python Demo | AlchemyAPI</title></head><body><h1>Did you know that AlchemyAPI works on HTML?</h1><p>Well, you do now.</p></body></html>'
#image_url = 'http://demo1.alchemyapi.com/images/vision/football.jpg'

# Create the AlchemyAPI Object
alchemyapi = AlchemyAPI()


print('')
print('')
print('')
print('############################################')
print('#   Combined  Example                      #')
print('############################################')
print('')
print('')

#print('Processing text: ', demo_text)
print('')

response = alchemyapi.combined('text', demo_text)

if response['status'] == 'OK':
    print('## Response Object ##')
    print(json.dumps(response, indent=4))

    print('')

    print('## Keywords ##')
    for keyword in response['keywords']:
        print(keyword['text'], ' : ', keyword['relevance'])
    print('')

    print('## Concepts ##')
    for concept in response['concepts']:
        print(concept['text'], ' : ', concept['relevance'])
    print('')

    print('## Entities ##')
    for entity in response['entities']:
        print(entity['type'], ' : ', entity['text'], ', ', entity['relevance'])
    print(' ')

else:
    print('Error in combined call: ', response['statusInfo'])

print('')
print('')
