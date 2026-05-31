import tkinter as tk
from tkinter import ttk
import random

# =========================
# НАЛАШТУВАННЯ СКЛАДНОСТІ
# =========================
DIFFICULTY_SETTINGS = {
    "easy": {
        "label": "🟢 ЛЕГКО",
        "color": "#00ff66",
        "description": "Повільний знос • Слабкі катастрофи • Більше часу на реакцію",
        "start": {"energy": 90, "security": 90, "training": 85, "core": 80,
                  "budget": 500, "staff": 30},
        "decay": {"energy": (0, 2), "security": (0, 1), "training": (0, 1), "core": (0, 1)},
        "disaster_mult": 0.6,
        "disaster_interval": 15000,
        "budget_income": 25,
        "staff_regen": 2,
        "combo_threshold": 60,
        "combo_reward": {"budget": 40, "staff": 1, "all_stats": 5},
    },
    "normal": {
        "label": "🟡 НОРМАЛЬНО",
        "color": "#ffd700",
        "description": "Стандартний знос • Звичайні катастрофи • Баланс",
        "start": {"energy": 78, "security": 91, "training": 65, "core": 52,
                  "budget": 300, "staff": 20},
        "decay": {"energy": (1, 3), "security": (0, 2), "training": (0, 1), "core": (1, 2)},
        "disaster_mult": 1.0,
        "disaster_interval": 10000,
        "budget_income": 15,
        "staff_regen": 1,
        "combo_threshold": 70,
        "combo_reward": {"budget": 60, "staff": 2, "all_stats": 8},
    },
    "hard": {
        "label": "🔴 ВАЖКО",
        "color": "#ff4444",
        "description": "Швидкий знос • Руйнівні катастрофи • Мало часу",
        "start": {"energy": 65, "security": 60, "training": 50, "core": 45,
                  "budget": 150, "staff": 12},
        "decay": {"energy": (2, 5), "security": (1, 3), "training": (1, 2), "core": (2, 4)},
        "disaster_mult": 1.7,
        "disaster_interval": 6000,
        "budget_income": 8,
        "staff_regen": 1,
        "combo_threshold": 80,
        "combo_reward": {"budget": 90, "staff": 3, "all_stats": 12},
    },
}

# Формат: (текст, енергія, безпека, навчання, core, бюджет, персонал)
DISASTERS = [
    ("🚨 КІБЕРАТАКА: Зловмисники атакують шлюзи! Безпека падає!", 0, -25, 0, -5, -40, 0),
    ("🔥 ЗБІЙ ДАТАЦЕНТРУ: Перегрів серверних стійок! CORE та Енергія падають!", -20, 0, 0, -25, -60, -2),
    ("💣 DDoS-АТАКА: Масове перевантаження мережі! Безпека та CORE падають!", 0, -15, 0, -15, -30, 0),
    ("🌩 СТРИБОК НАПРУГИ: Пошкоджено блоки живлення! Енергія критична!", -30, 0, 0, -10, -50, 0),
    ("👔 ЗВІЛЬНЕННЯ ПЕРСОНАЛУ: Масовий відхід співробітників!", 0, -10, -15, 0, 0, -5),
    ("💸 БЮДЖЕТНА КРИЗА: Фінансування урізано!", 0, 0, -10, -5, -80, 0),
]

# Глобальні змінні
energy = 0
security = 0
training = 0
core = 0
budget = 0
staff = 0
game_running = False
seconds_survived = 0
difficulty_key = "normal"
diff_cfg = {}
income_timer = 0
combo_active = False
combo_seconds = 0


# =========================
# ДОПОМІЖНІ ФУНКЦІЇ
# =========================

def clamp(value, min_v=0, max_v=100):
    return max(min_v, min(max_v, value))


def get_style_name(value):
    if value >= 70:
        return "green.Horizontal.TProgressbar"
    elif value >= 40:
        return "yellow.Horizontal.TProgressbar"
    else:
        return "red.Horizontal.TProgressbar"


def update_bar(bar, label, value, icon, text):
    bar["value"] = value
    bar.configure(style=get_style_name(value))
    if value < 30:
        label.config(text=f"🚨 {icon} {text}: {value}% [КРИТИЧНО]", fg="#ff4444")
    else:
        label.config(text=f"{icon} {text}: {value}%", fg="white")


