import random

class Pet:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.satiety = 30
        self.energy = 10
        self.alive = True

    def print_hi(self,name):
        print(f'Hi, {name}!')

    def __str__(self):
        return f'name: {self.name}, age: {self.age} '

    def eat(self):
        print("Time to eat!")
        self.satiety += 5
        self.energy -= 2

    def sleep(self):
        print("Time to sleep!")
        self.satiety -= 1
        self.energy += 8

    def play(self):
        print("Time to play!")
        self.satiety -= 2
        self.energy -= 2

    def end_of_day(self):
        print(f"satiety: {self.satiety}")
        print(f"energy: {self.energy}")

    def live(self, day):
        print("Time to live!")
        day_str = "Day " + str(day) + " of " + self.name
        print(day_str)
        live_r = random.randint(1,3)
        if live_r == 1:
            self.sleep()
        elif live_r == 2:
            self.eat()
        elif live_r == 3:
            self.play()

        self.end_of_day()

Murchik = Pet("Murchik", 5)
for day in range(1, 365):
    Murchik.live(day)