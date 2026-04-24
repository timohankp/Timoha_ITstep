class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def get_age(self):
        return self.age

    def show_info(self):
        print(f"Ім'я: {self.name}, вік: {self.age}")


class Driver(Person):
    def __init__(self, name, age, number, experience):
        super().__init__(name, age)
        self.number = number
        self.experience = experience

    def check_experience(self):
        if self.experience > 2:
            print("Водій має достатній стаж")
        else:
            print("Водій не має достатнього стажу")

    def show_info(self):
        super().show_info()
        print(f"Номер посвідчення: {self.number}")
        print(f"Стаж: {self.experience} років")
        self.check_experience()


driver1 = Driver("Нік", 20, 548, 1)
driver2 = Driver("Марк", 30, 967, 6)
driver3 = Driver("Білл", 46, 831, 13)

driver1.show_info()
print("-----")
driver2.show_info()
print("-----")
driver3.show_info()