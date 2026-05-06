def safe_calculator(func):
    def wrapper(expression):
        try:
            result = func(expression)
            return result

        except ZeroDivisionError:
            return "На нуль ділити не можна!"

        except ValueError:
            return "Неможливо обробити дані!"

        except SyntaxError:
            return "Синтаксична помилка!"

        except Exception as e:
            return f"Щось пішло не так: {e}"

    return wrapper


@safe_calculator
def calculate(expression):
    return eval(expression)


while True:
    expr = input("Напишіть вираз (або 'exit'): ")

    if expr.lower() == "exit":
        print("Калькулятор завершено")
        break

    res = calculate(expr)
    print("Результат:", res)
    if res == 67:
        print("ЄЄЄЄЄЄЄ 67!")