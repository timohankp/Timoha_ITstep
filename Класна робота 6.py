'''try:
    num = int(input("Enter a number: "))
    print(8/num)
except:
    print("invalid input")'''


'''try:
    count = int(input("Enter a number: "))
    type_box = input("Enter a box type: ")
    print(f"we got {type_box} in {count} times")
    part_count = count // int(input("Enter amount of parts: "))
except ZeroDivisionError:
    print("you can't divide by zero")
except ValueError:
    print("invalid input, try again, first number then type")
except Exception as e:
    print("something went wrong", e)
finally:
    print("Thank you for your time")'''


'''print("first task")
try:
    num1 = int(input("Enter a number: "))
except:
    print("It's not a number!")


print("second task")
while True:
    try:
        num2 = int(input("Введіть число: "))
        break
    except :
        print("Це не число, спробуйте ще раз.")


print("third task")
letters = ['a', 'b', 'c']
try:
    index = int(input("Enter a number: "))
    print("Елемент:", letters[index])
except ValueError:
    print("this is not a number")
except IndexError:
    print("wrong input")'''


try:
    age = int(input("Enter a number: "))
    if age < 0 or age > 120:
        raise Exception("invalid age")
except Exception as e:
    print(e)




