import pandas as pd
import numpy as np
from datetime import timedelta

from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score


class ExpenseForecaster:
    def __init__(self, manager):
        self.manager = manager

    def _profile_data(self):
        return self.manager._current_profile_data()

    def get_expense_dataframe(self, window_days=None):
        profile = self._profile_data()
        expenses = profile.get("expenses", [])

        if not expenses:
            return None

        df = pd.DataFrame(expenses)
        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = df["amount"].astype(float)

        daily = df.groupby("date")["amount"].sum().reset_index()
        daily = daily.sort_values("date")

        if window_days is not None and len(daily) > 0:
            last_date = daily["date"].max()
            start_date = last_date - timedelta(days=window_days - 1)
            daily = daily[daily["date"] >= start_date].copy()

        return daily.reset_index(drop=True)

    def _safe_metrics(self, y_true, y_pred):
        mae = mean_absolute_error(y_true, y_pred)
        mse = mean_squared_error(y_true, y_pred)

        try:
            r2 = r2_score(y_true, y_pred)
        except:
            r2 = 0.0

        return round(float(mae), 2), round(float(mse), 2), round(float(r2), 2)

    def _build_future_dates(self, last_date, future_days):
        return [last_date + timedelta(days=i) for i in range(1, future_days + 1)]

    def _stable_level(self, y):
        y = np.array(y, dtype=float)

        mean_val = np.mean(y)
        median_val = np.median(y)

        weights = np.arange(1, len(y) + 1)
        weighted_val = np.sum(y * weights) / np.sum(weights)

        stable = 0.35 * mean_val + 0.25 * median_val + 0.40 * weighted_val
        return float(stable)

    def _volatility_buffer(self, y):

        y = np.array(y, dtype=float)

        if len(y) < 2:
            return 0.0

        std_val = np.std(y)
        return float(std_val * 0.15)

    def forecast_with_model(self, window_days=30, model="linear", future_days=30):
        daily = self.get_expense_dataframe(window_days=window_days)

        if daily is None or len(daily) < 5:
            return {
                "status": "error",
                "message": f"Недостатньо даних для прогнозування за вікном {window_days} днів."
            }

        y = daily["amount"].to_numpy(dtype=float)
        last_date = daily["date"].max()


        if model == "linear":
            df = daily.copy()
            df["day_index"] = np.arange(len(df))

            X = df[["day_index"]]
            y_series = df["amount"]

            reg = LinearRegression()
            reg.fit(X, y_series)

            train_pred = reg.predict(X)

            future_index = np.arange(len(df), len(df) + future_days).reshape(-1, 1)
            raw_future_pred = reg.predict(future_index)

            stable_base = self._stable_level(y)
            volatility = self._volatility_buffer(y)

            # Комбінуємо регресію з базовим рівнем
            blended_pred = 0.45 * raw_future_pred + 0.55 * stable_base

            # Межі, щоб прогноз не провалювався до нуля і не був нереалістичним
            lower_bound = max(np.median(y) * 0.55, np.min(y) * 0.35, 50)
            upper_bound = max(np.max(y) * 1.20, stable_base * 1.8)

            final_pred = np.clip(blended_pred + volatility, lower_bound, upper_bound)

            future_dates = self._build_future_dates(last_date, future_days)
            future_df = pd.DataFrame({
                "date": future_dates,
                "forecast": np.round(final_pred, 2)
            })

            mae, mse, r2 = self._safe_metrics(y_series, train_pred)

            recent_avg = np.mean(y[-min(5, len(y)):])
            early_avg = np.mean(y[:min(5, len(y))])

            if recent_avg > early_avg * 1.08:
                trend_direction = "зростають"
            elif recent_avg < early_avg * 0.92:
                trend_direction = "зменшуються"
            else:
                trend_direction = "стабільні"

            return {
                "status": "ok",
                "model": "Лінійна регресія (стабілізована)",
                "model_key": "linear",
                "window": window_days,
                "mae": mae,
                "mse": mse,
                "r2": r2,
                "trend": trend_direction,
                "daily_history": daily,
                "future_forecast": future_df,
                "total_forecast": round(float(future_df["forecast"].sum()), 2)
            }


        elif model == "average":
            avg = float(np.mean(y))
            predictions = np.array([avg for _ in range(future_days)])

            future_dates = self._build_future_dates(last_date, future_days)
            future_df = pd.DataFrame({
                "date": future_dates,
                "forecast": np.round(predictions, 2)
            })

            mae, mse, r2 = self._safe_metrics(y, np.array([avg] * len(y)))

            return {
                "status": "ok",
                "model": "Середнє значення",
                "model_key": "average",
                "window": window_days,
                "mae": mae,
                "mse": mse,
                "r2": r2,
                "trend": "стабільні",
                "daily_history": daily,
                "future_forecast": future_df,
                "total_forecast": round(float(future_df["forecast"].sum()), 2)
            }


        elif model == "weighted":
            weights = np.arange(1, len(y) + 1)
            weighted_avg = float(np.sum(y * weights) / np.sum(weights))
            volatility = self._volatility_buffer(y)

            predictions = np.array([weighted_avg + volatility for _ in range(future_days)])

            future_dates = self._build_future_dates(last_date, future_days)
            future_df = pd.DataFrame({
                "date": future_dates,
                "forecast": np.round(predictions, 2)
            })

            mae, mse, r2 = self._safe_metrics(y, np.array([weighted_avg] * len(y)))

            recent_avg = np.mean(y[-min(5, len(y)):])
            early_avg = np.mean(y[:min(5, len(y))])

            if recent_avg > early_avg * 1.08:
                trend_direction = "зростають"
            elif recent_avg < early_avg * 0.92:
                trend_direction = "зменшуються"
            else:
                trend_direction = "стабільні"

            return {
                "status": "ok",
                "model": "Зважене середнє",
                "model_key": "weighted",
                "window": window_days,
                "mae": mae,
                "mse": mse,
                "r2": r2,
                "trend": trend_direction,
                "daily_history": daily,
                "future_forecast": future_df,
                "total_forecast": round(float(future_df["forecast"].sum()), 2)
            }

        else:
            return {
                "status": "error",
                "message": "Невідома модель прогнозування."
            }

    def forecast_next_30_days(self):
        return self.forecast_with_model(window_days=30, model="linear", future_days=30)

    def forecast_by_category(self, window_days=30):
        profile = self._profile_data()
        expenses = profile.get("expenses", [])

        if not expenses:
            return {}

        df = pd.DataFrame(expenses)
        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = df["amount"].astype(float)

        last_date = df["date"].max()
        df_recent = df[df["date"] >= (last_date - timedelta(days=window_days - 1))]

        if df_recent.empty:
            return {}

        result = df_recent.groupby("category")["amount"].mean().round(2).to_dict()
        forecast = {cat: round(val * 30, 2) for cat, val in result.items()}

        return dict(sorted(forecast.items(), key=lambda x: x[1], reverse=True))

    def generate_ai_recommendations(self, window_days=30):
        profile = self._profile_data()
        expenses = profile.get("expenses", [])

        if not expenses:
            return ["Немає даних для рекомендацій. Додайте витрати."]

        df = pd.DataFrame(expenses)
        df["date"] = pd.to_datetime(df["date"])
        df["amount"] = df["amount"].astype(float)

        last_date = df["date"].max()
        df_window = df[df["date"] >= (last_date - timedelta(days=window_days - 1))]
        df_prev = df[
            (df["date"] < (last_date - timedelta(days=window_days - 1))) &
            (df["date"] >= (last_date - timedelta(days=(2 * window_days) - 1)))
        ]

        recs = []

        if not df_window.empty:
            total_window = df_window["amount"].sum()

            if not df_prev.empty:
                total_prev = max(df_prev["amount"].sum(), 1e-9)
                growth = ((total_window / total_prev) - 1) * 100

                if growth > 10:
                    recs.append(f"Ваші витрати за останнє вікно {window_days} днів зросли приблизно на {growth:.1f}%.")
                elif growth < -10:
                    recs.append(f"Ваші витрати за останнє вікно {window_days} днів зменшилися приблизно на {abs(growth):.1f}%.")
                else:
                    recs.append("Ваші витрати залишаються відносно стабільними.")
            else:
                recs.append("Недостатньо історичних даних для порівняння попереднього періоду.")

            top_by_cat = df_window.groupby("category")["amount"].sum()
            if not top_by_cat.empty:
                top_category = top_by_cat.idxmax()
                top_value = top_by_cat.max()
                recs.append(f"Найбільша категорія витрат: {top_category} ({round(top_value, 2)} грн за {window_days} днів).")
                recs.append("Рекомендується встановити ліміт на найбільшу категорію витрат.")
        else:
            recs.append("Недостатньо даних для повного аналізу рекомендацій.")

        return recs