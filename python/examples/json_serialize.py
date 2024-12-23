#----- some garbage to make sure I can import what I need------
import os, sys
basedir = os.path.join(os.path.dirname(__file__), "..")
if not basedir in sys.path:
    sys.path.append(basedir)
# ---- Real code below here
# This file demonstrates how one can use SingleDispatch to write
# a function to_json that serializes an object to a json string. 



from src.dispatch import Dispatcher, dispatch

to_json = Dispatcher()

@dispatch(to_json, str)
def serialize_str(s):
    escaped_str = s.replace("\\", "\\\\").replace("\"", "\\\"")
    return "\"" + escaped_str + "\""

dispatch(to_json, int, str)
dispatch(to_json, float, str)
dispatch(to_json, bool, lambda b: "true" if b else "false")

@dispatch(to_json, list)
def serialize_list(lst):
    return "[ " + ", ".join(map(to_json, lst)) + " ]"

@dispatch(to_json, dict)
def serialize_dict(d):
    return "{ " + ", ".join(serialize_str(k) + " : " + to_json(v) for (k, v) in d.items()) + "}"

dispatch(to_json, type(None), lambda _none: "Null")


print(to_json([1, {"foo" : True, "bar" : None}, "ssa\"df", ["inner list"]]))
# --> [ 1, { "foo" : true, "bar" : Null}, "ssa\"df", [ "inner list" ] ]


# Note that it was possible to "add methods" to native builtin types like string and lists
# If, hypothetically, someone wanted to extend this functionality to some selfwritten class,
# one could easily do so like this:

# in some distant file:

# from to_json import to_json
# class MyThing():
#   ...
#   ...
#
# @dispatch(to_json, MyThing)
# def mything_to_json(thing):
#   ...


