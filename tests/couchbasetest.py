#!/usr/bin/env python

from couchbase import Couchbase

#cb = Couchbase.connect(host = '10.141.100.101', port=8091, bucket='default') #http://10.141.100.102:8091/

cb = Couchbase.connect(host = '10.141.100.101', port=8091, bucket='beer-sample') #http://10.141.100.102:8091/

result = cb.get('new_holland_brewing_company-sundog')

print result


new_beer = {
   "name": "Old Yankee Ale Jeren",
   "abv": 5.00,
   "ibu": 0,
   "srm": 0,
   "upc": 0,
   "type": "beer",
   "brewery_id": "cottrell_brewing_co",
   "updated": "2012-08-30 20:00:20",
   "description": ".A medium-bodied Amber Ale Jeren",
   "style": "American-Style Amber Jeren",
   "category": "North American Ale"
}

key = "{0}-{1}".format(
        new_beer['brewery_id'],
        new_beer['name'].replace(' ', '_').lower())
# key is "cottrell_brewing_co-old_yankee_ale"

result = cb.set(key, new_beer)

result = cb.get('cottrell_brewing_co-old_yankee_ale_jeren')

print result
