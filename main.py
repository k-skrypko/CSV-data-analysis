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


def select_column():
    df = pd.read_csv(select_csv_file())
    print(df.columns.tolist())

    selected_column = input("Введіть назву колонки: ")

    if selected_column not in df.columns.tolist():
        raise Exception("Неправильна назва колонки.")

    return selected_column


def average_number():
    pass


def min_number():
    pass


def max_number():
    pass


def main():
    select_column()
    operation = input("Оберіть бажану операцію (avg/min/max): ")

    if operation == "avg":
        average_number()

    elif operation == "min":
        min_number()

    elif operation == "max":
        max_number()

    else:
        raise Exception("Неправильно обрана операція.")
