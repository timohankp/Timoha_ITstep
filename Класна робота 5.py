'''import requests

help(requests)
print(requests.__cake__)

def func():
    pass

class Human:
    pass

rq = requests
f1 = func
max = Human

print(requests.__name__)
print(rq.__name__)

print(f1.__name__)
print(func.__name__)

(Human.__name__)
print(max.__name__)


max2 = Human()
print(type(max2))

print(type(func))


str1 = "python"
print(str1)
print(hasattr(str1,"reverse"))
print(hasattr(str1,"index"))

print(callable(max2))


class Driver(Human):
    pass

driver = Driver()

print(isinstance(driver, Driver))
print(isinstance(driver, Human))



import inspect

print(inspect.ismodule(requests))
print(inspect.ismodule(max))
print(inspect.isclass(max))
print(inspect.ismethod(max))'''

import requests
l1 = []

number = 123

text = "python"

print(type(number))
print(type(text))
print(type(l1))

print("--------------")

print(hasattr(number,"reverse"))
print(hasattr(number,"index"))

print("--------------")

method = getattr(text, "upper")
print(method())

print("--------------")

def explore(obj):
    print("Тип:", type(obj))
    print("Методи:", dir(obj))
    print("Має довжину:", hasattr(obj, "__len__"))

explore("Pycharm")
explore([1, 3, 5])
explore(67)