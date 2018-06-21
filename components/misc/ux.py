once_set = set()

def once(key):
    if key in once_set:
        return False
    else:
        once_set.add(key)
        return True

already_complained = set()


def deprecated(replacement=None):
    def outer(func):
        def inner(*args, **kwargs):
            if func not in already_complained:
                if replacement is None:
                    print ("Deprecation warning: Don't use %s" % (func.func_name))
                else:
                    print("Deprecation warning: Use %s insted of %s" % (replacement, func.func_name))

                already_complained.add(func)
            return func(*args, **kwargs)
        return inner
    return outer

