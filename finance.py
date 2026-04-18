import json
import os
import csv
from datetime import datetime


class PersonalFinanceManager:
    def __init__(self, data_file="data/data.json"):
        self.data_file = data_file
        self.data = self.load_data()

    def load_data(self):
        folder = os.path.dirname(self.data_file)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        if not os.path.exists(self.data_file):
            default_data = {
                "active_profile": "Основний",
                "profiles": {
                    "Основний": {
                        "income": [],
                        "expenses": []
                    }
                }
            }
            self.save_data(default_data)
            return default_data

        try:
            with open(self.data_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except json.JSONDecodeError:
            data = {
                "active_profile": "Основний",
                "profiles": {
                    "Основний": {
                        "income": [],
                        "expenses": []
                    }
                }
            }
            self.save_data(data)
            return data

        if "profiles" not in data:
            migrated_data = {
                "active_profile": "Основний",
                "profiles": {
                    "Основний": {
                        "income": data.get("income", []),
                        "expenses": data.get("expenses", [])
                    }
                }
            }
            self.save_data(migrated_data)
            return migrated_data

        if "active_profile" not in data:
            data["active_profile"] = "Основний"

        if "profiles" not in data:
            data["profiles"] = {}

        if not data["profiles"]:
            data["profiles"]["Основний"] = {"income": [], "expenses": []}
            data["active_profile"] = "Основний"

        if data["active_profile"] not in data["profiles"]:
            data["active_profile"] = list(data["profiles"].keys())[0]

        for profile_name in data["profiles"]:
            if "income" not in data["profiles"][profile_name]:
                data["profiles"][profile_name]["income"] = []
            if "expenses" not in data["profiles"][profile_name]:
                data["profiles"][profile_name]["expenses"] = []

        self.save_data(data)
        return data

    def save_data(self, data=None):
        if data is None:
            data = self.data

        folder = os.path.dirname(self.data_file)
        if folder and not os.path.exists(folder):
            os.makedirs(folder)

        with open(self.data_file, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)


    def get_profile_names(self):
        return list(self.data["profiles"].keys())

    def get_active_profile(self):
        return self.data["active_profile"]

    def set_active_profile(self, profile_name):
        if profile_name in self.data["profiles"]:
            self.data["active_profile"] = profile_name
            self.save_data()
            return True
        return False

    def create_profile(self, profile_name):
        profile_name = profile_name.strip()

        if not profile_name:
            return False, "Назва профілю не може бути порожньою."

        if profile_name in self.data["profiles"]:
            return False, "Профіль з такою назвою вже існує."

        self.data["profiles"][profile_name] = {
            "income": [],
            "expenses": []
        }
        self.save_data()
        return True, "Профіль створено."

    def rename_profile(self, old_name, new_name):
        new_name = new_name.strip()

        if old_name not in self.data["profiles"]:
            return False, "Профіль не знайдено."

        if not new_name:
            return False, "Нова назва профілю не може бути порожньою."

        if new_name == old_name:
            return False, "Нова назва збігається з поточною."

        if new_name in self.data["profiles"]:
            return False, "Профіль з такою назвою вже існує."

        self.data["profiles"][new_name] = self.data["profiles"].pop(old_name)

        if self.data["active_profile"] == old_name:
            self.data["active_profile"] = new_name

        self.save_data()
        return True, "Профіль перейменовано."

    def delete_profile(self, profile_name):
        if profile_name not in self.data["profiles"]:
            return False, "Профіль не знайдено."

        if len(self.data["profiles"]) == 1:
            return False, "Не можна видалити єдиний профіль."

        del self.data["profiles"][profile_name]

        if self.data["active_profile"] == profile_name:
            self.data["active_profile"] = list(self.data["profiles"].keys())[0]

        self.save_data()
        return True, "Профіль видалено."

    def get_profile_summary(self, profile_name=None):
        if profile_name is None:
            profile_name = self.get_active_profile()

        if profile_name not in self.data["profiles"]:
            return None

        profile = self.data["profiles"][profile_name]

        income_count = len(profile["income"])
        expense_count = len(profile["expenses"])
        total_income = sum(item["amount"] for item in profile["income"])
        total_expenses = sum(item["amount"] for item in profile["expenses"])
        balance = total_income - total_expenses

        return {
            "name": profile_name,
            "income_count": income_count,
            "expense_count": expense_count,
            "total_income": round(total_income, 2),
            "total_expenses": round(total_expenses, 2),
            "balance": round(balance, 2)
        }


    def _current_profile_data(self):
        active = self.data["active_profile"]
        return self.data["profiles"][active]


    def add_income(self, amount, category, date):
        transaction = {
            "amount": float(amount),
            "category": category.strip().capitalize(),
            "date": date
        }

        self._current_profile_data()["income"].append(transaction)
        self.save_data()

    def add_expense(self, amount, category, date):
        transaction = {
            "amount": float(amount),
            "category": category.strip().capitalize(),
            "date": date
        }

        self._current_profile_data()["expenses"].append(transaction)
        self.save_data()

    def get_transactions(self):
        profile = self._current_profile_data()
        transactions = []

        for item in profile["income"]:
            transactions.append({
                "type": "income",
                "amount": item["amount"],
                "category": item["category"],
                "date": item["date"]
            })

        for item in profile["expenses"]:
            transactions.append({
                "type": "expense",
                "amount": item["amount"],
                "category": item["category"],
                "date": item["date"]
            })

        transactions.sort(key=lambda x: x["date"])
        return transactions

    def get_transactions_with_index(self):
        profile = self._current_profile_data()
        transactions = []

        for i, inc in enumerate(profile["income"]):
            transactions.append({
                "type": "income",
                "index": i,
                "amount": inc["amount"],
                "category": inc["category"],
                "date": inc["date"]
            })

        for i, exp in enumerate(profile["expenses"]):
            transactions.append({
                "type": "expense",
                "index": i,
                "amount": exp["amount"],
                "category": exp["category"],
                "date": exp["date"]
            })

        transactions.sort(key=lambda x: x["date"])
        return transactions

    def delete_transaction(self, transaction_type, index):
        profile = self._current_profile_data()

        if transaction_type == "income":
            if 0 <= index < len(profile["income"]):
                profile["income"].pop(index)
                self.save_data()
                return True

        elif transaction_type == "expense":
            if 0 <= index < len(profile["expenses"]):
                profile["expenses"].pop(index)
                self.save_data()
                return True

        return False

    def update_transaction(self, transaction_type, index, new_amount, new_category, new_date):
        profile = self._current_profile_data()

        updated_transaction = {
            "amount": float(new_amount),
            "category": new_category.strip().capitalize(),
            "date": new_date
        }

        if transaction_type == "income":
            if 0 <= index < len(profile["income"]):
                profile["income"][index] = updated_transaction
                self.save_data()
                return True

        elif transaction_type == "expense":
            if 0 <= index < len(profile["expenses"]):
                profile["expenses"][index] = updated_transaction
                self.save_data()
                return True

        return False


    def get_balance(self):
        profile = self._current_profile_data()

        total_income = sum(item["amount"] for item in profile["income"])
        total_expenses = sum(item["amount"] for item in profile["expenses"])
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
            writer.writerow(["Профіль", "Тип", "Сума", "Категорія", "Дата"])

            current_profile = self.get_active_profile()

            for t in transactions:
                t_type = "Дохід" if t["type"] == "income" else "Витрата"
                writer.writerow([current_profile, t_type, t["amount"], t["category"], t["date"]])