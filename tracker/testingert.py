def calculator(func):
    def wrapper(*args, **kwargs):
        print("=" * 30)
        print(f"running: {func.__name__}")
        print(f"arguments: {args}")
        if kwargs:
            print(f"keyword arguments: {kwargs}")
        result = func(*args, **kwargs)
        print(f"result: {result}")
        return result
    return wrapper
@calculator
def add(a, b):
    return a + b
@calculator
def substract(a, b):
    return a - b
@calculator
def multiply(a, b):
    return a * b
@calculator
def words(name, age):
    print(f"hello my name is {name} and i am {age} years old")


print(add(2, 5))
print(words("Mark", 18))