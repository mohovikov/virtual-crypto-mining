from datetime import datetime, timezone
import hashlib
import random


def get_random_formula():
    now = datetime.now(timezone.utc)
    yyyy, mm, dd, HH, MM, ss = now.year, now.month, now.day, now.hour, now.minute, now.second

    formulas = [
        lambda: yyyy / (((dd + mm) * (HH + MM)) / (ss or 1)),
        lambda: (yyyy + dd) * (HH + 1) / (mm + ss + 1),
        lambda: ((yyyy % 100) * (dd + mm)) + (HH * ss),
        lambda: (yyyy / (mm + 1)) + (dd * HH) - ss,
        lambda: (((yyyy + mm) * (dd + 1)) % (HH + ss + 1)) + 1,
    ]

    return random.choice(formulas)

def generate_difficulty():
    formula = get_random_formula()
    difficulty = formula()

    # Страховка: только положительное число
    difficulty = abs(int(difficulty))

    # Шоб число не улетело в космос
    difficulty = difficulty % 500

    # Случайный коэффициент
    difficulty = int(difficulty * random.uniform(0.8, 1.2))

    # Обрезка в диапазон
    return max(10, min(difficulty, 300))

def generate_price() -> float:
    now = datetime.now(timezone.utc).isoformat()
    
    # Получить большого уникального числа
    h = int(hashlib.sha256(now.encode()).hexdigest(), 16)
    
    # Фиксация seed от хэша времени
    random.seed(h)

    noise = random.uniform(0.7, 1.3)
    
    # Базовая формула: цена = сложность * 5 * шум
    base = generate_difficulty() * 5
    price = base * noise
    
    return round(price, 2)