def refresh_resources():
    budget_color = "#ff4444" if budget < 50 else ("#ffd700" if budget < 150 else "#00ff66")
    budget_label.config(text=f"💰 Бюджет: {budget} грн", fg=budget_color)
    budget_bar["value"] = min(budget, 500)
    budget_bar.configure(style=get_style_name(min(budget / 5, 100)))

    staff_color = "#ff4444" if staff < 5 else ("#ffd700" if staff < 12 else "#00ff66")
    staff_label.config(text=f"👥 Персонал: {staff} ос.", fg=staff_color)
    staff_bar["value"] = min(staff, 50)
    staff_bar.configure(style=get_style_name(min(staff * 2, 100)))


def refresh_ui():
    update_bar(energy_bar, energy_label, energy, "⚡", "Енергія")
    update_bar(security_bar, security_label, security, "🔒", "Безпека")
    update_bar(training_bar, training_label, training, "📚", "Навчання")
    update_bar(core_bar, core_label, core, "🧠", "CORE")
    refresh_resources()
    timer_label.config(text=f"🏆 Час виживання: {seconds_survived} сек")


def log(text):
    event_log.configure(state="normal")
    event_log.insert(tk.END, text + "\n")
    event_log.see(tk.END)
    event_log.configure(state="disabled")
    event_log.update_idletasks()
    print(text)


def can_afford(cost_budget, cost_staff, action_name):
    if budget < cost_budget:
        log(f"❌ Недостатньо бюджету для '{action_name}'! Потрібно: {cost_budget} грн, є: {budget} грн")
        return False
    if staff < cost_staff:
        log(f"❌ Недостатньо персоналу для '{action_name}'! Потрібно: {cost_staff} ос., є: {staff} ос.")
        return False
    return True


# =========================
# AI АНАЛІТИК
# =========================

def update_ai():
    if not game_running:
        return
    messages = []
    has_critical = False

    if core < 30:
        messages.append("🔴 CORE нестабільний. Рекомендується негайне відновлення серверів.")
        has_critical = True
    if energy < 30:
        messages.append("🔴 Рівень енергії критичний. Системи під загрозою вимкнення.")
        has_critical = True
    if security < 30:
        messages.append("🚨 Критичний рівень безпеки! Високий ризик кібератаки.")
        has_critical = True
    if training < 30:
        messages.append("🟠 Недостатня підготовка курсантів. Продуктивність падає.")
    if budget < 50:
        messages.append("💸 Критично малий бюджет! Поповніть фінансування.")
        has_critical = True
    if staff < 5:
        messages.append("👥 Критично мало персоналу! Академія не може функціонувати.")
        has_critical = True

    if energy > 60 and security > 60 and training > 60 and core > 60 and budget >= 100 and staff >= 8:
        messages.append("🟢 Усі системи працюють стабільно.")
    elif not messages:
        messages.append("🟡 Системи працюють, але потребують контролю.")

    ai_label.config(text="\n".join(messages), fg="#ff4444" if has_critical else "white")


# =========================
# ПРОГНОЗ РИЗИКІВ
# =========================

def update_forecast():
    if not game_running:
        return
    risks = []
    has_critical = False

    if core < 40:
        chance = min(95, 100 - core)
        risks.append(f"💥 Збій CORE: {chance}%")
        if core < 30: has_critical = True
    if energy < 40:
        chance = min(95, 100 - energy)
        risks.append(f"⚡ Втрата живлення: {chance}%")
        if energy < 30: has_critical = True
    if security < 40:
        chance = min(95, 100 - security)
        risks.append(f"🔒 Потужна кібератака: {chance}%")
        if security < 30: has_critical = True
    if training < 40:
        chance = min(95, 100 - training)
        risks.append(f"📚 Провал поточної місії: {chance}%")
    if budget < 80:
        risks.append(f"💰 Банкрутство: {min(95, 100 - budget)}%")
        if budget < 40: has_critical = True
    if staff < 8:
        risks.append(f"👥 Колапс персоналу: {min(95, (8 - staff) * 12)}%")
        if staff < 4: has_critical = True

    if not risks:
        risks.append("🟢 Критичних ризиків не виявлено.")

    forecast_label.config(text="\n".join(risks), fg="#ff4444" if has_critical else "#ffb300")


