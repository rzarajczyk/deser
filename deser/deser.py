import collections.abc
import inspect


def serialize(o):
    if isinstance(o, int):
        return o
    elif isinstance(o, str):
        return o
    elif isinstance(o, float):
        return o
    elif isinstance(o, bool):
        return o
    elif isinstance(o, collections.abc.Sequence):
        return [serialize(it) for it in o]
    elif isinstance(o, dict):
        return {k: serialize(v) for k, v in o.items()}
    elif hasattr(o, '__dict__'):
        return serialize(o.__dict__)
    else:
        raise Exception("Can't serialize type: %s" % type(o))


def deserialize(o, type_hint=None):
    if isinstance(o, int):
        return o
    elif isinstance(o, str):
        return o
    elif isinstance(o, float):
        return o
    elif isinstance(o, bool):
        return o
    elif isinstance(o, collections.abc.Sequence):
        return [deserialize(it, type_hint) for it in o]
    elif isinstance(o, dict):
        spec = inspect.getfullargspec(type_hint.__init__)
        constructor_args = list(spec.args[1:])
        annotations = spec.annotations
        dict_keys = list(o.keys())
        if constructor_args != dict_keys:
            raise Exception("Deserialization problem: dict keys (%s) doesn't match constructor argument names (%s)" % (dict_keys, constructor_args))
        result = type_hint(**{k: deserialize(v, annotations.get(k)) for k,v in o.items()})
        return result
    else:
        raise Exception("Can't deserialize type: %s" % type(o))


def describe(o):
    if isinstance(o, int) or isinstance(o, str) or isinstance(o, float) or isinstance(o, bool):
        return "(%s) %s" % (type(o).__name__, o)
    elif isinstance(o, collections.abc.Sequence):
        return "[%s]" % ",".join([describe(it) for it in o])
    elif isinstance(o, dict):
        return "{%s}" % ",".join(["%s: %s" % (k, describe(v)) for k, v in o.items()])
    elif hasattr(o, '__dict__'):
        return "(%s) %s" % (type(o).__name__, describe(o.__dict__))
    else:
        return "(%s) %s" % (type(o).__name__, str(o))