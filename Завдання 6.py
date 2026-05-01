result = []

def divider(a, b):
    if isinstance(a, str) or isinstance(b, str):
        raise TypeError("одне з чисел текст а не цифра")
    if isinstance(a, tuple) or isinstance(b, tuple):
        raise TypeError("одне з чисел є кортежем")

    if a < b:
        raise ValueError("a менше за b")

    if b > 100:
        raise IndexError("b більше 100")

    if b == 0:
        raise ZeroDivisionError("На 0 ділити не можна")

    return a / b


data = {10: 2, 2: 5, "123": 4, 18: 0, (1, 2): 15, 200: 101, 8: 4}

for key in data:
    try:
        res = divider(key, data[key])
        result.append(res)

    except ValueError as e:
        print(f"ValueError для {key}: {data[key]} -> {e}")

    except IndexError as e:
        print(f"IndexError для {key}: {data[key]} -> {e}")

    except ZeroDivisionError as e:
        print(f"ZeroDivisionError для {key}: {data[key]} -> {e}")

    except TypeError as e:
        print(f"TypeError для {key}: {data[key]} -> {e}")

print("Результат:", result)