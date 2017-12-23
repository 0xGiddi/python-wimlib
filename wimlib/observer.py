def notify_observers(*args, **kwar):
    def _notify_observers(func):
        def wrapper(self, *args):
            print self
            return func(self, *args)
        return wrapper
    return _notify_observers

class Observerable(object):
    def __init__(self):
        self._callbacks = list()

    def _register(self, callback):
        self._callbacks.append(callback)

    def _notify(self, **attrs):
        event = type('Event', (object,), attrs)
        event.source = self
        for cbfunc in self._callbacks:
            cbfunc(event)