# =========================
# КОМБО-БОНУСИ
# =========================

def check_combo():
    global energy, security, training, core, budget, staff
    global combo_active, combo_seconds

    threshold = diff_cfg["combo_threshold"]
    all_high = (
        energy   >= threshold and
        security >= threshold and
        training >= threshold and
        core     >= threshold
    )

    was_active = combo_active
    combo_active = all_high

    if all_high:
        combo_seconds += 1
        thr_color = {"easy": "#00ff66", "normal": "#ffd700", "hard": "#ff4444"}[difficulty_key]
        combo_label.config(
            text=f"⚡ КОМБО АКТИВНЕ! [{combo_seconds} сек]  Поріг: >{threshold}%  "
                 f"Бонус через: {5 - (combo_seconds % 5)} сек",
            fg=thr_color
        )

        if combo_seconds % 5 == 0:
            r = diff_cfg["combo_reward"]
            budget = clamp(budget + r["budget"], 0, 9999)
            staff  = clamp(staff  + r["staff"],  0, 99)
            bonus  = r["all_stats"]
            energy   = clamp(energy   + bonus)
            security = clamp(security + bonus)
            training = clamp(training + bonus)
            core     = clamp(core     + bonus)
            log(
                f"🌟 КОМБО x{combo_seconds // 5}! Всі показники >{threshold}% → "
                f"+{bonus}% до всіх систем, +{r['budget']} грн, +{r['staff']} ос."
            )
            combo_label.config(fg="white")
            root.after(300, lambda: combo_label.config(fg=thr_color) if combo_active else None)
    else:
        combo_seconds = 0
        if was_active:
            combo_label.config(
                text=f"💤 Комбо перервано! Тримайте всі показники вище {threshold}% для бонусів",
                fg="#555555"
            )
            log(f"💤 Комбо перервано! Тримайте всі показники вище {threshold}%")
        else:
            combo_label.config(
                text=f"💤 Комбо неактивне  (потрібно >{threshold}% скрізь)",
                fg="#555555"
            )


# =========================
# ВИПАДКОВІ КАТАСТРОФИ
# =========================

def random_disaster():
    global energy, security, training, core, budget, staff
    if not game_running:
        return

    event = random.choice(DISASTERS)
    log(event[0])

    mult = diff_cfg["disaster_mult"]
    energy   = clamp(energy   + int(event[1] * mult))
    security = clamp(security + int(event[2] * mult))
    training = clamp(training + int(event[3] * mult))
    core     = clamp(core     + int(event[4] * mult))
    budget   = clamp(budget   + int(event[5] * mult), 0, 9999)
    staff    = clamp(staff    + int(event[6] * mult), 0, 99)

    refresh_ui()
    update_ai()
    update_forecast()

    root.after(diff_cfg["disaster_interval"], random_disaster)


# =========================
# GAME OVER
# =========================

def game_over(message):
    global game_running
    game_running = False

    popup = tk.Toplevel(root)
    popup.title("КІНЕЦЬ ГРИ")
    popup.geometry("500x300")
    popup.configure(bg="#1e1e1e")
    popup.transient(root)
    popup.grab_set()

    tk.Label(popup, text="💥 GAME OVER", font=("Arial", 22, "bold"),
             fg="#ff4444", bg="#1e1e1e").pack(pady=12)
    tk.Label(popup, text=message, font=("Arial", 14),
             fg="white", bg="#1e1e1e").pack()
    tk.Label(popup, text=f"🏆 Академія протрималась {seconds_survived} сек",
             font=("Arial", 12), fg="gold", bg="#1e1e1e").pack(pady=4)
    tk.Label(popup, text=f"Складність: {diff_cfg['label']}",
             font=("Arial", 11), fg=diff_cfg["color"], bg="#1e1e1e").pack()
    tk.Label(popup, text=f"💰 Залишок бюджету: {budget} грн   👥 Персонал: {staff} ос.",
             font=("Arial", 10), fg="#aaaaaa", bg="#1e1e1e").pack(pady=4)

    btn_frame = tk.Frame(popup, bg="#1e1e1e")
    btn_frame.pack(pady=10)
    tk.Button(btn_frame, text="🔄 Грати знову", font=("Arial", 10, "bold"),
              bg="#333333", fg="white",
              command=lambda: [popup.destroy(), show_menu()]).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="❌ Вийти", font=("Arial", 10, "bold"),
              bg="#333333", fg="white",
              command=root.destroy).grid(row=0, column=1, padx=10)


