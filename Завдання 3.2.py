class Product:
    def __init__(self, name, price, availability):
        self.name = name
        self.price = price
        self.availability = availability


class Cart:
    def __init__(self):
        self.products = []

    def add_product(self, product):
        self.products.append(product)

    def remove_product(self, product):
        if product in self.products:
            self.products.remove(product)

    def show_products(self):
        for product in self.products:
            print(f"{product.name} - ціна: {product.price}, наявність: {product.availability}")

    def total_price(self):
        total = 0
        for product in self.products:
            if product.availability == True:
                total += product.price
        print(f"Загальна сума: {total}")
        return total


p1 = Product("Телефон", 8000, True)
p2 = Product("Худі", 2500, True)
p3 = Product("Лего", 1700, False)

cart = Cart()

cart.add_product(p1)
cart.add_product(p2)
cart.add_product(p3)

cart.show_products()
cart.total_price()


