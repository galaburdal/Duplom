from datetime import datetime, timedelta
from collections import defaultdict

def monthly_forecast(data, months=1):
    """
    Прогноз витрат на основі середніх щомісячних витрат.
    
    data: словник з даними фінансів, наприклад:
        {
            "income": [...],
            "expenses": [
                {"amount": 1000, "category": "Їжа", "date": "2026-03-01"},
                ...
            ]
        }
    months: кількість місяців для прогнозу
    """
    
    if "expenses" not in data or not data["expenses"]:
        return "Немає даних для прогнозу."

    # Сума витрат по категоріях
    category_sums = defaultdict(float)
    month_counts = defaultdict(set)  # для підрахунку кількості місяців на категорію
    
    for expense in data["expenses"]:
        amount = float(expense["amount"])
        category = expense.get("category", "Інше")
        date_obj = datetime.strptime(expense["date"], "%Y-%m-%d")
        
        category_sums[category] += amount
        month_counts[category].add((date_obj.year, date_obj.month))
    
    # Середні витрати на місяць
    category_avg = {}
    for cat, total in category_sums.items():
        months_count = len(month_counts[cat])
        category_avg[cat] = total / months_count if months_count else 0

    # Прогноз на задану кількість місяців
    forecast = {}
    for cat, avg in category_avg.items():
        forecast[cat] = avg * months

    return forecast

# ---------------- ДРУК ПРОГНОЗУ ---------------- #
def print_forecast(forecast):
    if isinstance(forecast, str):
        print(forecast)
    else:
        print("--- Прогноз витрат ---")
        for cat, amount in forecast.items():
            print(f"{cat}: {amount:,.2f} ₴")