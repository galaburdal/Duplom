import json
from utils import validate_date

class PersonalFinanceManager:
    def __init__(self, filename="data.json"):
        self.filename = filename
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                self.data = json.load(f)
        except FileNotFoundError:
            self.data = {"income": [], "expenses": []}
            self.save_data()

    def save_data(self):
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(self.data, f, indent=4, ensure_ascii=False)

    def add_income(self):
        amount = float(input("Введіть суму доходу: "))
        category = input("Введіть категорію доходу (наприклад, Зарплата, Подарунки): ")
        date = validate_date(input("Введіть дату доходу (рррр-мм-дд): "))
        self.data["income"].append({"amount": amount, "category": category, "date": date})
        self.save_data()
        print("Дохід додано ✅")

    def add_expense(self):
        amount = float(input("Введіть суму витрати: "))
        category = input("Введіть категорію витрати (наприклад, Продукти, Транспорт): ")
        date = validate_date(input("Введіть дату витрати (рррр-мм-дд): "))
        self.data["expenses"].append({"amount": amount, "category": category, "date": date})
        self.save_data()
        print("Витрату додано ✅")

    def get_balance(self):
        total_income = sum(item["amount"] for item in self.data["income"])
        total_expense = sum(item["amount"] for item in self.data["expenses"])
        return total_income - total_expense

    def view_finances(self):
        print("\nДоходи:")
        for i, inc in enumerate(self.data["income"], 1):
            print(f"{i}. {inc['date']} | {inc['category']} | {inc['amount']:,.2f} ₴")
        print("\nВитрати:")
        for i, exp in enumerate(self.data["expenses"], 1):
            print(f"{i}. {exp['date']} | {exp['category']} | {exp['amount']:,.2f} ₴")