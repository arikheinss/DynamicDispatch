class Dispatcher():
    def __init__(self, init = {}):
        self.methodTable = dict()
        self.methodTable.update(init)
    def __call__(self, obj, *args, **kwargs):
        for dtype in type(obj).__mro__:
            if (method := self.methodTable.get(dtype, None)) is not None:
                return method(obj, *args, **kwargs)
        raise Exception(f"Method not found for object of type {type(obj)}")
    def __setitem__(self, t, mthd):
        self.methodTable[t] = mthd
    

def dispatch(fn, t, mthd = None):
    if mthd is None:
        def register_method(mthd):
            fn[t] = mthd
            return mthd
        return register_method
    else:
        fn[t] = mthd

