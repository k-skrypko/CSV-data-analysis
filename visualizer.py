import os
import pandas as pd
import matplotlib
matplotlib.use('Agg')  # Зберігаємо у файл без відкриття вікна
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# ── Загальні налаштування стилю ─────────────────────────────────────────────
plt.rcParams['font.family'] = 'DejaVu Sans'
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 11


def save_chart(fig, filename: str):
    """Зберігає графік у папку results/charts/"""
    os.makedirs("results/charts", exist_ok=True)
    path = f"results/charts/{filename}"
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"📊 Графік збережено: {path}")
    return path


# ────────────────────────────────────────────────────────────────────────────
# ГРАФІК 1 — sales.csv: Топ-10 товарів за кількістю продажів
# ────────────────────────────────────────────────────────────────────────────
def plot_sales(df: pd.DataFrame):
    top10 = df.sort_values('Продано', ascending=False).head(10)

    fig, ax = plt.subplots(figsize=(12, 6))

    bars = ax.barh(
        top10['Назва_товару'],
        top10['Продано'],
        color='steelblue',
        edgecolor='white'
    )

    # Підписи значень на кінці кожного стовпця
    for bar in bars:
        width = bar.get_width()
        ax.text(
            width + 1, bar.get_y() + bar.get_height() / 2,
            str(int(width)),
            va='center', ha='left', fontsize=9
        )

    ax.set_title('Топ-10 товарів за кількістю продажів', fontweight='bold', pad=15)
    ax.set_xlabel('Кількість продажів')
    ax.set_ylabel('Товар')
    ax.invert_yaxis()  # Найбільший зверху
    ax.grid(axis='x', linestyle='--', alpha=0.5)
    fig.tight_layout()

    return save_chart(fig, 'sales_top10.png')


# ────────────────────────────────────────────────────────────────────────────
# ГРАФІК 2 — students.csv: Кількість студентів по спеціальностях
# ────────────────────────────────────────────────────────────────────────────
def plot_students(df: pd.DataFrame):
    counts = df['Спеціальність'].value_counts()

    colors = [
        '#4C72B0', '#DD8452', '#55A868', '#C44E52',
        '#8172B2', '#937860', '#DA8BC3', '#8C8C8C',
        '#CCB974', '#64B5CD'
    ]

    fig, ax = plt.subplots(figsize=(8, 8))

    wedges, texts, autotexts = ax.pie(
        counts.values,
        labels=counts.index,
        autopct='%1.1f%%',
        colors=colors[:len(counts)],
        startangle=140,
        pctdistance=0.82
    )

    # Робимо підписи трохи більшими
    for text in texts:
        text.set_fontsize(10)
    for autotext in autotexts:
        autotext.set_fontsize(9)
        autotext.set_fontweight('bold')

    ax.set_title('Розподіл студентів по спеціальностях', fontweight='bold', pad=20)
    fig.tight_layout()

    return save_chart(fig, 'students_specialties.png')


# ────────────────────────────────────────────────────────────────────────────
# ГРАФІК 3 — weather_2025.csv: Середня температура по місяцях
# ────────────────────────────────────────────────────────────────────────────
def plot_weather(df: pd.DataFrame):
    # Рахуємо середню температуру по кожному місяцю
    monthly = df.groupby('Місяць', sort=False)['Температура'].mean().round(1)

    # Правильний порядок місяців
    month_order = [
        'Січень', 'Лютий', 'Березень', 'Квітень', 'Травень', 'Червень',
        'Липень', 'Серпень', 'Вересень', 'Жовтень', 'Листопад', 'Грудень'
    ]
    monthly = monthly.reindex([m for m in month_order if m in monthly.index])

    fig, ax = plt.subplots(figsize=(12, 5))

    # Лінія температури
    ax.plot(
        monthly.index, monthly.values,
        color='tomato', linewidth=2.5,
        marker='o', markersize=7, markerfacecolor='white',
        markeredgewidth=2, markeredgecolor='tomato'
    )

    # Заливка під лінією
    ax.fill_between(monthly.index, monthly.values, alpha=0.15, color='tomato')

    # Підписи значень над кожною точкою
    for x, y in zip(monthly.index, monthly.values):
        ax.annotate(
            f'{y}°',
            (x, y),
            textcoords="offset points",
            xytext=(0, 10),
            ha='center', fontsize=9, color='tomato', fontweight='bold'
        )

    # Горизонтальна лінія нуля
    ax.axhline(0, color='gray', linewidth=0.8, linestyle='--', alpha=0.6)

    ax.set_title('Середня температура по місяцях (2025)', fontweight='bold', pad=15)
    ax.set_xlabel('Місяць')
    ax.set_ylabel('Температура (°C)')
    ax.tick_params(axis='x', rotation=30)
    ax.grid(axis='y', linestyle='--', alpha=0.4)
    fig.tight_layout()

    return save_chart(fig, 'weather_monthly.png')


# ────────────────────────────────────────────────────────────────────────────
# Головна функція — визначає який графік будувати
# ────────────────────────────────────────────────────────────────────────────
def build_chart(df: pd.DataFrame, source_file: str):
    """
    Автоматично визначає тип CSV і будує відповідний графік.
    Викликається з main.py після завантаження файлу.
    """
    name = os.path.basename(source_file).lower()

    if 'sales' in name:
        return plot_sales(df)
    elif 'students' in name or 'student' in name:
        return plot_students(df)
    elif 'weather' in name:
        return plot_weather(df)
    else:
        print("⚠️  Невідомий тип файлу — графік не побудовано.")
        return None