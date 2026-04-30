from colorama import Back, Fore, Style, Cursor, init #Імпорт елементів з бібліотеки
import time # інша бібліотека

# --- Блок інтроспекції ---
print(f"Атрибути Fore: {dir(Fore)}")
print(f"Тип об'єкта Fore: {type(Fore)}")

print(f"Атрибути Back: {dir(Back)}")
print(f"Тип об'єкта Back: {type(Back)}")

print(f"Атрибути Style: {dir(Style)}")
print(f"Тип об'єкта Style: {type(Style)}")

print(f"Атрибути Cursor: {dir(Cursor)}")
print(f"Тип об'єкта Cursor: {type(Cursor)}")

if hasattr(Fore,"BLACK"):
    print("Fore має атрибут BLACK")
else:
    print("Fore не має атрибут BLACK")
if hasattr(Back,"67"):
    print("Fore має атрибут 67")
else:
    print("Back не має атрибут 67")

print("Приклад:")

init(autoreset=True) # дозволяє кожен раз не писати RESET

print(Back.GREEN + "Зелений фон") # Змінює колір фону тексту

print(Fore.RED + "Червоний текст") # Змінює колір тексту

print(Style.BRIGHT + "Яскравий текст", end="") # Змінює стиль

time.sleep(3) # Дозволяє зробити паузу

print(Cursor.UP(1) + "\r" + "Новий текст замість попереднього" + " " * 10) # піднімає курсор вверх, а потім змінює текст

# --- ВИСНОВКИ ---
# 1. Об'єкти Fore, Back, Style містять атрибути у вигляді ANSI-кодів для зміни кольору тексту та фону в консолі.

# 2. Cursor містить методи (наприклад UP), які дозволяють керувати положенням курсора в терміналі.

# 3. Функція init() ініціалізує бібліотеку і дозволяє автоматично скидати стилі (autoreset=True).

# 4. dir() дозволяє отримати список атрибутів об'єкта, а type() — визначити його тип.

# 5. hasattr() перевіряє, чи існує певний атрибут у об'єкта.