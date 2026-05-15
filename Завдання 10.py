import sqlite3
import requests
import time
import threading
from datetime import datetime
import tkinter as tk
from tkinter import ttk


class ConsoleWeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Terminal")
        self.root.geometry("650x400")  # Збільшено ширину для дати
        self.root.configure(bg="black")

        # Стиль для темно-сірого скролбару
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure(
            "Vertical.TScrollbar",
            background="#333333",
            troughcolor="#1e1e1e",
            bordercolor="#1e1e1e",
            arrowcolor="#00FF00",
            gripcount=0
        )

        # Головний заголовок
        self.label = tk.Label(
            root,
            text="WEATHER_MONITOR_SYSTEM v1.0",
            font=("Consolas", 12, "bold"),
            bg="black",
            fg="#00FF00"
        )
        self.label.pack(pady=5)

        self.main_frame = tk.Frame(root, bg="#1e1e1e")
        self.main_frame.pack(pady=10, padx=10, fill="both", expand=True)

        self.log_area = tk.Text(
            self.main_frame,
            font=("Consolas", 10),
            bg="#1e1e1e",
            fg="#00FF00",
            insertbackground="#00FF00",
            borderwidth=0,
            highlightthickness=0,
            state='disabled'
        )

        self.scrollbar = ttk.Scrollbar(
            self.main_frame,
            orient="vertical",
            command=self.log_area.yview,
            style="Vertical.TScrollbar"
        )
        self.log_area.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.log_area.pack(side="left", fill="both", expand=True)

        # Теги кольорів
        self.log_area.tag_config("blue_val", foreground="#00AEEF")
        self.log_area.tag_config("yellow_txt", foreground="#FFD700")
        self.log_area.tag_config("green_sep", foreground="#00FF00")

        self.is_running = True
        self.setup_db()

        # Завантажуємо історію з повною датою
        self.load_history()

        self.thread = threading.Thread(target=self.update_loop, daemon=True)
        self.thread.start()

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

    def setup_db(self):
        self.conn = sqlite3.connect('weather_log.db', check_same_thread=False)
        self.conn.execute("PRAGMA journal_mode=WAL")
        cursor = self.conn.cursor()
        cursor.execute('CREATE TABLE IF NOT EXISTS data (id INTEGER PRIMARY KEY AUTOINCREMENT, dt TEXT, temp TEXT)')
        self.conn.commit()

    def load_history(self):
        try:
            cursor = self.conn.cursor()
            cursor.execute("SELECT dt, temp FROM data ORDER BY id DESC LIMIT 50")
            rows = cursor.fetchall()

            for dt, temp in reversed(rows):
                self.write_to_terminal(dt, temp)

            if rows:
                self.log_area.configure(state='normal')
                self.log_area.insert(tk.END, "-" * 65 + "\n", "green_sep")
                self.log_area.insert(tk.END, f"> SYSTEM: {len(rows)} RECORDS RESTORED FROM DATABASE\n", "green_sep")
                self.log_area.insert(tk.END, "-" * 65 + "\n", "green_sep")
                self.log_area.configure(state='disabled')
        except Exception as e:
            print(f"Load error: {e}")

    def write_to_terminal(self, dt_string, temp):
        """dt_string тепер містить дату і час."""
        self.log_area.configure(state='normal')

        self.log_area.insert(tk.END, "> ", "green_sep")
        self.log_area.insert(tk.END, "LOG: ", "yellow_txt")

        # Виводимо повну дату і час синім
        self.log_area.insert(tk.END, f"{dt_string} ", "blue_val")

        self.log_area.insert(tk.END, "| ", "green_sep")
        self.log_area.insert(tk.END, "TEMP: ", "yellow_txt")
        self.log_area.insert(tk.END, f"{temp} ", "blue_val")
        self.log_area.insert(tk.END, "| ", "green_sep")
        self.log_area.insert(tk.END, "STATUS: ", "yellow_txt")
        self.log_area.insert(tk.END, "SAVED\n", "blue_val")

        self.log_area.see(tk.END)
        self.log_area.configure(state='disabled')

    def get_weather(self):
        url = "https://wttr.in/Nikopol?format=%t"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                return response.text.strip()
        except:
            return None
        return None

    def update_loop(self):
        while self.is_running:
            temp = self.get_weather()
            # Додаємо день, місяць та рік
            full_dt = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

            if temp:
                cursor = self.conn.cursor()
                cursor.execute("INSERT INTO data (dt, temp) VALUES (?, ?)", (full_dt, temp))
                self.conn.commit()
                self.write_to_terminal(full_dt, temp)
            else:
                current_time = datetime.now().strftime("%H:%M:%S")
                self.log_area.configure(state='normal')
                self.log_area.insert(tk.END, f"> ERROR: {current_time} | CONNECTION FAILED\n", "yellow_txt")
                self.log_area.configure(state='disabled')

            time.sleep(1800)

    def on_close(self):
        self.is_running = False
        try:
            self.conn.close()
        except:
            pass
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ConsoleWeatherApp(root)
    root.mainloop()