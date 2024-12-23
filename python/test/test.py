# run  from within the directory python/ the command `python -m unittest discover -s test`
import unittest
from src.dispatch import Dispatcher, dispatch


class A(): pass
a = A()

class B(A): pass
b = B()

class C(B): pass
c = C()

class D(C): pass
d = D()

testfun = Dispatcher({
    object : lambda x: "object",
    B : lambda x: "B",
    })

@dispatch(testfun, list)
def _test_list(lst):
    return "list"
print("asdf")

class runtests(unittest.TestCase):
    def test_dispatcher(self):
        self.assertEqual(testfun(a), "object")
        self.assertEqual(testfun(b), "B")
        self.assertEqual(testfun(c), "B")
        self.assertEqual(testfun(d), "B")
        self.assertEqual(testfun([1,2]), "list")
        
        dispatch(testfun, D, lambda x: "D")
        self.assertEqual(testfun(d), "D")
        self.assertEqual(testfun(c), "B")

    
