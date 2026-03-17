import os
import pandas as pd
from datetime import datetime


def save_result(df_result, operation: str, column: str, source_file: str):
    """
    Зберігає результат операції у текстовий файл в папку results/.

    Параметри:
        df_result  — результат (число або DataFrame)
        operation  — назва операції: avg / min / max / filter / sort / top10
        column     — назва колонки з якою працювали
        source_file — шлях до оригінального CSV файлу
    """

    # ── 1. Створюємо папку results ───────────────────────
    os.makedirs("results", exist_ok=True)

    # ── 2. Формуємо назву файлу ────────────────────────────────────────────
    base_name = os.path.splitext(os.path.basename(source_file))[0]

    # Формуємо назву: sales_avg_Ціна.txt
    file_name = f"{base_name}_{operation}_{column}.txt"
    file_path = os.path.join("results", file_name)

    # ── 3. Формуємо вміст файлу ────────────────────────────────────────────
    timestamp = datetime.now().strftime("%d.%m.%Y %H:%M:%S")

    lines = [
        "=" * 50,
        f"  Результат аналізу CSV даних",
        "=" * 50,
        f"  Дата та час : {timestamp}",
        f"  Файл        : {os.path.basename(source_file)}",
        f"  Операція    : {operation.upper()}",
        f"  Колонка     : {column}",
        "=" * 50,
        "",
    ]

    # Якщо результат — DataFrame (filter / sort / top10)
    if isinstance(df_result, pd.DataFrame):
        lines.append(f"Кількість рядків у результаті: {len(df_result)}")
        lines.append("")
        lines.append(df_result.to_string(index=False))
    else:
        # Якщо результат — просте число (avg / min / max)
        lines.append(f"Результат: {df_result}")

    lines.append("")
    lines.append("=" * 50)

    # ── 4. Записуємо у файл ────────────────────────────────────────────────
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("\n".join(lines))

    print(f"💾 Результат збережено у файл: results/{file_name}")
    return file_path