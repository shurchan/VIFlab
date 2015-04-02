#!/usr/bin/env python
import jsonpickle
import json

def json_serialize(obj, filename, use_jsonpickle=True):
    f = open(filename, 'w')
    if use_jsonpickle:
        import jsonpickle
        #json_obj = jsonpickle.encode(obj)
        json_obj = jsonpickl.encode({'foo': True}, unpicklable=False, max_depth=2)
        
        f.write(json_obj)
    else:
        json.dump(obj, f) 
    f.close()

def json_load_file(filename, use_jsonpickle=True):
    f = open(filename)
    if use_jsonpickle:
        import jsonpickle
        json_str = f.read()
        obj = jsonpickle.decode(json_str)
    else:
        obj = json.load(f)
    return obj

class Foo(object):
    #def __init__(self, hello):
    #    self.hello = 'hello world'

    def __init__(self, value):
        self.key1 = value
        arr={}
        #append value to arr
        arr.update({'key3':'value3'})
        arr.update({'key4':'value4'})
        self.key2 = arr


# make a Foo obj
obj = Foo("hello world")
#obj_str = jsonpickle.encode(obj)
#jsonpickle.encode(obj, unpicklable=False)
obj_str = jsonpickle.encode(obj, unpicklable=False, max_depth=2)
f = open("test1.js", 'w')
f.write(obj_str)
f.close()

print "test111"

#restored_obj = jsonpickle.decode(obj_str)
#list_objects = [restored_obj]
# We now get a list with a dictionary, rather than
# a list containing a Foo object

#print "list_objects: ", list_objects