import cv2
import numpy as np


def overlay_image(background, overlay, x, y, width, height):
    """
    Функція для накладання зображення з прозорістю (PNG) на фон.
    """
    # Змінюємо розмір маски під цільові координати
    overlay_resized = cv2.resize(overlay, (width, height))

    # Якщо маска не має альфа-каналу (прозорості), додаємо його або використовуємо як є
    if overlay_resized.shape[2] == 3:
        overlay_resized = cv2.cvtColor(overlay_resized, cv2.COLOR_BGR2BGRA)

    # Вирізаємо область інтересу (ROI) на фоновому зображенні
    roi = background[y:y + height, x:x + width]

    # Розділяємо канали маски
    overlay_rgb = overlay_resized[:, :, :3]
    alpha = overlay_resized[:, :, 3] / 255.0
    alpha_inv = 1.0 - alpha

    # Поканальне змішування фону та маски
    for c in range(0, 3):
        roi[:, :, c] = (alpha * overlay_rgb[:, :, c] + alpha_inv * roi[:, :, c])

    background[y:y + height, x:x + width] = roi


# 1. Завантаження каскадів Хаара (передвстановлені моделі нейромережевого типу)
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# 2. Завантаження оригінального фото та елементів маски
# Замініть шляхи до файлів на ваші власні, якщо вони відрізняються
img_man = cv2.imread('image_090bd3.jpg')
img_mustache = cv2.imread('image_090870.png', cv2.IMREAD_UNCHANGED)  # Завантажуємо з альфа-каналом
img_glasses = cv2.imread('image_090bb3.jpg', cv2.IMREAD_UNCHANGED)

# Створюємо копію для результату
result_img = img_man.copy()

# Перетворюємо в сірий колір для коректної роботи детектора
gray = cv2.cvtColor(img_man, cv2.COLOR_BGR2GRAY)

# 3. Пошук першого патерну: Обличчя (для позиціонування вусів)
faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(100, 100))

for (x, y, w, h) in faces:
    # Область для пошуку очей всередині обличчя
    roi_gray = gray[y:y + h, x:x + w]

    # Розрахунок координат для вусів (приблизно посередині нижньої частини обличчя)
    mustache_width = int(w * 0.55)
    mustache_height = int(mustache_width * (img_mustache.shape[0] / img_mustache.shape[1]))
    mustache_x = x + int((w - mustache_width) / 2)
    mustache_y = y + int(h * 0.62)

    # Накладаємо вуса
    overlay_image(result_img, img_mustache, mustache_x, mustache_y, mustache_width, mustache_height)

    # 4. Пошук другого патерну: Очі (для позиціонування окулярів)
    eyes = eye_cascade.detectMultiScale(roi_gray, scaleFactor=1.1, minNeighbors=10, minSize=(30, 30))

    if len(eyes) >= 2:
        # Сортуємо знайдені очі за координатою X, щоб чітко знайти ліве і праве
        eyes = sorted(eyes, key=lambda e: e[0])

        ex1, ey1, ew1, eh1 = eyes[0]
        ex2, ey2, ew2, eh2 = eyes[1]

        # Обчислюємо загальну ширину та висоту для окулярів, які мають покрити обидва ока
        glasses_x = x + ex1 - int(ew1 * 0.3)
        glasses_y = y + min(ey1, ey2) - int(eh1 * 0.2)
        glasses_width = (ex2 + ew2) - ex1 + int(ew1 * 0.6)
        glasses_height = int(glasses_width * (img_glasses.shape[0] / img_glasses.shape[1]))

        # Обробка чорного фону окулярів (робимо його прозорим, якщо зображення JPG)
        if img_glasses.shape[2] == 3:
            # Створюємо альфа-канал на основі яскравості: все, що майже чорне, стає прозорим
            tmp = cv2.cvtColor(img_glasses, cv2.COLOR_BGR2GRAY)
            _, alpha = cv2.threshold(tmp, 20, 255, cv2.THRESH_BINARY)
            b, g, r = cv2.split(img_glasses)
            img_glasses_rgba = cv2.merge([b, g, r, alpha])
        else:
            img_glasses_rgba = img_glasses

        # Накладаємо окуляри
        overlay_image(result_img, img_glasses_rgba, glasses_x, glasses_y, glasses_width, glasses_height)

# 5. Збереження та відображення результату
cv2.imwrite('final_result.jpg', result_img)
cv2.imshow('Result', result_img)
cv2.waitKey(0)
cv2.destroyAllWindows()