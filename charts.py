# charts.py
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

def plot_income_expense(data, parent_frame):
    # Збираємо дані
    income_dates = [item["date"] for item in data.get("income", [])]
    income_values = [item["amount"] for item in data.get("income", [])]

    expense_dates = [item["date"] for item in data.get("expenses", [])]
    expense_values = [item["amount"] for item in data.get("expenses", [])]

    # Малюємо графік
    fig, ax = plt.subplots(figsize=(6,4))
    ax.plot(income_dates, income_values, label="Доходи", marker='o', color='#4CAF50')
    ax.plot(expense_dates, expense_values, label="Витрати", marker='o', color='#F44336')
    ax.set_title("Доходи та витрати")
    ax.set_xlabel("Дата")
    ax.set_ylabel("Сума")
    ax.legend()
    ax.grid(True)

    # Вставка графіка в tkinter
    canvas = FigureCanvasTkAgg(fig, master=parent_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)