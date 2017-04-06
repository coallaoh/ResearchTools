__author__ = 'joon'


def apply_async_wrapper(func, *args):
    try:
        return func(*args)
    except Exception as e:
        return e
