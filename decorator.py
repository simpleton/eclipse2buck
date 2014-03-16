class target(object):
    
    def __init__(self, name):
        self.name = name

    def __call__(self, f):
        def wrapped(*args):
            print self.name + "("
            result = f(*args)
            print ")\n"
            return result
        return wrapped

class var(object):
    
    def __init__(self, name):
        self.name = name

    def __call__(self, f):
        def wrapped(*args):
            print self.name + " = ["
            result = f(*args)
            print "]\n"
            return result
        return wrapped

class var_with_comma(object):
    
    def __init__(self, name):
        self.name = name

    def __call__(self, f):
        def wrapped(*args):
            print self.name + " = ["
            result = f(*args)
            print "],"
            return result
        return wrapped
