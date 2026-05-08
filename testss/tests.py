import unittest
from Timoha_ITstep.testss.task import *


class TestLogin(unittest.TestCase):

    def test_arg1(self):
        self.assertEqual(login("timoha", "12345678"), "Вхід виконано успішно")

    def test_arg2(self):
        self.assertEqual(login("artem", "12345678"), "Невірне ім'я користувача або пароль")

    def test_arg3(self):
        self.assertEqual(login("timoha", "11111111"), "Невірне ім'я користувача або пароль")


if __name__ == "__main__":
    unittest.main()