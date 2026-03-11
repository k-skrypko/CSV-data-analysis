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

    return file_path


def select_column(df):
    selected_column = input("Введіть назву колонки: ")

    if selected_column not in df.columns.tolist():
        raise Exception("Неправильна назва колонки.")

    return selected_column


def average_number(column, df):
    return round(df[column].mean(), 1)


def min_number(column, df):
    return df[column].min()


def max_number(column, df):
    return df[column].max()


def filter_by_value(column, df):
    value = input("Введіть значення для фільтрації: ")

    if pd.api.types.is_numeric_dtype(df[column]):
        result = df[df[column] == float(value)]
    else:
        result = df[df[column].str.contains(value, case=False, na=False)]

    return result


def sort_by_column(column, df):
    order = input("Оберіть порядок сортування (asc/desc): ")
    ascending = order == "asc"

    return df.sort_values(by=column, ascending=ascending)


def top_10(column, df):
    return df.sort_values(by=column, ascending=False).head(10)


def main():
    df = pd.read_csv(select_csv_file())
    print(df)
    selected_column = select_column(df)

    operation = input("Оберіть бажану операцію (avg/min/max/filter/sort/top10): ")

    if operation == "avg":
        print(f"Середнє значення для колонки {selected_column}:")
        print(average_number(selected_column, df))

    elif operation == "min":
        num_value = min_number(selected_column, df)
        print(df.query(f"{selected_column} == {num_value}"))

    elif operation == "max":
        num_value = max_number(selected_column, df)
        print(df.query(f"{selected_column} == {num_value}"))

    elif operation == "filter":
        result = filter_by_value(selected_column, df)
        if result.empty:
            print("Немає рядків з таким значенням.")
        else:
            print(result)
    
    elif operation == "sort":
        print(sort_by_column(selected_column, df))
    
    elif operation == "top10":
        print(top_10(selected_column, df))

    else:
        raise Exception("Неправильно обрана операція.")