# =========================
# ЩОСЕКУНДНЕ ОНОВЛЕННЯ
# =========================

def update_stats():
    global energy, security, training, core, seconds_survived, budget, staff, income_timer

    if not game_running:
        return

    seconds_survived += 1
    income_timer += 1
    d = diff_cfg["decay"]

    energy   = clamp(energy   - random.randint(*d["energy"]))
    security = clamp(security - random.randint(*d["security"]))
    training = clamp(training - random.randint(*d["training"]))
    core     = clamp(core     - random.randint(*d["core"]))

    if income_timer % 10 == 0:
        income = diff_cfg["budget_income"]
        budget = clamp(budget + income, 0, 9999)
        log(f"💰 Нараховано фінансування: +{income} грн (баланс: {budget} грн)")

    if income_timer % 15 == 0:
        regen = diff_cfg["staff_regen"]
        staff = clamp(staff + regen, 0, 99)
        if regen > 0:
            log(f"👥 Прийнято нових співробітників: +{regen} ос. (всього: {staff} ос.)")

    refresh_ui()
    update_ai()
    update_forecast()
    check_combo()

    if core <= 0:
        log("💥 КРИТИЧНО: STEPus-CORE повністю зруйновано!")
        game_over("STEPus-CORE зруйновано")
        return
    if energy <= 0:
        log("⚡ КРИТИЧНО: Академія повністю знеструмлена!")
        game_over("Відсутня енергія")
        return
    if security <= 0:
        log("🔒 КРИТИЧНО: Системи безпеки зламані!")
        game_over("Повна втрата безпеки")
        return
    if budget <= 0:
        log("💸 КРИТИЧНО: Академія збанкрутіла!")
        game_over("Банкрутство академії")
        return
    if staff <= 0:
        log("👥 КРИТИЧНО: Весь персонал покинув академію!")
        game_over("Колапс персоналу")
        return

    root.after(1000, update_stats)


# =========================
# ДІЇ ГРАВЦЯ
# =========================

def restore_server():
    global core, energy, budget, staff
    if not game_running: return
    if not can_afford(80, 2, "Відновити сервер"): return
    core = clamp(core + 20); energy = clamp(energy - 5)
    budget -= 80; staff = clamp(staff - 2, 0, 99)
    log("🔧 Дія: Сервер відновлено (+20 CORE, -5 Енергія, -80 грн, -2 ос.)")
    refresh_ui(); _update_btn_states()

def training_mission():
    global training, energy, budget, staff
    if not game_running: return
    if not can_afford(60, 3, "Провести тренування"): return
    training = clamp(training + 15); energy = clamp(energy - 8)
    budget -= 60; staff = clamp(staff - 3, 0, 99)
    log("🎓 Дія: Проведено тренування (+15 Навчання, -8 Енергія, -60 грн, -3 ос.)")
    refresh_ui(); _update_btn_states()

def increase_security():
    global security, energy, budget, staff
    if not game_running: return
    if not can_afford(50, 2, "Посилити захист"): return
    security = clamp(security + 20); energy = clamp(energy - 5)
    budget -= 50; staff = clamp(staff - 2, 0, 99)
    log("🛡 Дія: Перезапущено брандмауери (+20 Безпека, -50 грн, -2 ос.)")
    refresh_ui(); _update_btn_states()

def upgrade_system():
    global energy, core, budget
    if not game_running: return
    if not can_afford(40, 0, "Оновити систему"): return
    energy = clamp(energy + 20); core = clamp(core - 5)
    budget -= 40
    log("🚀 Дія: Оптимізовано енергомережу (+20 Енергія, -5 CORE, -40 грн)")
    refresh_ui(); _update_btn_states()

def hire_staff():
    global staff, budget
    if not game_running: return
    if not can_afford(120, 0, "Найняти персонал"): return
    staff = clamp(staff + 5, 0, 99); budget -= 120
    log("👔 Дія: Найнято нових співробітників (+5 ос., -120 грн)")
    refresh_ui(); _update_btn_states()

