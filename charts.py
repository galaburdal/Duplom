import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


class ChartBuilder:
    def __init__(self):
        plt.style.use("default")

    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def draw_expenses_pie(self, expenses_by_category, frame):
        self.clear_frame(frame)

        if not expenses_by_category:
            label = tk.Label(frame, text="Немає даних для графіка витрат", fg="gray")
            label.pack(pady=20)
            return

        categories = list(expenses_by_category.keys())
        values = list(expenses_by_category.values())

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.pie(values, labels=categories, autopct="%1.1f%%", startangle=90)
        ax.set_title("Витрати по категоріях")

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def draw_income_pie(self, income_by_category, frame):
        self.clear_frame(frame)

        if not income_by_category:
            label = tk.Label(frame, text="Немає даних для графіка доходів", fg="gray")
            label.pack(pady=20)
            return

        categories = list(income_by_category.keys())
        values = list(income_by_category.values())

        fig, ax = plt.subplots(figsize=(6, 4), dpi=100)
        ax.pie(values, labels=categories, autopct="%1.1f%%", startangle=90)
        ax.set_title("Доходи по категоріях")

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def draw_expenses_line(self, expenses_by_month, frame):
        self.clear_frame(frame)

        if not expenses_by_month:
            label = tk.Label(frame, text="Немає даних для графіка витрат по місяцях", fg="gray")
            label.pack(pady=20)
            return

        months = list(expenses_by_month.keys())
        values = list(expenses_by_month.values())

        fig, ax = plt.subplots(figsize=(7, 4), dpi=100)
        ax.plot(months, values, marker="o")
        ax.set_title("Динаміка витрат по місяцях")
        ax.set_xlabel("Місяць")
        ax.set_ylabel("Сума витрат")
        ax.grid(True)

        ax.tick_params(axis='x', rotation=45)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

    def draw_top_expenses_bar(self, top_categories, frame):
        self.clear_frame(frame)

        if not top_categories:
            label = tk.Label(frame, text="Немає даних для топ витрат", fg="gray")
            label.pack(pady=20)
            return

        categories = list(top_categories.keys())
        values = list(top_categories.values())

        fig, ax = plt.subplots(figsize=(7, 4), dpi=100)
        ax.bar(categories, values)
        ax.set_title("ТОП категорій витрат")
        ax.set_xlabel("Категорії")
        ax.set_ylabel("Сума витрат")
        ax.grid(axis="y")

        ax.tick_params(axis='x', rotation=30)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)