from datetime import datetime
import numpy as np
from sklearn.linear_model import LinearRegression


class ExpenseForecaster:
    def __init__(self, finance_manager):
        self.manager = finance_manager

    def _group_expenses_by_month(self):
        """
        Групує витрати по місяцях.
        Повертає словник:
        {
            "2026-01": 1500,
            "2026-02": 2300
        }
        """
        expenses = self.manager.data["expenses"]
        monthly_data = {}

        for e in expenses:
            date_obj = datetime.strptime(e["date"], "%Y-%m-%d")
            key = date_obj.strftime("%Y-%m")
            monthly_data[key] = monthly_data.get(key, 0) + float(e["amount"])

        return dict(sorted(monthly_data.items()))

    def get_monthly_expense_series(self):
        """
        Повертає два списки:
        months = ["2026-01", "2026-02"]
        values = [1500, 2300]
        """
        monthly_data = self._group_expenses_by_month()

        months = list(monthly_data.keys())
        values = list(monthly_data.values())

        return months, values

    def forecast_next_month(self):
        """
        Прогноз загальних витрат на наступний місяць.
        Використовує лінійну регресію.
        """
        months, values = self.get_monthly_expense_series()

        if len(values) < 2:
            return {
                "status": "error",
                "message": "Недостатньо даних для прогнозу (потрібно хоча б 2 місяці витрат)."
            }

        X = np.array(range(len(values))).reshape(-1, 1)
        y = np.array(values)

        model = LinearRegression()
        model.fit(X, y)

        next_month_index = np.array([[len(values)]])
        prediction = model.predict(next_month_index)[0]

        prediction = max(prediction, 0)

        return {
            "status": "success",
            "forecast": round(float(prediction), 2),
            "months": months,
            "values": values
        }

    def forecast_by_category(self):
        """
        Прогноз витрат по категоріях.
        Повертає словник:
        {
            "Їжа": 3500,
            "Транспорт": 1200
        }
        """
        expenses = self.manager.data["expenses"]

        category_data = {}

        for e in expenses:
            category = e["category"]
            category_data.setdefault(category, [])
            category_data[category].append(float(e["amount"]))

        forecast_result = {}

        for category, amounts in category_data.items():
            if len(amounts) < 2:
                forecast_result[category] = round(sum(amounts), 2)
                continue

            X = np.array(range(len(amounts))).reshape(-1, 1)
            y = np.array(amounts)

            model = LinearRegression()
            model.fit(X, y)

            next_index = np.array([[len(amounts)]])
            prediction = model.predict(next_index)[0]
            prediction = max(prediction, 0)

            forecast_result[category] = round(float(prediction), 2)

        return dict(sorted(forecast_result.items(), key=lambda x: x[1], reverse=True))

    def get_forecast_summary(self):
        """
        Формує текстову рекомендацію на основі прогнозу.
        """
        forecast = self.forecast_next_month()

        if forecast["status"] == "error":
            return forecast["message"]

        value = forecast["forecast"]

        if value < 2000:
            return f"Прогноз витрат на наступний місяць: {value} грн. Витрати виглядають стабільними."
        elif value < 7000:
            return f"Прогноз витрат на наступний місяць: {value} грн. Рекомендується контролювати бюджет."
        else:
            return f"Прогноз витрат на наступний місяць: {value} грн. Високий рівень витрат! Варто оптимізувати витрати."