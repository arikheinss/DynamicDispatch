
#----- some garbage to make sure I can import what I need------
import os, sys
basedir = os.path.join(os.path.dirname(__file__), "..")
if not basedir in sys.path:
    sys.path.append(basedir)
# ---- Real code below here

from src.dispatch import Dispatcher, dispatch

haskey = Dispatcher({
    object : lambda obj, k: False, # if we don't know how to index, it cannot index
    dict: lambda d, k: k in d,
    list: lambda lst, idx: isinstance(idx, int) and 0<=idx<=len(lst),
    })



