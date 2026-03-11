import pandas as pd
import tkinter as tk
from tkinter import filedialog


def select_csv_file():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(
        title="Оберіть CSV файл",
        filetypes=[("CSV файли", "*.csv")]
    )

    if not file_path:
        raise Exception("Файл не обрано.")

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
    return df[column].min()


def max_number(column, df):
    return df[column].max()


def main():
    df = pd.read_csv(select_csv_file())
    selected_column = select_column(df)

    operation = input("Оберіть бажану операцію (avg/min/max): ")

    if operation == "avg":
        print(average_number(selected_column, df))

    elif operation == "min":
        num_value = min_number(selected_column, df)
        print(df.query(f"{selected_column} == {num_value}"))

    elif operation == "max":
        num_value = max_number(selected_column, df)
        print(df.query(f"{selected_column} == {num_value}"))

    else:
        raise Exception("Неправильно обрана операція.")
