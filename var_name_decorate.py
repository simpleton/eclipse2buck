def print_var(func):
    def __decorator(var_name):
        print var_name + " = ["
        result = func(var_name)
        print "]"
        return result
    return __decorator

def print_var(func):
    def __decorator(var_name, root):
        print var_name + " = ["
        result = func(var_name, root)
        print "]"
        return result
    return __decorator