def emergency_funding():
    global budget, core
    if not game_running: return
    if core < 20:
        log("❌ Недостатньо CORE для аварійного фінансування (потрібно ≥20)")
        return
    core = clamp(core - 15); budget = clamp(budget + 200, 0, 9999)
    log("💵 Дія: Аварійне фінансування (+200 грн, -15 CORE)")
    refresh_ui(); _update_btn_states()


def _update_btn_states():
    costs = [
        (btn_restore,  80, 2),
        (btn_training, 60, 3),
        (btn_security, 50, 2),
        (btn_upgrade,  40, 0),
        (btn_hire,    120, 0),
        (btn_funding,   0, 0),
    ]
    for btn, cb, cs in costs:
        can = (budget >= cb) and (staff >= cs)
        btn.config(fg="white" if can else "#666666")


# =========================
# СТАРТ / МЕНЮ
# =========================

def start_game(chosen_difficulty):
    global energy, security, training, core, budget, staff
    global game_running, seconds_survived, difficulty_key, diff_cfg, income_timer
    global combo_active, combo_seconds

    difficulty_key = chosen_difficulty
    diff_cfg = DIFFICULTY_SETTINGS[chosen_difficulty]

    menu_frame.pack_forget()
    game_frame.pack(fill="both", expand=True)

    s = diff_cfg["start"]
    energy   = s["energy"];  security = s["security"]
    training = s["training"]; core    = s["core"]
    budget   = s["budget"];  staff    = s["staff"]
    seconds_survived = 0
    income_timer = 0
    combo_active = False
    combo_seconds = 0
    game_running = True

    event_log.configure(state="normal")
    event_log.delete("1.0", tk.END)
    event_log.configure(state="disabled")

    diff_badge.config(text=f"Складність: {diff_cfg['label']}", fg=diff_cfg["color"])
    combo_label.config(
        text=f"💤 Комбо неактивне  (потрібно >{diff_cfg['combo_threshold']}% скрізь)",
        fg="#555555"
    )

    log(f"🟢 Систему Digital Twin STEPus запущено | {diff_cfg['label']}")
    log(f"💰 Стартовий бюджет: {budget} грн  |  👥 Персонал: {staff} ос.")
    log("⚠ Системи піддаються природному зносу та деградації")

    refresh_ui(); update_ai(); update_forecast(); _update_btn_states()

    root.after(1000, update_stats)
    root.after(diff_cfg["disaster_interval"], random_disaster)


def show_menu():
    game_frame.pack_forget()
    menu_frame.pack(fill="both", expand=True)

def back_to_menu():
    global game_running
    game_running = False
    show_menu()


# =========================
# ІНТЕРФЕЙС
# =========================

root = tk.Tk()
root.title("Digital Twin STEPus v2.4")
root.geometry("980x1020")
root.configure(bg="#1e1e1e")

style = ttk.Style()
style.theme_use("clam")
style.configure("green.Horizontal.TProgressbar",  background="#00ff66")
style.configure("yellow.Horizontal.TProgressbar", background="#ffd700")
style.configure("red.Horizontal.TProgressbar",    background="#ff4444")

# ──────────────────────────────────────────────
# МЕНЮ
# ──────────────────────────────────────────────
menu_frame = tk.Frame(root, bg="#1e1e1e")
menu_frame.pack(fill="both", expand=True)

tk.Label(menu_frame, text="🛰 DIGITAL TWIN STEPUS",
         font=("Arial", 28, "bold"), bg="#1e1e1e", fg="cyan").pack(pady=(50, 5))
tk.Label(menu_frame, text="Симулятор управління цифровою академією",
         font=("Arial", 13), bg="#1e1e1e", fg="#aaaaaa").pack(pady=(0, 40))
tk.Label(menu_frame, text="ОБЕРІТЬ РІВЕНЬ СКЛАДНОСТІ",
         font=("Arial", 16, "bold"), bg="#1e1e1e", fg="white").pack(pady=(0, 20))

cards_frame = tk.Frame(menu_frame, bg="#1e1e1e")
cards_frame.pack()

