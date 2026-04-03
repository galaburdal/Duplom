from datetime import datetime

# ---------------- ПЕРЕВІРКА ДАТ ---------------- #
def validate_date(date_str):
    """
    Перевіряє чи рядок є датою у форматі YYYY-MM-DD.
    Якщо ні — викликає ValueError.
    """
    try:
        datetime_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return datetime_obj.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("Невірний формат дати. Використовуйте YYYY-MM-DD.")

# ---------------- ФОРМАТУВАННЯ СУМ ---------------- #
def format_currency(amount):
    """
    Форматує суму у вигляді рядка з гривнями.
    """
    return f"{amount:,.2f} ₴"

# ---------------- ПЕРЕВІРКА ЧИСЕЛ ---------------- #
def validate_amount(amount):
    """
    Перевіряє, що введене число є додатнім числом.
    """
    try:
        value = float(amount)
        if value <= 0:
            raise ValueError("Сума повинна бути більшою за 0.")
        return value
    except ValueError:
        raise ValueError("Сума повинна бути числом.")

# ---------------- ІНШІ КОРИСНІ ФУНКЦІЇ ---------------- #
def prompt_input(prompt_text, validate_func=None):
    """
    Загальна функція для введення з перевіркою.
    validate_func - функція перевірки, наприклад validate_amount або validate_date
    """
    while True:
        value = input(prompt_text)
        if validate_func:
            try:
                return validate_func(value)
            except ValueError as e:
                print(e)
        else:
            return value