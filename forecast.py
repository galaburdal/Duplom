import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


class ExpenseForecaster:
    def __init__(self, manager):
        self.manager = manager

    def _prepare_daily_expenses(self):
        """Збирає витрати по днях у DataFrame."""
        expenses = self.manager.data.get("expenses", [])

        if not expenses:
            return None

        df = pd.DataFrame(expenses)
        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = df["amount"].astype(float)

        daily = df.groupby("date")["amount"].sum().reset_index()
        daily = daily.sort_values("date")

        return daily

    def _create_features(self, daily_df):
        """Створює набір ознак для ML моделі."""
        df = daily_df.copy()
        df["day"] = df["date"].dt.day
        df["month"] = df["date"].dt.month
        df["weekday"] = df["date"].dt.weekday
        df["trend"] = np.arange(len(df))

        # rolling mean (середнє значення за останні N днів)
        df["rolling_7"] = df["amount"].rolling(7).mean()
        df["rolling_30"] = df["amount"].rolling(30).mean()

        df["rolling_7"] = df["rolling_7"].fillna(df["amount"].mean())
        df["rolling_30"] = df["rolling_30"].fillna(df["amount"].mean())

        return df

    def forecast_next_30_days(self):
        """Прогнозує витрати на наступні 30 днів."""
        daily = self._prepare_daily_expenses()

        if daily is None or len(daily) < 15:
            return {
                "status": "error",
                "message": "Недостатньо даних для прогнозування. Додайте більше витрат (мінімум 15 днів)."
            }

        df = self._create_features(daily)

        X = df[["day", "month", "weekday", "trend", "rolling_7", "rolling_30"]]
        y = df["amount"]

        model = LinearRegression()
        model.fit(X, y)

        # Оцінка точності (на тренувальних даних)
        predictions = model.predict(X)

        mae = mean_absolute_error(y, predictions)
        mse = mean_squared_error(y, predictions)
        r2 = r2_score(y, predictions)

        # Створюємо майбутні дні
        last_date = df["date"].max()
        future_dates = [last_date + timedelta(days=i) for i in range(1, 31)]

        future_df = pd.DataFrame({"date": future_dates})
        future_df["day"] = future_df["date"].dt.day
        future_df["month"] = future_df["date"].dt.month
        future_df["weekday"] = future_df["date"].dt.weekday
        future_df["trend"] = np.arange(len(df), len(df) + 30)

        # rolling беремо як останні значення
        last_7_mean = df["amount"].tail(7).mean()
        last_30_mean = df["amount"].tail(30).mean()

        future_df["rolling_7"] = last_7_mean
        future_df["rolling_30"] = last_30_mean

        future_X = future_df[["day", "month", "weekday", "trend", "rolling_7", "rolling_30"]]
        future_pred = model.predict(future_X)

        future_df["forecast"] = np.maximum(future_pred, 0).round(2)

        total_forecast = float(future_df["forecast"].sum().round(2))

        trend_direction = "зростають" if df["amount"].tail(7).mean() > df["amount"].head(7).mean() else "зменшуються"

        return {
            "status": "ok",
            "model": "Linear Regression + Time Features",
            "mae": round(float(mae), 2),
            "mse": round(float(mse), 2),
            "r2": round(float(r2), 2),
            "trend": trend_direction,
            "daily_history": daily,
            "future_forecast": future_df,
            "total_forecast": total_forecast
        }

    def forecast_by_category(self):
        """Прогноз по категоріях: беремо середнє за останні 30 днів."""
        expenses = self.manager.data.get("expenses", [])

        if not expenses:
            return {}

        df = pd.DataFrame(expenses)
        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = df["amount"].astype(float)

        last_date = df["date"].max()
        df_recent = df[df["date"] >= (last_date - timedelta(days=30))]

        result = df_recent.groupby("category")["amount"].mean().round(2).to_dict()

        # Перетворюємо в прогноз на 30 днів
        forecast = {cat: round(val * 30, 2) for cat, val in result.items()}

        return forecast

    def generate_ai_recommendations(self):
        """Генерує рекомендації на основі витрат."""
        expenses = self.manager.data.get("expenses", [])

        if not expenses:
            return ["Немає даних для рекомендацій. Додайте витрати."]

        df = pd.DataFrame(expenses)
        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = df["amount"].astype(float)

        last_date = df["date"].max()
        df_30 = df[df["date"] >= (last_date - timedelta(days=30))]
        df_60 = df[df["date"] >= (last_date - timedelta(days=60))]

        total_30 = df_30["amount"].sum()
        total_60 = df_60["amount"].sum()

        recs = []

        if total_60 > 0:
            growth = ((total_30 / (total_60 - total_30 + 1e-9)) - 1) * 100
            if growth > 10:
                recs.append(f"Ваші витрати за останні 30 днів зросли приблизно на {growth:.1f}%.")
            else:
                recs.append("Ваші витрати залишаються стабільними.")

        top_category = df_30.groupby("category")["amount"].sum().idxmax()
        top_value = df_30.groupby("category")["amount"].sum().max()

        recs.append(f"Найбільша категорія витрат: {top_category} ({round(top_value, 2)} грн за 30 днів).")
        recs.append("Рекомендується встановити ліміт на найбільшу категорію витрат.")

        return recs