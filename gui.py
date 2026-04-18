import customtkinter as ctk
from tkinter import messagebox, simpledialog
from datetime import datetime

from finance import PersonalFinanceManager
from analytics import FinanceAnalytics
from forecast import ExpenseForecaster
from charts import ChartBuilder


ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")


BG_COLOR = "#1e1e1e"
SIDEBAR_COLOR = "#2a2a2a"
CARD_COLOR = "#2f2f2f"

BUTTON_COLOR = "#c8b6a6"
BUTTON_HOVER = "#bfa892"

TEXT_COLOR = "#f2f2f2"
ACCENT_COLOR = "#e0c9a6"


class FinanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Personal Finance Manager Pro")
        self.geometry("1400x900")
        self.minsize(1200, 780)

        self.manager = PersonalFinanceManager()
        self.analytics = FinanceAnalytics(self.manager)
        self.forecaster = ExpenseForecaster(self.manager)
        self.charts = ChartBuilder()

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)


        self.sidebar = ctk.CTkScrollableFrame(
            self,
            width=300,
            fg_color=SIDEBAR_COLOR,
            corner_radius=0
        )
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_columnconfigure(0, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="Finance Pro",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=ACCENT_COLOR
        )
        self.logo_label.grid(row=0, column=0, padx=24, pady=(24, 14), sticky="w")

        self.menu_label = ctk.CTkLabel(
            self.sidebar,
            text="Меню",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_COLOR
        )
        self.menu_label.grid(row=1, column=0, padx=24, pady=(0, 10), sticky="w")

        self.profile_label = ctk.CTkLabel(
            self.sidebar,
            text="Керування профілями",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_COLOR
        )
        self.profile_label.grid(row=2, column=0, padx=24, pady=(10, 5), sticky="w")

        self.profile_var = ctk.StringVar(value=self.manager.get_active_profile())

        self.profile_menu = ctk.CTkOptionMenu(
            self.sidebar,
            values=self.manager.get_profile_names(),
            variable=self.profile_var,
            command=self.change_profile,
            corner_radius=12
        )
        self.profile_menu.grid(row=3, column=0, padx=24, pady=(0, 10), sticky="we")

        self.new_profile_entry = ctk.CTkEntry(
            self.sidebar,
            placeholder_text="Новий профіль",
            corner_radius=12
        )
        self.new_profile_entry.grid(row=4, column=0, padx=24, pady=(0, 8), sticky="we")

        self.create_profile_btn = ctk.CTkButton(
            self.sidebar,
            text="➕ Створити профіль",
            command=self.create_profile,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER,
            text_color="#1a1a1a",
            corner_radius=15,
            height=42,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.create_profile_btn.grid(row=5, column=0, padx=24, pady=(0, 8), sticky="we")

        self.rename_profile_btn = ctk.CTkButton(
            self.sidebar,
            text="✏ Перейменувати профіль",
            command=self.rename_profile,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER,
            text_color="#1a1a1a",
            corner_radius=15,
            height=42,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.rename_profile_btn.grid(row=6, column=0, padx=24, pady=(0, 8), sticky="we")

        self.delete_profile_btn = ctk.CTkButton(
            self.sidebar,
            text="🗑 Видалити профіль",
            command=self.delete_profile,
            fg_color="#d9534f",
            hover_color="#c9302c",
            text_color="white",
            corner_radius=15,
            height=42,
            font=ctk.CTkFont(size=13, weight="bold")
        )
        self.delete_profile_btn.grid(row=7, column=0, padx=24, pady=(0, 12), sticky="we")

        self.profile_info_box = ctk.CTkTextbox(self.sidebar, height=125, corner_radius=12)
        self.profile_info_box.grid(row=8, column=0, padx=24, pady=(0, 18), sticky="we")


        self.btn_dashboard = self.create_sidebar_button("📊 Dashboard", self.show_dashboard)
        self.btn_dashboard.grid(row=9, column=0, padx=24, pady=8, sticky="we")

        self.btn_add_transaction = self.create_sidebar_button("➕ Додати транзакцію", self.show_add_transaction)
        self.btn_add_transaction.grid(row=10, column=0, padx=24, pady=8, sticky="we")

        self.btn_transactions = self.create_sidebar_button("📄 Транзакції", self.show_transactions)
        self.btn_transactions.grid(row=11, column=0, padx=24, pady=8, sticky="we")

        self.btn_analytics = self.create_sidebar_button("📈 Аналітика", self.show_analytics)
        self.btn_analytics.grid(row=12, column=0, padx=24, pady=8, sticky="we")

        self.btn_forecast = self.create_sidebar_button("🤖 Прогноз", self.show_forecast)
        self.btn_forecast.grid(row=13, column=0, padx=24, pady=8, sticky="we")

        self.btn_export = self.create_sidebar_button("💾 Експорт CSV", self.export_csv)
        self.btn_export.grid(row=14, column=0, padx=24, pady=8, sticky="we")

        self.footer_label = ctk.CTkLabel(
            self.sidebar,
            text="© 2026 Finance Pro",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.footer_label.grid(row=15, column=0, padx=24, pady=(18, 24))


        self.content_frame = ctk.CTkScrollableFrame(
            self,
            fg_color=BG_COLOR,
            corner_radius=0
        )
        self.content_frame.grid(row=0, column=1, sticky="nswe")
        self.content_frame.grid_columnconfigure(0, weight=1)

        self.refresh_profile_info()
        self.show_dashboard()

    def create_sidebar_button(self, text, command):
        return ctk.CTkButton(
            self.sidebar,
            text=text,
            command=command,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER,
            text_color="#1a1a1a",
            corner_radius=15,
            height=44,
            font=ctk.CTkFont(size=14, weight="bold")
        )

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    def create_card(self, parent, title, value, col):
        card = ctk.CTkFrame(parent, fg_color=CARD_COLOR, corner_radius=20, height=120)
        card.grid(row=0, column=col, padx=10, pady=10, sticky="we")

        lbl_title = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=16, weight="bold"))
        lbl_title.pack(pady=(20, 5))

        lbl_value = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(size=22, weight="bold"),
            text_color=ACCENT_COLOR
        )
        lbl_value.pack()

    def refresh_profile_menu(self):
        names = self.manager.get_profile_names()
        self.profile_menu.configure(values=names)
        self.profile_var.set(self.manager.get_active_profile())

    def refresh_profile_info(self):
        summary = self.manager.get_profile_summary()

        self.profile_info_box.configure(state="normal")
        self.profile_info_box.delete("1.0", "end")

        if summary:
            self.profile_info_box.insert(
                "end",
                f"Активний профіль:\n"
                f"{summary['name']}\n\n"
                f"Доходів: {summary['income_count']}\n"
                f"Витрат: {summary['expense_count']}\n"
                f"Баланс: {summary['balance']} грн"
            )

        self.profile_info_box.configure(state="disabled")


    def create_profile(self):
        profile_name = self.new_profile_entry.get().strip()
        success, message = self.manager.create_profile(profile_name)

        if success:
            messagebox.showinfo("Успіх", message)
            self.new_profile_entry.delete(0, "end")
            self.refresh_profile_menu()
            self.refresh_profile_info()
        else:
            messagebox.showerror("Помилка", message)

    def rename_profile(self):
        old_name = self.manager.get_active_profile()
        new_name = simpledialog.askstring(
            "Перейменування профілю",
            f"Введіть нову назву для профілю '{old_name}':",
            parent=self
        )

        if new_name is None:
            return

        success, message = self.manager.rename_profile(old_name, new_name)

        if success:
            messagebox.showinfo("Успіх", message)
            self.analytics = FinanceAnalytics(self.manager)
            self.forecaster = ExpenseForecaster(self.manager)
            self.refresh_profile_menu()
            self.refresh_profile_info()
            self.show_dashboard()
        else:
            messagebox.showerror("Помилка", message)

    def delete_profile(self):
        profile_name = self.manager.get_active_profile()

        confirm = messagebox.askyesno(
            "Підтвердження видалення",
            f"Ви дійсно хочете видалити профіль '{profile_name}'?"
        )

        if not confirm:
            return

        success, message = self.manager.delete_profile(profile_name)

        if success:
            messagebox.showinfo("Успіх", message)
            self.analytics = FinanceAnalytics(self.manager)
            self.forecaster = ExpenseForecaster(self.manager)
            self.refresh_profile_menu()
            self.refresh_profile_info()
            self.show_dashboard()
        else:
            messagebox.showerror("Помилка", message)

    def change_profile(self, profile_name):
        ok = self.manager.set_active_profile(profile_name)
        if ok:
            self.analytics = FinanceAnalytics(self.manager)
            self.forecaster = ExpenseForecaster(self.manager)
            self.profile_var.set(profile_name)
            self.refresh_profile_info()
            self.show_dashboard()
        else:
            messagebox.showerror("Помилка", "Не вдалося перемкнути профіль.")


    def show_dashboard(self):
        self.clear_content()

        title = ctk.CTkLabel(
            self.content_frame,
            text=f"Dashboard — {self.manager.get_active_profile()}",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=ACCENT_COLOR
        )
        title.pack(pady=(26, 18), padx=30, anchor="w")

        report = self.analytics.get_full_report()

        cards_frame = ctk.CTkFrame(self.content_frame, fg_color=BG_COLOR)
        cards_frame.pack(fill="x", padx=30)
        cards_frame.grid_columnconfigure((0, 1, 2), weight=1)

        self.create_card(cards_frame, "Доходи", f"{report['total_income']} грн", 0)
        self.create_card(cards_frame, "Витрати", f"{report['total_expenses']} грн", 1)
        self.create_card(cards_frame, "Баланс", f"{report['balance']} грн", 2)

        rec_title = ctk.CTkLabel(
            self.content_frame,
            text="Рекомендації системи:",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=TEXT_COLOR
        )
        rec_title.pack(pady=(25, 10), padx=30, anchor="w")

        rec_box = ctk.CTkTextbox(self.content_frame, height=220, corner_radius=15)
        rec_box.pack(fill="x", padx=30, pady=(0, 20))
        rec_box.configure(state="normal")

        for r in report["recommendations"]:
            rec_box.insert("end", f"• {r}\n")

        rec_box.configure(state="disabled")

    def show_add_transaction(self):
        self.clear_content()

        title = ctk.CTkLabel(
            self.content_frame,
            text=f"Додати транзакцію — {self.manager.get_active_profile()}",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=ACCENT_COLOR
        )
        title.pack(pady=(26, 18), padx=30, anchor="w")

        form = ctk.CTkFrame(self.content_frame, fg_color=CARD_COLOR, corner_radius=20)
        form.pack(padx=30, pady=10, fill="x")
        form.grid_columnconfigure((0, 1), weight=1)

        type_label = ctk.CTkLabel(form, text="Тип:", font=ctk.CTkFont(size=14, weight="bold"))
        type_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.type_option = ctk.CTkOptionMenu(
            form,
            values=["Дохід", "Витрата"],
            corner_radius=15
        )
        self.type_option.grid(row=0, column=1, padx=20, pady=(20, 5), sticky="we")

        amount_label = ctk.CTkLabel(form, text="Сума:", font=ctk.CTkFont(size=14, weight="bold"))
        amount_label.grid(row=1, column=0, padx=20, pady=10, sticky="w")

        self.amount_entry = ctk.CTkEntry(form, placeholder_text="Наприклад: 1500", corner_radius=15)
        self.amount_entry.grid(row=1, column=1, padx=20, pady=10, sticky="we")

        category_label = ctk.CTkLabel(form, text="Категорія:", font=ctk.CTkFont(size=14, weight="bold"))
        category_label.grid(row=2, column=0, padx=20, pady=10, sticky="w")

        self.category_entry = ctk.CTkEntry(form, placeholder_text="Наприклад: Їжа", corner_radius=15)
        self.category_entry.grid(row=2, column=1, padx=20, pady=10, sticky="we")

        date_label = ctk.CTkLabel(form, text="Дата (YYYY-MM-DD):", font=ctk.CTkFont(size=14, weight="bold"))
        date_label.grid(row=3, column=0, padx=20, pady=10, sticky="w")

        self.date_entry = ctk.CTkEntry(form, placeholder_text="2026-01-15", corner_radius=15)
        self.date_entry.grid(row=3, column=1, padx=20, pady=10, sticky="we")

        add_btn = ctk.CTkButton(
            form,
            text="Зберегти транзакцію",
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER,
            text_color="#1a1a1a",
            corner_radius=18,
            height=45,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.add_transaction
        )
        add_btn.grid(row=4, column=0, columnspan=2, padx=20, pady=(20, 20), sticky="we")

    def add_transaction(self):
        transaction_type = self.type_option.get()
        category = self.category_entry.get().strip().capitalize()
        amount = self.amount_entry.get().strip()
        date = self.date_entry.get().strip()

        if not category or not amount or not date:
            messagebox.showerror("Помилка", "Заповніть всі поля!")
            return

        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Помилка", "Сума повинна бути числом більше 0!")
            return

        try:
            datetime.strptime(date, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Помилка", "Дата повинна бути у форматі YYYY-MM-DD!")
            return

        if transaction_type == "Дохід":
            self.manager.add_income(amount, category, date)
            messagebox.showinfo("Успіх", "Дохід додано!")
        else:
            self.manager.add_expense(amount, category, date)
            messagebox.showinfo("Успіх", "Витрату додано!")

        self.refresh_profile_info()

        self.amount_entry.delete(0, "end")
        self.category_entry.delete(0, "end")
        self.date_entry.delete(0, "end")


    def show_transactions(self):
        self.clear_content()

        title_label = ctk.CTkLabel(
            self.content_frame,
            text=f"Транзакції — {self.manager.get_active_profile()}",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=ACCENT_COLOR
        )
        title_label.pack(pady=(26, 15), padx=30, anchor="w")

        container = ctk.CTkFrame(self.content_frame, fg_color=BG_COLOR)
        container.pack(fill="both", expand=True, padx=30, pady=10)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.transactions_textbox = ctk.CTkTextbox(container, corner_radius=15, height=420)
        self.transactions_textbox.grid(row=0, column=0, sticky="nsew", pady=(0, 10))

        button_frame = ctk.CTkFrame(container, fg_color=BG_COLOR)
        button_frame.grid(row=1, column=0, sticky="we")
        button_frame.grid_columnconfigure((0, 1, 2), weight=1)

        refresh_btn = ctk.CTkButton(
            button_frame,
            text="🔄 Оновити",
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER,
            text_color="#1a1a1a",
            corner_radius=18,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.load_transactions
        )
        refresh_btn.grid(row=0, column=0, padx=5, pady=5, sticky="we")

        edit_btn = ctk.CTkButton(
            button_frame,
            text="✏ Редагувати",
            fg_color="#5bc0de",
            hover_color="#31b0d5",
            text_color="white",
            corner_radius=18,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.edit_selected_transaction
        )
        edit_btn.grid(row=0, column=1, padx=5, pady=5, sticky="we")

        delete_btn = ctk.CTkButton(
            button_frame,
            text="🗑 Видалити",
            fg_color="#d9534f",
            hover_color="#c9302c",
            text_color="white",
            corner_radius=18,
            height=40,
            font=ctk.CTkFont(size=14, weight="bold"),
            command=self.delete_selected_transaction
        )
        delete_btn.grid(row=0, column=2, padx=5, pady=5, sticky="we")

        self.load_transactions()

    def load_transactions(self):
        self.transactions_textbox.configure(state="normal")
        self.transactions_textbox.delete("1.0", "end")

        self.transactions_cache = self.manager.get_transactions_with_index()

        if not self.transactions_cache:
            self.transactions_textbox.insert("end", "Немає транзакцій.\n")
            self.transactions_textbox.configure(state="disabled")
            return

        for i, t in enumerate(self.transactions_cache):
            t_type = "ДОХІД" if t["type"] == "income" else "ВИТРАТА"
            self.transactions_textbox.insert(
                "end",
                f"{i+1}. [{t['date']}] {t_type} | {t['category']} | {t['amount']} грн\n"
            )

        self.transactions_textbox.configure(state="disabled")

    def delete_selected_transaction(self):
        if not hasattr(self, "transactions_cache") or not self.transactions_cache:
            messagebox.showerror("Помилка", "Список транзакцій порожній.")
            return

        try:
            cursor_position = self.transactions_textbox.index("insert")
            line_number = int(cursor_position.split(".")[0]) - 1
        except Exception:
            messagebox.showerror("Помилка", "Не вдалося визначити транзакцію.")
            return

        if line_number < 0 or line_number >= len(self.transactions_cache):
            messagebox.showerror("Помилка", "Оберіть транзакцію (поставте курсор на рядок).")
            return

        transaction = self.transactions_cache[line_number]

        confirm = messagebox.askyesno(
            "Підтвердження",
            f"Видалити транзакцію?\n\n"
            f"Дата: {transaction['date']}\n"
            f"Категорія: {transaction['category']}\n"
            f"Сума: {transaction['amount']} грн"
        )

        if not confirm:
            return

        success = self.manager.delete_transaction(transaction["type"], transaction["index"])

        if success:
            messagebox.showinfo("Успіх", "Транзакцію видалено!")
            self.load_transactions()
            self.refresh_profile_info()
        else:
            messagebox.showerror("Помилка", "Не вдалося видалити транзакцію.")

    def edit_selected_transaction(self):
        if not hasattr(self, "transactions_cache") or not self.transactions_cache:
            messagebox.showerror("Помилка", "Список транзакцій порожній.")
            return

        try:
            cursor_position = self.transactions_textbox.index("insert")
            line_number = int(cursor_position.split(".")[0]) - 1
        except Exception:
            messagebox.showerror("Помилка", "Не вдалося визначити транзакцію.")
            return

        if line_number < 0 or line_number >= len(self.transactions_cache):
            messagebox.showerror("Помилка", "Оберіть транзакцію (поставте курсор на рядок).")
            return

        transaction = self.transactions_cache[line_number]

        edit_window = ctk.CTkToplevel(self)
        edit_window.title("Редагувати транзакцію")
        edit_window.geometry("420x420")
        edit_window.resizable(False, False)

        ctk.CTkLabel(edit_window, text="Тип", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(15, 5))
        type_var = ctk.StringVar(value="Дохід" if transaction["type"] == "income" else "Витрата")
        ctk.CTkOptionMenu(edit_window, values=["Дохід", "Витрата"], variable=type_var).pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(edit_window, text="Сума", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        amount_entry = ctk.CTkEntry(edit_window)
        amount_entry.insert(0, str(transaction["amount"]))
        amount_entry.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(edit_window, text="Категорія", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        category_entry = ctk.CTkEntry(edit_window)
        category_entry.insert(0, transaction["category"])
        category_entry.pack(pady=5, padx=20, fill="x")

        ctk.CTkLabel(edit_window, text="Дата (YYYY-MM-DD)", font=ctk.CTkFont(size=14, weight="bold")).pack(pady=(10, 5))
        date_entry = ctk.CTkEntry(edit_window)
        date_entry.insert(0, transaction["date"])
        date_entry.pack(pady=5, padx=20, fill="x")

        def save_edit():
            new_type = "income" if type_var.get() == "Дохід" else "expense"
            new_amount = amount_entry.get().strip()
            new_category = category_entry.get().strip()
            new_date = date_entry.get().strip()

            if not new_amount or not new_category or not new_date:
                messagebox.showerror("Помилка", "Заповніть всі поля.")
                return

            try:
                new_amount = float(new_amount)
                if new_amount <= 0:
                    raise ValueError
            except ValueError:
                messagebox.showerror("Помилка", "Сума повинна бути числом більше 0.")
                return

            try:
                datetime.strptime(new_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showerror("Помилка", "Дата повинна бути у форматі YYYY-MM-DD.")
                return

            if new_type == transaction["type"]:
                success = self.manager.update_transaction(
                    transaction["type"],
                    transaction["index"],
                    new_amount,
                    new_category,
                    new_date
                )
            else:
                self.manager.delete_transaction(transaction["type"], transaction["index"])
                if new_type == "income":
                    self.manager.add_income(new_amount, new_category, new_date)
                else:
                    self.manager.add_expense(new_amount, new_category, new_date)
                success = True

            if success:
                messagebox.showinfo("Успіх", "Транзакцію оновлено.")
                edit_window.destroy()
                self.load_transactions()
                self.refresh_profile_info()
            else:
                messagebox.showerror("Помилка", "Не вдалося оновити транзакцію.")

        ctk.CTkButton(
            edit_window,
            text="Зберегти зміни",
            command=save_edit,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER,
            text_color="#1a1a1a",
            corner_radius=14,
            height=42,
            font=ctk.CTkFont(size=14, weight="bold")
        ).pack(pady=(20, 15), padx=20, fill="x")

    def show_analytics(self):
        self.clear_content()

        title = ctk.CTkLabel(
            self.content_frame,
            text=f"Аналітика — {self.manager.get_active_profile()}",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=ACCENT_COLOR
        )
        title.pack(pady=(26, 15), padx=30, anchor="w")

        frame = ctk.CTkFrame(self.content_frame, fg_color=CARD_COLOR, corner_radius=20)
        frame.pack(fill="both", expand=True, padx=30, pady=10)

        frame.grid_columnconfigure((0, 1), weight=1)
        frame.grid_rowconfigure((0, 1), weight=1)

        expenses_cat = self.analytics.expenses_by_category()
        income_cat = self.analytics.income_by_category()

        chart1 = ctk.CTkFrame(frame, fg_color="#ffffff", corner_radius=15)
        chart1.grid(row=0, column=0, padx=15, pady=15, sticky="nsew")

        chart2 = ctk.CTkFrame(frame, fg_color="#ffffff", corner_radius=15)
        chart2.grid(row=0, column=1, padx=15, pady=15, sticky="nsew")

        chart3 = ctk.CTkFrame(frame, fg_color="#ffffff", corner_radius=15)
        chart3.grid(row=1, column=0, columnspan=2, padx=15, pady=15, sticky="nsew")

        self.charts.draw_expenses_pie(expenses_cat, chart1)
        self.charts.draw_income_pie(income_cat, chart2)
        self.charts.draw_expenses_line(self.analytics.expenses_by_month(), chart3)


    def show_forecast(self):
        self.clear_content()

        title = ctk.CTkLabel(
            self.content_frame,
            text=f"Прогноз витрат (AI) — {self.manager.get_active_profile()}",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=ACCENT_COLOR
        )
        title.pack(pady=(26, 15), padx=30, anchor="w")

        controls = ctk.CTkFrame(self.content_frame, fg_color=CARD_COLOR, corner_radius=20)
        controls.pack(fill="x", padx=30, pady=(0, 10))

        ctk.CTkLabel(
            controls,
            text="Вікно аналізу",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=0, padx=20, pady=(15, 5), sticky="w")

        ctk.CTkLabel(
            controls,
            text="Модель",
            font=ctk.CTkFont(size=14, weight="bold")
        ).grid(row=0, column=1, padx=20, pady=(15, 5), sticky="w")

        self.window_option = ctk.CTkOptionMenu(controls, values=["30", "60", "90"])
        self.window_option.grid(row=1, column=0, padx=20, pady=(0, 15), sticky="we")
        self.window_option.set("30")

        self.model_option = ctk.CTkOptionMenu(
            controls,
            values=["linear", "average", "weighted"]
        )
        self.model_option.grid(row=1, column=1, padx=20, pady=(0, 15), sticky="we")
        self.model_option.set("linear")

        controls.grid_columnconfigure((0, 1), weight=1)

        result_frame = ctk.CTkFrame(self.content_frame, fg_color=BG_COLOR)
        result_frame.pack(fill="both", expand=True, padx=0, pady=0)

        def render_forecast():
            for widget in result_frame.winfo_children():
                widget.destroy()

            window = int(self.window_option.get())
            model = self.model_option.get()

            result = self.forecaster.forecast_with_model(window_days=window, model=model)

            box = ctk.CTkFrame(result_frame, fg_color=CARD_COLOR, corner_radius=20)
            box.pack(fill="x", padx=30, pady=10)

            if result["status"] == "error":
                ctk.CTkLabel(
                    box,
                    text=result["message"],
                    text_color="red",
                    font=ctk.CTkFont(size=14)
                ).pack(pady=20)
                return

            info_text = (
                f"Модель: {result['model']}\n"
                f"Вікно аналізу: {result['window']} днів\n"
                f"Прогноз загальних витрат на наступні 30 днів: {result['total_forecast']} грн\n"
                f"MAE: {result['mae']} | MSE: {result['mse']} | R²: {result['r2']}\n"
                f"Тренд витрат: {result['trend']}"
            )

            ctk.CTkLabel(
                box,
                text=info_text,
                font=ctk.CTkFont(size=15, weight="bold"),
                text_color=ACCENT_COLOR,
                justify="left"
            ).pack(pady=(20, 15), padx=20, anchor="w")

            rec_title = ctk.CTkLabel(
                result_frame,
                text="AI-рекомендації:",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=TEXT_COLOR
            )
            rec_title.pack(pady=(15, 5), padx=30, anchor="w")

            rec_box = ctk.CTkTextbox(result_frame, height=120, corner_radius=15)
            rec_box.pack(fill="x", padx=30, pady=(0, 15))
            rec_box.configure(state="normal")

            recommendations = self.forecaster.generate_ai_recommendations(window_days=window)
            for rec in recommendations:
                rec_box.insert("end", f"• {rec}\n")

            rec_box.configure(state="disabled")

            chart_title = ctk.CTkLabel(
                result_frame,
                text="Графік прогнозування:",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=TEXT_COLOR
            )
            chart_title.pack(pady=(10, 5), padx=30, anchor="w")

            chart_frame = ctk.CTkFrame(result_frame, fg_color="#ffffff", corner_radius=15)
            chart_frame.pack(fill="x", padx=30, pady=(0, 15))

            self.charts.draw_forecast_chart(
                result["daily_history"],
                result["future_forecast"],
                chart_frame
            )

            cat_forecast = self.forecaster.forecast_by_category(window_days=window)

            cat_title = ctk.CTkLabel(
                result_frame,
                text="Прогноз по категоріях:",
                font=ctk.CTkFont(size=18, weight="bold"),
                text_color=TEXT_COLOR
            )
            cat_title.pack(pady=(10, 5), padx=30, anchor="w")

            cat_box = ctk.CTkTextbox(result_frame, height=170, corner_radius=15)
            cat_box.pack(fill="x", padx=30, pady=(0, 24))
            cat_box.configure(state="normal")

            if cat_forecast:
                for cat, val in cat_forecast.items():
                    cat_box.insert("end", f"• {cat}: {val} грн\n")
            else:
                cat_box.insert("end", "Недостатньо даних для прогнозу по категоріях.\n")

            cat_box.configure(state="disabled")

        ctk.CTkButton(
            controls,
            text="Побудувати прогноз",
            command=render_forecast,
            fg_color=BUTTON_COLOR,
            hover_color=BUTTON_HOVER,
            text_color="#1a1a1a",
            corner_radius=15,
            height=40,
            font=ctk.CTkFont(size=13, weight="bold")
        ).grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 15), sticky="we")

        render_forecast()

    def export_csv(self):
        self.manager.export_to_csv()
        messagebox.showinfo("Експорт", "Файл report.csv збережено у папці exports/")