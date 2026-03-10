import pandas as pd
import tkinter as tk
from tkinter import filedialog


def select_csv_file():
    selected_file = None

    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Оберіть CSV файл",
        filetypes=[("CSV файли", "*.csv")]
    )

    selected_file = file_path

    return selected_file


def select_column(df):
    print(df.columns.tolist())

    selected_column = input("Введіть назву колонки: ")

    if selected_column not in df.columns.tolist():
        raise Exception("Неправильна назва колонки.")

    return selected_column


def average_number(column, df):
    print(f"Середнє значення для колонки {column}:")
    return round(df[column].mean(), 1)


def min_number(column, df):
    print(f"Мінімальне значення для колонки {column}:")
    return df[column].min()


def max_number(column, df):
    print(f"Максимальне значення для колонки {column}:")
    return df[column].max()


def main():
    df = pd.read_csv(select_csv_file())
    selected_culumn = select_column(df)

    operation = input("Оберіть бажану операцію (avg/min/max): ")

    if operation == "avg":
        return average_number(selected_culumn, df)

    elif operation == "min":
        return min_number(selected_culumn, df)

    elif operation == "max":
        return max_number(selected_culumn, df)

    else:
        raise Exception("Неправильно обрана операція.")