for key, cfg in DIFFICULTY_SETTINGS.items():
    card = tk.Frame(cards_frame, bg="#2a2a2a", bd=2, relief="groove", padx=20, pady=20)
    card.pack(side="left", padx=15, pady=10, ipadx=10, ipady=10)

    tk.Label(card, text=cfg["label"], font=("Arial", 18, "bold"),
             bg="#2a2a2a", fg=cfg["color"]).pack(pady=(0, 6))
    tk.Label(card, text=cfg["description"], font=("Arial", 9),
             bg="#2a2a2a", fg="#cccccc", wraplength=165, justify="center").pack(pady=(0, 8))

    s = cfg["start"]
    r = cfg["combo_reward"]
    stats_text = (
        f"⚡ Енергія:    {s['energy']}%\n"
        f"🔒 Безпека:   {s['security']}%\n"
        f"📚 Навчання:  {s['training']}%\n"
        f"🧠 CORE:      {s['core']}%\n"
        f"💰 Бюджет:   {s['budget']} грн\n"
        f"👥 Персонал: {s['staff']} ос.\n"
        f"🌟 Комбо:    >{cfg['combo_threshold']}%  →  "
        f"+{r['all_stats']}% / +{r['budget']}грн / +{r['staff']}ос."
    )
    tk.Label(card, text=stats_text, font=("Courier", 9),
             bg="#2a2a2a", fg="#aaaaaa", justify="left").pack(pady=(0, 12))

    tk.Button(card, text="▶ СТАРТ", font=("Arial", 12, "bold"),
              bg=cfg["color"], fg="#1e1e1e", width=14, cursor="hand2",
              activebackground=cfg["color"],
              command=lambda k=key: start_game(k)).pack()

tk.Label(menu_frame, text="v2.4 | Digital Twin STEPus",
         font=("Arial", 9), bg="#1e1e1e", fg="#555555").pack(side="bottom", pady=10)

# ──────────────────────────────────────────────
# ІГРОВИЙ ФРЕЙМ
# ──────────────────────────────────────────────
game_frame = tk.Frame(root, bg="#1e1e1e")

top_bar = tk.Frame(game_frame, bg="#1e1e1e")
top_bar.pack(fill="x", padx=20, pady=(10, 0))
tk.Label(top_bar, text="🛰 DIGITAL TWIN STEPUS",
         font=("Arial", 20, "bold"), bg="#1e1e1e", fg="cyan").pack(side="left")
diff_badge = tk.Label(top_bar, text="", font=("Arial", 11, "bold"), bg="#1e1e1e", fg="white")
diff_badge.pack(side="right", padx=10)
tk.Button(top_bar, text="☰ Меню", font=("Arial", 10), bg="#333333", fg="white",
          command=back_to_menu).pack(side="right")

timer_label = tk.Label(game_frame, text="🏆 Час виживання: 0 сек",
                       font=("Arial", 13, "bold"), bg="#1e1e1e", fg="gold")
timer_label.pack()

# Системні шкали
for (lname, bname) in [("energy_label","energy_bar"), ("security_label","security_bar"),
                        ("training_label","training_bar"), ("core_label","core_bar")]:
    lbl = tk.Label(game_frame, font=("Arial", 11, "bold"), bg="#1e1e1e", fg="white")
    lbl.pack(pady=(6, 0))
    bar = ttk.Progressbar(game_frame, length=580, maximum=100)
    bar.pack(pady=2)
    globals()[lname] = lbl
    globals()[bname] = bar

# Ресурси
res_frame = tk.Frame(game_frame, bg="#252525", bd=1, relief="groove")
res_frame.pack(fill="x", padx=40, pady=(10, 4))
tk.Label(res_frame, text="📦 РЕСУРСИ АКАДЕМІЇ",
         font=("Arial", 11, "bold"), bg="#252525", fg="cyan").pack(pady=(6, 2))
res_bars = tk.Frame(res_frame, bg="#252525")
res_bars.pack(padx=20, pady=(0, 8))

budget_label = tk.Label(res_bars, text="💰 Бюджет: 0 грн",
                         font=("Arial", 11, "bold"), bg="#252525", fg="white", width=22, anchor="w")
budget_label.grid(row=0, column=0, padx=(0, 10))
budget_bar = ttk.Progressbar(res_bars, length=340, maximum=500)
budget_bar.grid(row=0, column=1)

staff_label = tk.Label(res_bars, text="👥 Персонал: 0 ос.",
                        font=("Arial", 11, "bold"), bg="#252525", fg="white", width=22, anchor="w")
