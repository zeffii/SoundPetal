from collections import namedtuple

socket_types = {
    'array': 'FlowArraySocket',
    'scalar': 'FlowScalarSocket',
}


def sock(kind='array', name='', default=None):
    '''
    converts a function call, with given parameters to a namedtuple
    All defaults and rewrites should happen in this function, to keep it out
    of the working code in prototyper.py
    '''
    kind = socket_types.get(kind)
    v = vars()
    return namedtuple('Sock', v.keys())(**v)
