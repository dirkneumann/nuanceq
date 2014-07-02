def f_skip(f):
    def _f(x):
        fx = f(x)
        return [fx] if fx != None else []
    return _f


def add_(f):
    def _f(x):
        return (f(x), x)
    return _f


def _add(f):
    def _f(x):
        return (x, f(x))
    return _f


def add_skip(f):
    def _f(x):
        fk = f(x)
        return [(fk, x)] if fk != None else []
    return _f


def fk_(f):
    def _f(x):
        return (f(x[0]), x[1])
    return _f


def _fv(f):
    def _f(x):
        return (x[0], f(x[1]))
    return _f


def fk_skip(f):
    def _f(x):
        fk = f(x[0])
        return [(fk, x[0])] if fk != None else []
    return _f


def _fv_skip(f):
    def _f(x):
        fv = f(x[1])
        return [(x[0], fv)] if fv != None else []
    return _f


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
