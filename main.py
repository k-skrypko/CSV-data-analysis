import os
import pandas as pd
import sys

# ── Підключаємо модулі Учасника B ──────────────────────────────────────────
from validator import validate_csv
from saver import save_result
from visualizer import build_chart


def select_csv_file():
    print("\nДоступні файли: sales.csv, students.csv, weather_2025.csv")
    while True:
        file_path = input("Введіть назву CSV файлу: ").strip()

        if os.path.exists(file_path):
            return file_path

        print(f"❌ Файл '{file_path}' не знайдено. Перевірте назву і спробуйте ще раз.")


def select_column(df):
    print(f"\nДоступні колонки: {', '.join(df.columns)}")

    while True:
        selected_column = input("Введіть назву колонки: ").strip()

        if selected_column in df.columns:
            return selected_column

        print("❌ Помилка: Такої колонки немає в таблиці. Перевірте правильність написання.")


def average_number(column, df):
    return round(df[column].mean(), 1)


def min_number(column, df):
    return df[column].min()


def max_number(column, df):
    return df[column].max()


def filter_by_value(column, df):
    while True:
        value = input("Введіть значення для фільтрації: ").strip()

        if pd.api.types.is_numeric_dtype(df[column]):
            try:
                num_value = float(value)
                return df[df[column] == num_value]
            except ValueError:
                print("❌ Помилка: Ця колонка містить числа. Будь ласка, введіть числове значення.")
        else:
            return df[df[column].str.contains(value, case=False, na=False)]


def sort_by_column(column, df):
    while True:
        order = input("Оберіть порядок сортування (asc - зростання / desc - спадання): ").strip().lower()

        if order in ['asc', 'desc']:
            ascending = order == "asc"
            return df.sort_values(by=column, ascending=ascending)

        print("❌ Помилка: Введіть 'asc' або 'desc'.")


def top_10(column, df):
    return df.sort_values(by=column, ascending=False).head(10)


def ask_to_save(result, operation, column, file_path):
    """Запитує користувача чи зберегти результат у файл."""
    answer = input("\n💾 Зберегти результат у файл? (y/n): ").strip().lower()
    if answer == 'y':
        save_result(result, operation, column, file_path)


def main():
    print("--- Програма для аналізу CSV даних ---")

    file_path = select_csv_file()
    try:
        df = pd.read_csv(file_path)
    except Exception as e:
        print(f"❌ Сталася помилка при читанні файлу: {e}")
        return

    print("\n✅ Дані успішно завантажено! Ось перші 5 рядків:")
    print(df.head())

    # ── Валідація даних (Учасник B) ─────────────────────────────────────────
    validate_csv(df, file_path)

    # ── Графік (Учасник B) ───────────────────────────────────────────────────
    answer = input("\n📊 Побудувати графік для цього файлу? (y/n): ").strip().lower()
    if answer == 'y':
        build_chart(df, file_path)

    # Головний цикл програми
    while True:
        print("\n" + "="*40)
        selected_column = select_column(df)

        while True:
            operation = input("\nОберіть операцію (avg/min/max/filter/sort/top10) або 'exit' для виходу: ").strip().lower()

            if operation == "exit":
                print("Дякую за використання програми! Гарного дня.")
                return

            if operation in ["avg", "min", "max", "filter", "sort", "top10"]:
                break
            print("❌ Помилка: Невідома операція. Оберіть зі списку.")

        print("\n--- Результат ---")

        try:
            if operation == "avg":
                if pd.api.types.is_numeric_dtype(df[selected_column]):
                    result = average_number(selected_column, df)
                    print(f"Середнє значення: {result}")
                    ask_to_save(result, operation, selected_column, file_path)
                else:
                    print("❌ Помилка: Середнє значення можна порахувати лише для числових колонок.")

            elif operation == "min":
                num_value = min_number(selected_column, df)
                result = df[df[selected_column] == num_value]
                print(result)
                ask_to_save(result, operation, selected_column, file_path)

            elif operation == "max":
                num_value = max_number(selected_column, df)
                result = df[df[selected_column] == num_value]
                print(result)
                ask_to_save(result, operation, selected_column, file_path)

            elif operation == "filter":
                result = filter_by_value(selected_column, df)
                if result.empty:
                    print("Не знайдено жодного рядка з таким значенням.")
                else:
                    print(result)
                    ask_to_save(result, operation, selected_column, file_path)

            elif operation == "sort":
                result = sort_by_column(selected_column, df)
                print(result)
                ask_to_save(result, operation, selected_column, file_path)

            elif operation == "top10":
                result = top_10(selected_column, df)
                print(result)
                ask_to_save(result, operation, selected_column, file_path)

        except Exception as e:
            print(f"❌ Сталася помилка під час обробки: {e}")


if __name__ == "__main__":
    main()