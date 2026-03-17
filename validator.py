import pandas as pd


def validate_csv(df: pd.DataFrame, file_path: str = "") -> bool:
    """
    Перевіряє DataFrame на коректність даних.
    Повертає True якщо дані валідні, False якщо є критичні помилки.
    """
    print("\n🔍 Валідація даних...")
    has_critical_errors = False

    # ── 1. Перевірка на порожній файл ──────────────────────────────────────
    if df.empty:
        print("❌ КРИТИЧНА ПОМИЛКА: Файл порожній — немає жодного рядка даних.")
        return False

    print(f"✅ Кількість рядків: {len(df)}, колонок: {len(df.columns)}")

    # ── 2. Перевірка на порожні клітинки (NaN) ─────────────────────────────
    missing = df.isnull().sum()
    missing_cols = missing[missing > 0]

    if not missing_cols.empty:
        print("\n⚠️  Знайдено порожні клітинки:")
        for col, count in missing_cols.items():
            print(f"   • Колонка '{col}': {count} порожніх значень")
        has_critical_errors = True
    else:
        print("✅ Порожніх клітинок немає.")

    # ── 3. Перевірка числових колонок ──────────────────────────────────────
    numeric_issues = []
    for col in df.columns:
        # Якщо pandas вважає колонку текстовою — перевіримо чи не числова вона насправді
        if df[col].dtype == object:
            converted = pd.to_numeric(df[col], errors="coerce")
            valid_numeric = converted.notnull().sum()
            total = df[col].notnull().sum()
            # Перевіряємо лише якщо більше 50% значень схожі на числа
            if total > 0 and (valid_numeric / total) > 0.5:
                bad_count = converted.isnull().sum() - df[col].isnull().sum()
            else:
                bad_count = 0
            if bad_count > 0:
                # Знаходимо приклади поганих значень
                bad_values = df[col][converted.isnull() & df[col].notnull()].unique()[:3]
                numeric_issues.append((col, bad_count, bad_values))

    if numeric_issues:
        print("\n⚠️  Знайдено нечислові значення в можливо числових колонках:")
        for col, count, examples in numeric_issues:
            print(f"   • Колонка '{col}': {count} проблемних значень (приклади: {list(examples)})")
    else:
        print("✅ Типи даних виглядають коректно.")

    # ── 4. Перевірка на дублікати ───────────────────────────────────────────
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        print(f"\n⚠️  Знайдено {duplicate_count} дублікатів рядків.")
        has_critical_errors = True
    else:
        print("✅ Дублікатів рядків немає.")

    # ── Підсумок ────────────────────────────────────────────────────────────
    if has_critical_errors:
        print("\n⚠️  Валідація завершена З ПОПЕРЕДЖЕННЯМИ. Дані можуть бути неточними.")
    else:
        print("\n✅ Валідація пройдена успішно! Дані виглядають коректно.")

    return not has_critical_errors