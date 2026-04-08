from datetime import datetime

def validate_date(date_str):
   
    try:
        datetime_obj = datetime.strptime(date_str, "%Y-%m-%d")
        return datetime_obj.strftime("%Y-%m-%d")
    except ValueError:
        raise ValueError("Невірний формат дати. Використовуйте YYYY-MM-DD.")

def format_currency(amount):
 
    return f"{amount:,.2f} ₴"

def validate_amount(amount):
   
    try:
        value = float(amount)
        if value <= 0:
            raise ValueError("Сума повинна бути більшою за 0.")
        return value
    except ValueError:
        raise ValueError("Сума повинна бути числом.")

def prompt_input(prompt_text, validate_func=None):
   
    while True:
        value = input(prompt_text)
        if validate_func:
            try:
                return validate_func(value)
            except ValueError as e:
                print(e)
        else:
            return value