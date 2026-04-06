import customtkinter as ctk
from tkinter import messagebox
from finance import PersonalFinanceManager
from analytics import FinanceAnalytics
from forecast import ExpenseForecaster
from charts import ChartBuilder
from datetime import datetime


# --- Стиль програми ---
ctk.set_appearance_mode("dark")  # dark mode
ctk.set_default_color_theme("blue")


# --- Основні кольори (ніжний бежевий стиль) ---
BG_COLOR = "#1e1e1e"
SIDEBAR_COLOR = "#2a2a2a"
CARD_COLOR = "#2f2f2f"
BUTTON_COLOR = "#c8b6a6"      # ніжний беж
BUTTON_HOVER = "#bfa892"
TEXT_COLOR = "#f2f2f2"
ACCENT_COLOR = "#e0c9a6"


class FinanceApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Personal Finance Manager Pro")
        self.geometry("1100x700")
        self.minsize(1100, 700)

        # --- Менеджери ---
        self.manager = PersonalFinanceManager()
        self.analytics = FinanceAnalytics(self.manager)
        self.forecaster = ExpenseForecaster(self.manager)
        self.charts = ChartBuilder()

        # --- Основний контейнер ---
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=250, fg_color=SIDEBAR_COLOR, corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nswe")
        self.sidebar.grid_rowconfigure(8, weight=1)

        self.logo_label = ctk.CTkLabel(
            self.sidebar,
            text="Finance Pro",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=ACCENT_COLOR
        )
        self.logo_label.grid(row=0, column=0, padx=20, pady=(25, 15))

        self.menu_label = ctk.CTkLabel(
            self.sidebar,
            text="Меню",
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color=TEXT_COLOR
        )
        self.menu_label.grid(row=1, column=0, padx=20, pady=(0, 10), sticky="w")

        # --- Кнопки меню ---
        self.btn_dashboard = self.create_sidebar_button("📊 Dashboard", self.show_dashboard)
        self.btn_dashboard.grid(row=2, column=0, padx=20, pady=10, sticky="we")

        self.btn_add_transaction = self.create_sidebar_button("➕ Додати транзакцію", self.show_add_transaction)
        self.btn_add_transaction.grid(row=3, column=0, padx=20, pady=10, sticky="we")

        self.btn_transactions = self.create_sidebar_button("📄 Транзакції", self.show_transactions)
        self.btn_transactions.grid(row=4, column=0, padx=20, pady=10, sticky="we")

        self.btn_analytics = self.create_sidebar_button("📈 Аналітика", self.show_analytics)
        self.btn_analytics.grid(row=5, column=0, padx=20, pady=10, sticky="we")

        self.btn_forecast = self.create_sidebar_button("🤖 Прогноз", self.show_forecast)
        self.btn_forecast.grid(row=6, column=0, padx=20, pady=10, sticky="we")

        self.btn_export = self.create_sidebar_button("💾 Експорт CSV", self.export_csv)
        self.btn_export.grid(row=7, column=0, padx=20, pady=10, sticky="we")

        self.footer_label = ctk.CTkLabel(
            self.sidebar,
            text="© 2026 Finance Pro",
            font=ctk.CTkFont(size=12),
            text_color="gray"
        )
        self.footer_label.grid(row=9, column=0, padx=20, pady=20)

        # --- Контентна зона справа ---
        self.content_frame = ctk.CTkFrame(self, fg_color=BG_COLOR, corner_radius=0)
        self.content_frame.grid(row=0, column=1, sticky="nswe")
        self.content_frame.grid_columnconfigure(0, weight=1)
        self.content_frame.grid_rowconfigure(0, weight=1)

        self.current_page = None

        # стартова сторінка
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
            height=45,
            font=ctk.CTkFont(size=14, weight="bold")
        )

    def clear_content(self):
        for widget in self.content_frame.winfo_children():
            widget.destroy()

    # ==========================================================
    # DASHBOARD
    # ==========================================================
    def show_dashboard(self):
        self.clear_content()

        title = ctk.CTkLabel(
            self.content_frame,
            text="Dashboard",
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color=ACCENT_COLOR
        )
        title.pack(pady=(30, 20), padx=30, anchor="w")

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

        rec_box = ctk.CTkTextbox(self.content_frame, height=200, corner_radius=15)
        rec_box.pack(fill="x", padx=30, pady=(0, 20))
        rec_box.configure(state="normal")

        for r in report["recommendations"]:
            rec_box.insert("end", f"• {r}\n")

        rec_box.configure(state="disabled")

    def create_card(self, parent, title, value, col):
        card = ctk.CTkFrame(parent, fg_color=CARD_COLOR, corner_radius=20, height=120)
        card.grid(row=0, column=col, padx=10, pady=10, sticky="we")

        lbl_title = ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=16, weight="bold"))
        lbl_title.pack(pady=(20, 5))

        lbl_value = ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=22, weight="bold"), text_color=ACCENT_COLOR)
        lbl_value.pack()

    # ==========================================================
    # ADD TRANSACTION
    # ==========================================================
    def show_add_transaction(self):
        self.clear_content()

        title = ctk.CTkLabel(
            self.content_frame,
            text="Додати транзакцію",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=ACCENT_COLOR
        )
        title.pack(pady=(30, 20), padx=30, anchor="w")

        form = ctk.CTkFrame(self.content_frame, fg_color=CARD_COLOR, corner_radius=20)
        form.pack(padx=30, pady=10, fill="x")

        form.grid_columnconfigure((0, 1), weight=1)

        self.type_var = ctk.StringVar(value="expense")

        type_label = ctk.CTkLabel(form, text="Тип:", font=ctk.CTkFont(size=14, weight="bold"))
        type_label.grid(row=0, column=0, padx=20, pady=(20, 5), sticky="w")

        self.type_menu = ctk.CTkOptionMenu(
            form,
            values=["expense", "income"],
            variable=self.type_var,
            corner_radius=15
        )
        self.type_menu.grid(row=0, column=1, padx=20, pady=(20, 5), sticky="we")

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
        t_type = self.type_var.get()
        amount = self.amount_entry.get()
        category = self.category_entry.get()
        date = self.date_entry.get()

        if not amount or not category or not date:
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
            messagebox.showerror("Помилка", "Невірний формат дати! Використовуйте YYYY-MM-DD")
            return

        if t_type == "income":
            self.manager.add_income(amount, category, date)
        else:
            self.manager.add_expense(amount, category, date)

        messagebox.showinfo("Успіх", "Транзакцію додано!")
        self.amount_entry.delete(0, "end")
        self.category_entry.delete(0, "end")
        self.date_entry.delete(0, "end")

    # ==========================================================
    # TRANSACTIONS LIST
    # ==========================================================
    def show_transactions(self):
        self.clear_content()

        title = ctk.CTkLabel(
            self.content_frame,
            text="Транзакції",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=ACCENT_COLOR
        )
        title.pack(pady=(30, 15), padx=30, anchor="w")

        box = ctk.CTkTextbox(self.content_frame, corner_radius=15)
        box.pack(fill="both", expand=True, padx=30, pady=10)

        transactions = self.manager.get_transactions()

        box.configure(state="normal")
        box.delete("1.0", "end")

        if not transactions:
            box.insert("end", "Немає транзакцій.\n")
        else:
            for t in transactions:
                t_type = "ДОХІД" if t["type"] == "income" else "ВИТРАТА"
                box.insert("end", f"[{t['date']}] {t_type} | {t['category']} | {t['amount']} грн\n")

        box.configure(state="disabled")

    # ==========================================================
    # ANALYTICS PAGE
    # ==========================================================
    def show_analytics(self):
        self.clear_content()

        title = ctk.CTkLabel(
            self.content_frame,
            text="Аналітика",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=ACCENT_COLOR
        )
        title.pack(pady=(30, 15), padx=30, anchor="w")

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

        expenses_month = self.analytics.expenses_by_month()
        self.charts.draw_expenses_line(expenses_month, chart3)

    # ==========================================================
    # FORECAST PAGE
    # ==========================================================
    def show_forecast(self):
        self.clear_content()

        title = ctk.CTkLabel(
            self.content_frame,
            text="Прогноз витрат (AI)",
            font=ctk.CTkFont(size=26, weight="bold"),
            text_color=ACCENT_COLOR
        )
        title.pack(pady=(30, 15), padx=30, anchor="w")

        forecast_result = self.forecaster.forecast_next_month()

        box = ctk.CTkFrame(self.content_frame, fg_color=CARD_COLOR, corner_radius=20)
        box.pack(fill="x", padx=30, pady=10)

        if forecast_result["status"] == "error":
            label = ctk.CTkLabel(box, text=forecast_result["message"], text_color="red")
            label.pack(pady=20)
            return

        forecast_value = forecast_result["forecast"]
        summary = self.forecaster.get_forecast_summary()

        lbl = ctk.CTkLabel(
            box,
            text=f"Прогноз витрат на наступний місяць: {forecast_value} грн",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=ACCENT_COLOR
        )
        lbl.pack(pady=(20, 10))

        lbl2 = ctk.CTkLabel(
            box,
            text=summary,
            font=ctk.CTkFont(size=14),
            wraplength=900
        )
        lbl2.pack(pady=(0, 20))

        # Прогноз по категоріях
        cat_forecast = self.forecaster.forecast_by_category()

        text = "Прогноз витрат по категоріях:\n\n"
        for cat, val in cat_forecast.items():
            text += f"• {cat}: {val} грн\n"

        textbox = ctk.CTkTextbox(self.content_frame, height=250, corner_radius=15)
        textbox.pack(fill="x", padx=30, pady=15)
        textbox.configure(state="normal")
        textbox.insert("end", text)
        textbox.configure(state="disabled")

    # ==========================================================
    # EXPORT CSV
    # ==========================================================
    def export_csv(self):
        self.manager.export_to_csv()
        messagebox.showinfo("Експорт", "Файл report.csv збережено у папці exports/")