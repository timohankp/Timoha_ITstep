import random

class Student:
    def __init__(self, name, age):
        self.name = name
        self.age = age
        self.avg_mark = random.randint(8, 12)
        self.gladness = 50
        self.progress = 0
        self.money = 50

    def __str__(self):
        return f"Name: {self.name}, Age: {self.age}, Mark: {self.avg_mark}"

    def to_study(self):
        print("Time to study")
        self.progress += 1
        self.gladness -= 5
        self.money += 10

    def to_sleep(self):
        print("Time to sleep")
        self.gladness += 3

    def to_chill(self):
        print("Time to chill")
        self.gladness += 5
        self.progress -= 0.5
        self.money -= 40

    def to_work(self):
        print("Time to work")
        self.gladness -= 5
        self.progress -= 0.5
        self.money += 100

    def to_go_shopping(self):
        print("Time to go shopping")
        self.gladness += 3
        self.money -= 50

    def end_of_day(self):
        print(f"Progression: {self.progress:.2f}")
        print(f"Gladness: {self.gladness:.2f}")
        print(f"Money: {self.money:.2f}")

    def live(self,day):
        print("Time to live")
        day = "Day " + str(day) + " of " + self.name
        print(day)
        if self.progress <= 0:
            self.to_study()
        elif self.gladness <= 0:
            if self.money < 100:
                self.to_sleep()
            else:
                self.to_chill()
        elif self.money <= 0:
            self.to_work()
        else:
            live_r = random.randint(1, 5)
            if live_r == 1:
                self.to_study()
            elif live_r == 2:
                self.to_sleep()
            elif live_r == 3:
                self.to_chill()
            elif live_r == 4:
                self.to_work()
            elif live_r == 5:
                self.to_go_shopping()

        self.end_of_day()


nick = Student("Nick", 20)
for day in range(1, 366):
    nick.live(day)