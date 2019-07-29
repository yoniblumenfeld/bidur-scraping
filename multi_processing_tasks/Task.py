class Task(object):
    def __init__(self,func,*args,**kwargs):
        self.original_func = func
        self.args = args
        self.kwargs = kwargs
        self.func = lambda: func(*args,**kwargs)

    def __str__(self):
        return '{}({}{})'.format(self.original_func.__name__,self.args,self.kwargs if self.kwargs else '')

    def __repr__(self):
        return self.__str__()

    def __call__(self, *args, **kwargs):
        return self.func()
