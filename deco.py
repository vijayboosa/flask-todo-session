def validator(func):
    print("inside validator")

    def wrapper(*args, **kwargs):
        # args -> (2,4)
        print("inside wrapper")
        if isinstance(args[0], str) or isinstance(args[1], str):
            print("Arguments must be numeric")
            return
        print("going to call the actual add function")
        return func(*args, **kwargs)

    print("returning wrapper")
    return wrapper


@validator  # validator(add) -> add = wrapper
def add(x, y):
    return x + y


def validate_and_sum(x, y):
    if isinstance(x, str) or isinstance(y, str):
        raise TypeError("Arguments must be numeric")
    return add(x, y)


# a = validate_and_sum(2, 3)
# b = validate_and_sum("hello", "world")
print("going to start the addition")
a = add(2, 3)
print(a)
b = add("hello", "world")
print(b)
