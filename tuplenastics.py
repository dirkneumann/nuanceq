'''
.flatMap(f_skip(lambda x: x['text'] if 'text' in x else None))
'''
def f_skip(f):
    def _f(x):
        fx = f(x)
        return [fx] if fx != None else []
    return _f


'''
.map(add_(lambda x: x['key']]))
'''
def add_(f):
    def _f(x):
        return (f(x), x)
    return _f


'''
.flatMap(add_skip(lambda x: x['value'] if 'value' in x else None]))
'''
def add_skip(f):
    def _f(x):
        fk = f(x)
        return [(fk, x)] if fk != None else []
    return _f


'''
.map(_add(lambda x: x['value']]))
'''
def _add(f):
    def _f(x):
        return (x, f(x))
    return _f


'''
.map(fk_(lambda key: key + 1))
'''
def fk_(f):
    def _f(x):
        return (f(x[0]), x[1])
    return _f


'''
.flatMap(fk_(lambda key: key + 1 if key > 0 else None))
'''
def fk_skip(f):
    def _f(x):
        fk = f(x[0])
        return [(fk, x[0])] if fk != None else []
    return _f


'''
.map(_fv(lambda value: value + 1))
'''
def _fv(f):
    def _f(x):
        return (x[0], f(x[1]))
    return _f


'''
.flatMap(_fv_skip(lambda value: value['counter'] + 1 if 'counter' in value else None))
'''
def _fv_skip(f):
    def _f(x):
        fv = f(x[1])
        return [(x[0], fv)] if fv != None else []
    return _f


'''
.flatMap(lambda x: x + 1 if x > 0 else None)
)'''
def skip_(f):
    def _f(x):
        fx = f(x)
        return [fx] if fx != None else []
    return _


def fk_skip(f):
    def _f(x):
        fk = f(x[0])
        return [(fk, x[1])] if fk != None else []
    return _f


'''
.map(swap).sortByKey(...).map(swap)
'''
def swap(x):
    return (x[1], x[0])


def fk(f):
    def _f(x):
        return f(x[0])
    return _f


def fv(f):
    def _f(x):
        return f(x[1])
    return _f


def k(x):
    return x[0]


def v(x):
    return x[1]


def dict_kv(x, k, v):
    x[k] = v
    return x
