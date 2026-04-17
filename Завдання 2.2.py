import random

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.avg_mark = random.randint(8, 12)
        self.gladness = 50
        self.prograss = 0
        self.alive = True

    def print_hi(self, name):
        print(f'Hi, {name}')

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}, Mark: {self.avg_mark}"

    def to_study(self):
        print("Time to study")
        self.prograss += 1
        self.gladness -= 5

    def to_sleep(self):
        print("Time to sleep")
        self.gladness += 3

    def to_chill(self):
        print("Time to chill")
        self.gladness += 5
        self.prograss -= 0.5

    def end_of_day(self):
        print(f"Progression: {self.prograss:.2f}")
        print(f"Gladness: {self.gladness:.2f}")

    def live(self,day):
        print("Time to live")
        day = "Day " + str(day) + " of " + self.name
        print(day)
        live_r = random.randint(1,3)
        if live_r == 1:
            self.to_study()
        elif live_r == 2:
            self.to_sleep()
        elif live_r == 3:
            self.to_chill()

        self.end_of_day()


nick = Student("Nick", 20)
for day in range(365):
    nick.live(day)