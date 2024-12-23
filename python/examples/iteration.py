#----- some garbage to make sure I can import what I need------
import os, sys
basedir = os.path.join(os.path.dirname(__file__), "..")
if not basedir in sys.path:
    sys.path.append(basedir)
# ---- Real code below here

from dataclasses import dataclass
from src.dispatch import Dispatcher, dispatch
# This File demonstrates how one might set up iteration utilities 
# using a single-dispatch function, in a similar manner as is 
# implemented by julia. It does not require StopIteration-Exceptions to be thrown.
# The funcion provides a fallback-implementation that uses pythons native iteration
# if no specific method is provided

iterate = Dispatcher()

@dispatch(iterate, object)
def iterate_fallback(obj, iterator = None):
    if iterator is None:
        iterator = iter(obj)
    try:
        val = next(iterator)
        return val, iterator
    except StopIteration:
        return None

@dispatch(iterate, list)
def iterate_list(lst, index = 0):
    if index < len(lst):
        return lst[index], index + 1
    else:
        return None

@dataclass
class UnitRange():
    start: int
    stop: int

@dispatch(iterate, UnitRange)
def iterate_list(urange, index = None):
    if index is None:
        index = urange.start
    if index <= urange.stop:
        return index, index + 1
    else:
        return None

mysum = Dispatcher()

@dispatch(mysum, object)
def sum_by_iteration(iterable):
    "Fallback implementation. Anything iterable can be summed up"
    acc = 0
    itr_state = iterate(iterable)

    while itr_state is not None:
        val, _state = itr_state
        acc += val
        itr_state = iterate(iterable, _state)
    print("summed by iteration: ", iterable, ", result: ", acc)

    return acc

# lets pretend the sum over a dictionary should sum up the values, not the keys:
dispatch(mysum, dict, lambda d: mysum(d.values()))

assert mysum((1,2,3)) == 6
# --> summed by iteration:  (1, 2, 3) , result:  6
assert mysum({"a": 3, "b" : 3}) == 6
# --> summed by iteration:  dict_values([3, 3]) , result:  6

assert mysum(UnitRange(1,3)) == 6
# --> summed by iteration:  UnitRange(start=1, stop=3) , result:  6


# ... But hold on a moment. A UnitRange Object can be summed up much more efficient by
# invoking the gauss formula, `sum(1, 2, ..., n) = n * (n+1) / 2`


def gauss_sum(n): return n * (n+1) / 2

@dispatch(mysum, UnitRange)
def sum_urange(urange):
    result = gauss_sum(urange.stop) - gauss_sum(urange.start - 1)
    print("summed via gauss formula: ", urange, ", result: ", acc)
    return acc

# while we're at it...
dispatch(mysum, type(range(12)),  lambda urange: gauss_sum(urange.stop) - gauss_sum(urange.start))

assert mysum(UnitRange(1,3)) == 6
# --> summed via gauss formula:  UnitRange(start=1, stop=3) , result:  6.0


