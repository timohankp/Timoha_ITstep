class Pet:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.satiety = 30
        self.sleep = 10


    def print_hi(self,name):
        print(f'Hi, {name}!')


    def __str__(self):
        return f'name: {self.name}, age: {self.age} '
