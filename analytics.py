from datetime import datetime
from collections import defaultdict


class FinanceAnalytics:
    def __init__(self, finance_manager):
        self.manager = finance_manager

    def total_income(self):
        return sum(i["amount"] for i in self.manager.data["income"])

    def total_expenses(self):
        return sum(e["amount"] for e in self.manager.data["expenses"])

    def balance(self):
        return self.total_income() - self.total_expenses()

    def expenses_by_category(self):
        result = defaultdict(float)

        for e in self.manager.data["expenses"]:
            result[e["category"]] += float(e["amount"])

        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

    def income_by_category(self):
        result = defaultdict(float)

        for i in self.manager.data["income"]:
            result[i["category"]] += float(i["amount"])

        return dict(sorted(result.items(), key=lambda x: x[1], reverse=True))

    def expenses_by_month(self):
        """
        Повертає витрати по місяцях:
        {
            "2026-01": 3000,
            "2026-02": 2500
        }
        """
        result = defaultdict(float)

        for e in self.manager.data["expenses"]:
            date_obj = datetime.strptime(e["date"], "%Y-%m-%d")
            month_key = date_obj.strftime("%Y-%m")
            result[month_key] += float(e["amount"])

        return dict(sorted(result.items()))

    def income_by_month(self):
        """
        Повертає доходи по місяцях:
        {
            "2026-01": 8000,
            "2026-02": 7500
        }
        """
        result = defaultdict(float)

        for i in self.manager.data["income"]:
            date_obj = datetime.strptime(i["date"], "%Y-%m-%d")
            month_key = date_obj.strftime("%Y-%m")
            result[month_key] += float(i["amount"])

        return dict(sorted(result.items()))

    def top_expense_categories(self, limit=5):
        categories = self.expenses_by_category()
        return dict(list(categories.items())[:limit])

    def average_monthly_expenses(self):
        monthly = self.expenses_by_month()
        if len(monthly) == 0:
            return 0
        return round(sum(monthly.values()) / len(monthly), 2)

    def average_monthly_income(self):
        monthly = self.income_by_month()
        if len(monthly) == 0:
            return 0
        return round(sum(monthly.values()) / len(monthly), 2)

    def spending_trend(self):
        """
        Аналіз тренду витрат:
        - якщо останній місяць > середнього → "increasing"
        - якщо останній місяць < середнього → "decreasing"
        - інакше "stable"
        """
        monthly = self.expenses_by_month()

        if len(monthly) < 2:
            return "not_enough_data"

        values = list(monthly.values())
        avg = sum(values[:-1]) / (len(values) - 1)
        last = values[-1]

        if last > avg * 1.15:
            return "increasing"
        elif last < avg * 0.85:
            return "decreasing"
        else:
            return "stable"

    def generate_recommendations(self):
        """
        Формує список рекомендацій для користувача.
        """
        recommendations = []

        balance = self.balance()
        avg_expenses = self.average_monthly_expenses()
        trend = self.spending_trend()
        top_categories = self.top_expense_categories(3)

        if balance < 0:
            recommendations.append("Ваш баланс від’ємний. Варто зменшити витрати або збільшити дохід.")

        if avg_expenses > 0:
            recommendations.append(f"Середні витрати за місяць: {avg_expenses} грн.")

        if trend == "increasing":
            recommendations.append("Увага! Витрати зростають. Рекомендується переглянути бюджет.")
        elif trend == "decreasing":
            recommendations.append("Добре! Витрати зменшуються у порівнянні з попередніми місяцями.")
        elif trend == "stable":
            recommendations.append("Витрати стабільні. Ви добре контролюєте фінанси.")

        if len(top_categories) > 0:
            text = "Найбільші витрати у категоріях: "
            text += ", ".join([f"{cat} ({val:.2f} грн)" for cat, val in top_categories.items()])
            recommendations.append(text)

        if len(recommendations) == 0:
            recommendations.append("Недостатньо даних для аналізу. Додайте більше транзакцій.")

        return recommendations

    def get_full_report(self):
        """
        Повертає повний звіт як словник.
        """
        return {
            "total_income": round(self.total_income(), 2),
            "total_expenses": round(self.total_expenses(), 2),
            "balance": round(self.balance(), 2),
            "avg_monthly_income": self.average_monthly_income(),
            "avg_monthly_expenses": self.average_monthly_expenses(),
            "top_expense_categories": self.top_expense_categories(5),
            "trend": self.spending_trend(),
            "recommendations": self.generate_recommendations()
        }