import requests
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, messagebox

# =========================
# Темна тема
# =========================
BG_COLOR = "#1e1e1e"
CARD_COLOR = "#2b2b2b"
TEXT_COLOR = "#ffffff"
ACCENT_COLOR = "#4e9cff"

# =========================
# Парсинг сайту
# =========================

def get_books():
    base_url = "http://books.toscrape.com/catalogue/page-{}.html"
    all_books = []

    for page in range(1, 51):
        url = base_url.format(page)

        response = requests.get(url)
        soup = BeautifulSoup(response.text, "html.parser")

        books = soup.find_all("article", class_="product_pod")

        for book in books:
            title = book.h3.a["title"]
            price = book.find("p", class_="price_color").text
            availability = book.find(
                "p",
                class_="instock availability"
            ).text.strip()
            rating = book.find("p")["class"][1]

            all_books.append({
                "title": title,
                "price": price,
                "availability": availability,
                "rating": rating
            })

    return all_books

# =========================
# GUI
# =========================

books_data = get_books()

root = tk.Tk()
root.title("Books Scraper")
root.geometry("1000x650")
root.configure(bg=BG_COLOR)

# Стилі
style = ttk.Style()
style.theme_use("clam")

style.configure(
    "Treeview",
    background=CARD_COLOR,
    foreground=TEXT_COLOR,
    fieldbackground=CARD_COLOR,
    rowheight=30,
    font=("Arial", 11)
)

style.map(
    "Treeview",
    background=[("selected", ACCENT_COLOR)]
)

style.configure(
    "Treeview.Heading",
    background=ACCENT_COLOR,
    foreground="white",
    font=("Arial", 12, "bold")
)

# Заголовок
header = tk.Label(
    root,
    text="📚 Books To Scrape",
    bg=BG_COLOR,
    fg=TEXT_COLOR,
    font=("Arial", 24, "bold")
)
header.pack(pady=15)

# Інструкція
info_label = tk.Label(
    root,
    text="Подвійний клік по книзі для перегляду характеристик",
    bg=BG_COLOR,
    fg="#bbbbbb",
    font=("Arial", 11)
)
info_label.pack(pady=5)

# Таблиця
columns = ("Назва", "Ціна", "Наявність", "Рейтинг")

tree = ttk.Treeview(root, columns=columns, show="headings")

for col in columns:
    tree.heading(col, text=col)

    # Назви книг — ліворуч
    if col == "Назва":
        tree.column(col, width=420, anchor="w")
    else:
        # Інші колонки — по центру
        tree.column(col, width=170, anchor="center")

# Додаємо книги
for book in books_data:
    tree.insert(
        "",
        tk.END,
        values=(
            book["title"],
            book["price"],
            book["availability"],
            book["rating"]
        )
    )

# Скролбар
scrollbar = ttk.Scrollbar(root, orient="vertical", command=tree.yview)
tree.configure(yscrollcommand=scrollbar.set)

scrollbar.pack(side="right", fill="y")
tree.pack(fill="both", expand=True, padx=20, pady=20)

# =========================
# Вікно інформації
# =========================

def show_book_info(event):
    selected_item = tree.selection()

    if selected_item:
        item = tree.item(selected_item)
        values = item["values"]

        messagebox.showinfo(
            "Інформація про книгу",
            f"📖 Назва: {values[0]}\n\n"
            f"💰 Ціна: {values[1]}\n\n"
            f"📦 Наявність: {values[2]}\n\n"
            f"⭐ Рейтинг: {values[3]}"
        )

# Подвійний клік

tree.bind("<Double-1>", show_book_info)

# Запуск програми
root.mainloop()

