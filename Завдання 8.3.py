def login():
    username = input("Username: ")
    password = input("Password: ")

    if len(username) < 3 or len(username) > 20 or len(password) < 8:
        print("Invalid username or password, please try again.")
    else:
        print("Login Successful")

    return username, password