staff_label.grid(row=1, column=0, padx=(0, 10), pady=(6, 0))
staff_bar = ttk.Progressbar(res_bars, length=340, maximum=50)
staff_bar.grid(row=1, column=1, pady=(6, 0))

# Комбо-індикатор
combo_frame = tk.Frame(game_frame, bg="#1a1a2e", bd=1, relief="groove")
combo_frame.pack(fill="x", padx=40, pady=(4, 4))
combo_header = tk.Frame(combo_frame, bg="#1a1a2e")
combo_header.pack(fill="x", padx=15, pady=(6, 2))
tk.Label(combo_header, text="🌟 КОМБО-БОНУС",
         font=("Arial", 11, "bold"), bg="#1a1a2e", fg="#a78bfa").pack(side="left")
tk.Label(combo_header, text="Легко: >60%  |  Норм: >70%  |  Важко: >80%",
         font=("Arial", 8), bg="#1a1a2e", fg="#555577").pack(side="right")
combo_label = tk.Label(combo_frame, text="💤 Комбо неактивне",
                        font=("Arial", 10, "bold"), bg="#1a1a2e", fg="#555555")
combo_label.pack(pady=(2, 8))

# Кнопки дій
tk.Label(game_frame, text="⚙ ДІЇ ОПЕРАТОРА",
         font=("Arial", 11, "bold"), bg="#1e1e1e", fg="#aaaaaa").pack(pady=(8, 2))

buttons = tk.Frame(game_frame, bg="#1e1e1e")
buttons.pack(pady=4)

btn_style = {"width": 26, "font": ("Arial", 10, "bold"), "bg": "#333333",
             "fg": "white", "activebackground": "cyan"}

btn_restore  = tk.Button(buttons, text="🔧 Відновити сервер\n[80 грн | 2 ос.]",   command=restore_server,    **btn_style)
btn_training = tk.Button(buttons, text="🎓 Провести тренування\n[60 грн | 3 ос.]", command=training_mission,  **btn_style)
btn_security = tk.Button(buttons, text="🛡 Посилити захист\n[50 грн | 2 ос.]",    command=increase_security, **btn_style)
btn_upgrade  = tk.Button(buttons, text="🚀 Оновити систему\n[40 грн | 0 ос.]",    command=upgrade_system,    **btn_style)
btn_hire     = tk.Button(buttons, text="👔 Найняти персонал\n[120 грн | +5 ос.]", command=hire_staff,        **btn_style)
btn_funding  = tk.Button(buttons, text="💵 Аварійне фінансування\n[-15 CORE | +200 грн]", command=emergency_funding, **btn_style)

btn_restore .grid(row=0, column=0, padx=8, pady=4)
btn_training.grid(row=0, column=1, padx=8, pady=4)
btn_security.grid(row=1, column=0, padx=8, pady=4)
btn_upgrade .grid(row=1, column=1, padx=8, pady=4)
btn_hire    .grid(row=2, column=0, padx=8, pady=4)
btn_funding .grid(row=2, column=1, padx=8, pady=4)

# AI-аналітик
tk.Label(game_frame, text="🤖 AI-АНАЛІТИК СИСТЕМИ",
         font=("Arial", 12, "bold"), bg="#1e1e1e", fg="cyan").pack(pady=(6, 0))
ai_label = tk.Label(game_frame, text="", font=("Arial", 10), justify="left",
                    wraplength=900, bg="#1e1e1e", fg="white")
ai_label.pack(pady=3)

# Прогноз ризиків
tk.Label(game_frame, text="📈 ОЦІНКА РИЗИКІВ НАЙБЛИЖЧИХ ХВИЛИН",
         font=("Arial", 12, "bold"), bg="#1e1e1e", fg="orange").pack()
forecast_label = tk.Label(game_frame, text="", font=("Arial", 10), justify="left",
                           wraplength=900, bg="#1e1e1e", fg="white")
forecast_label.pack(pady=3)

# Журнал подій
tk.Label(game_frame, text="📜 ЖУРНАЛ ПОДІЙ СИСТЕМИ",
         font=("Arial", 12, "bold"), bg="#1e1e1e", fg="white").pack()
event_log = tk.Text(game_frame, width=110, height=7, bg="black", fg="#00ff66",
                    font=("Courier", 9), insertbackground="white", state="disabled")
event_log.pack(pady=6, padx=10)

root.mainloop()