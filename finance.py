import json
import os
import csv
from datetime import datetime


class PersonalFinanceManager:
    def __init__(self, data_file="data/data.json"):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        if not os.path.exists(self.data_file):
            default_data = {
                "income": [],
                "expenses": []
            }
            self.save_data(default_data)
            return default_data

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            if "income" not in data:
                data["income"] = []
            if "expenses" not in data:
                data["expenses"] = []

            return data

        except json.JSONDecodeError:
            default_data = {
                "income": [],
                "expenses": []
            }
            self.save_data(default_data)
            return default_data

    def save_data(self, data=None):
        if data is None:
            data = self.data

        folder = os.path.dirname(self.data_file)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    def add_income(self, amount, category, date):
        transaction = {
            "amount": float(amount),
            "category": category,
            "date": date
        }

        self.data["income"].append(transaction)
        self.save_data()

    def add_expense(self, amount, category, date):
        transaction = {
            "amount": float(amount),
            "category": category,
            "date": date
        }

        self.data["expenses"].append(transaction)
        self.save_data()

    def get_transactions(self):
        transactions = []

        for item in self.data["income"]:
            transactions.append({
                "type": "income",
                "amount": item["amount"],
                "category": item["category"],
                "date": item["date"]
            })

        for item in self.data["expenses"]:
            transactions.append({
                "type": "expense",
                "amount": item["amount"],
                "category": item["category"],
                "date": item["date"]
            })

        transactions.sort(key=lambda x: x["date"])
        return transactions

    def get_balance(self):
        total_income = sum(item["amount"] for item in self.data["income"])
        total_expenses = sum(item["amount"] for item in self.data["expenses"])
        balance = total_income - total_expenses

        return {
            "income": total_income,
            "expenses": total_expenses,
            "balance": balance
        }

    def filter_transactions(self, start_date=None, end_date=None, category=None, transaction_type=None):
        transactions = self.get_transactions()
        result = []

        for t in transactions:
            t_date = datetime.strptime(t["date"], "%Y-%m-%d")

            if start_date:
                start = datetime.strptime(start_date, "%Y-%m-%d")
                if t_date < start:
                    continue

            if end_date:
                end = datetime.strptime(end_date, "%Y-%m-%d")
                if t_date > end:
                    continue

            if category:
                if t["category"].lower() != category.lower():
                    continue

            if transaction_type:
                if t["type"] != transaction_type:
                    continue

            result.append(t)

        return result

    def export_to_csv(self, filename="exports/report.csv"):
        folder = os.path.dirname(filename)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        transactions = self.get_transactions()

        with open(filename, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["Тип", "Сума", "Категорія", "Дата"])

            for t in transactions:
                t_type = "Дохід" if t["type"] == "income" else "Витрата"
                writer.writerow([t_type, t["amount"], t["category"], t["date"]])