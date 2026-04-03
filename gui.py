# gui.py
import customtkinter as ctk
from finance import PersonalFinanceManager
from utils import validate_date, validate_amount
from charts import plot_income_expense

ctk.set_appearance_mode("Light")  # Мінімалістичний стиль
ctk.set_default_color_theme("blue")

class FinanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Особисті фінанси")
        self.geometry("800x600")
        self.manager = PersonalFinanceManager()

        # Ліва панель для форм
        self.left_frame = ctk.CTkFrame(self, width=300)
        self.left_frame.pack(side="left", fill="y", padx=10, pady=10)

        ctk.CTkLabel(self.left_frame, text="Доходи", font=("Arial", 16, "bold")).pack(pady=(0,5))
        self.income_amount = ctk.CTkEntry(self.left_frame, placeholder_text="Сума")
        self.income_amount.pack(pady=5)
        self.income_category = ctk.CTkEntry(self.left_frame, placeholder_text="Категорія")
        self.income_category.pack(pady=5)
        self.income_date = ctk.CTkEntry(self.left_frame, placeholder_text="Дата (YYYY-MM-DD)")
        self.income_date.pack(pady=5)
        ctk.CTkButton(self.left_frame, text="Додати дохід", command=self.add_income).pack(pady=5)

        ctk.CTkLabel(self.left_frame, text="Витрати", font=("Arial", 16, "bold")).pack(pady=(20,5))
        self.expense_amount = ctk.CTkEntry(self.left_frame, placeholder_text="Сума")
        self.expense_amount.pack(pady=5)
        self.expense_category = ctk.CTkEntry(self.left_frame, placeholder_text="Категорія")
        self.expense_category.pack(pady=5)
        self.expense_date = ctk.CTkEntry(self.left_frame, placeholder_text="Дата (YYYY-MM-DD)")
        self.expense_date.pack(pady=5)
        ctk.CTkButton(self.left_frame, text="Додати витрату", command=self.add_expense).pack(pady=5)

        # Права панель для графіків та балансу
        self.right_frame = ctk.CTkFrame(self)
        self.right_frame.pack(side="right", fill="both", expand=True, padx=10, pady=10)

        ctk.CTkButton(self.left_frame, text="Показати баланс", command=self.show_balance).pack(pady=(20,5))
        ctk.CTkButton(self.left_frame, text="Показати графік", command=self.show_charts).pack(pady=5)

        self.output = ctk.CTkTextbox(self.right_frame, width=400, height=200)
        self.output.pack(pady=10, padx=10)

    def add_income(self):
        try:
            amount = validate_amount(self.income_amount.get())
            category = self.income_category.get()
            date = validate_date(self.income_date.get())
            self.manager.add_income(amount, category, date)
            self.output.insert("end", f"Дохід додано: {amount} | {category} | {date}\n")
        except Exception as e:
            self.output.insert("end", f"Помилка: {e}\n")

    def add_expense(self):
        try:
            amount = validate_amount(self.expense_amount.get())
            category = self.expense_category.get()
            date = validate_date(self.expense_date.get())
            self.manager.add_expense(amount, category, date)
            self.output.insert("end", f"Витрата додана: {amount} | {category} | {date}\n")
        except Exception as e:
            self.output.insert("end", f"Помилка: {e}\n")

    def show_balance(self):
        balance = self.manager.get_balance()
        self.output.insert("end", f"Баланс: {balance}\n")

    def show_charts(self):
        # Очищаємо старі графіки
        for widget in self.right_frame.winfo_children():
            if isinstance(widget, ctk.CTkCanvas):
                widget.destroy()
        plot_income_expense(self.manager.data, self.right_frame)

if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()