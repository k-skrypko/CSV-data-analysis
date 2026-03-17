import pandas as pd
import os
import sys

# Підключаємо функції з main.py та validator.py
sys.path.insert(0, os.path.dirname(__file__))
from main import average_number, min_number, max_number, top_10, filter_by_value
from validator import validate_csv


# ── ТЕСТ 1: Середнє значення ────────────────────────────────────────────────
def test_average_number():
    """average_number повинна повертати правильне середнє значення"""
    df = pd.DataFrame({'Ціна': [10.0, 20.0, 30.0]})
    result = average_number('Ціна', df)
    assert result == 20.0, f"Очікувалось 20.0, отримано {result}"


# ── ТЕСТ 2: Мінімальне значення ─────────────────────────────────────────────
def test_min_number():
    """min_number повинна повертати найменше значення в колонці"""
    df = pd.DataFrame({'Бал': [55.0, 78.0, 92.0, 43.0]})
    result = min_number('Бал', df)
    assert result == 43.0, f"Очікувалось 43.0, отримано {result}"


# ── ТЕСТ 3: Максимальне значення ────────────────────────────────────────────
def test_max_number():
    """max_number повинна повертати найбільше значення в колонці"""
    df = pd.DataFrame({'Температура': [-5.0, 0.0, 25.0, 18.0]})
    result = max_number('Температура', df)
    assert result == 25.0, f"Очікувалось 25.0, отримано {result}"


# ── ТЕСТ 4: Топ-10 ──────────────────────────────────────────────────────────
def test_top_10():
    """top_10 повинна повертати не більше 10 рядків, відсортованих за спаданням"""
    # Створюємо таблицю з 15 рядків
    df = pd.DataFrame({'Продано': list(range(1, 16))})
    result = top_10('Продано', df)

    # Перевіряємо що повернулось рівно 10 рядків
    assert len(result) == 10, f"Очікувалось 10 рядків, отримано {len(result)}"

    # Перевіряємо що перший рядок — найбільший (15)
    assert result.iloc[0]['Продано'] == 15, "Перший рядок повинен бути найбільшим"


# ── ТЕСТ 5: Валідація — порожній файл ───────────────────────────────────────
def test_validate_empty_dataframe():
    """validate_csv повинна повертати False для порожнього DataFrame"""
    df = pd.DataFrame()
    result = validate_csv(df)
    assert result == False, "Порожній DataFrame повинен не пройти валідацію"


# ── ТЕСТ 6: Валідація — нормальні дані ──────────────────────────────────────
def test_validate_correct_dataframe():
    """validate_csv повинна повертати True для коректних даних"""
    df = pd.DataFrame({
        'Назва': ['Товар А', 'Товар Б', 'Товар В'],
        'Ціна': [100.0, 200.0, 300.0],
        'Кількість': [5, 10, 15]
    })
    result = validate_csv(df)
    assert result == True, "Коректний DataFrame повинен пройти валідацію"


# ── Запуск тестів вручну (без pytest) ───────────────────────────────────────
if __name__ == "__main__":
    tests = [
        ("Тест 1 — average_number", test_average_number),
        ("Тест 2 — min_number",     test_min_number),
        ("Тест 3 — max_number",     test_max_number),
        ("Тест 4 — top_10",         test_top_10),
        ("Тест 5 — валідація порожнього DataFrame", test_validate_empty_dataframe),
        ("Тест 6 — валідація коректного DataFrame", test_validate_correct_dataframe),
    ]

    passed = 0
    failed = 0

    print("\n" + "="*50)
    print("  Запуск unit-тестів")
    print("="*50)

    for name, test_func in tests:
        try:
            test_func()
            print(f"✅ {name}")
            passed += 1
        except AssertionError as e:
            print(f"❌ {name} — {e}")
            failed += 1
        except Exception as e:
            print(f"❌ {name} — Несподівана помилка: {e}")
            failed += 1

    print("="*50)
    print(f"  Результат: {passed} пройшло, {failed} провалилось")
    print("="*50)