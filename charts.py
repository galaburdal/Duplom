import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


plt.rcParams["figure.facecolor"] = "#f8f1e7"
plt.rcParams["axes.facecolor"] = "#f8f1e7"
plt.rcParams["axes.edgecolor"] = "#333333"
plt.rcParams["text.color"] = "#111111"
plt.rcParams["axes.labelcolor"] = "#111111"
plt.rcParams["xtick.color"] = "#111111"
plt.rcParams["ytick.color"] = "#111111"


class ChartBuilder:
    def clear_frame(self, frame):
        for widget in frame.winfo_children():
            widget.destroy()

    def draw_expenses_pie(self, data, frame):
        self.clear_frame(frame)

        if not data:
            return

        labels = list(data.keys())
        values = list(data.values())
        total = sum(values)

        def autopct_func(pct):
            return f"{pct:.1f}%" if pct >= 6 else ""

        legend_labels = [
            f"{label} — {value / total * 100:.1f}%"
            for label, value in zip(labels, values)
        ]

        fig, ax = plt.subplots(figsize=(6.4, 4), dpi=110)

        wedges, texts, autotexts = ax.pie(
            values,
            autopct=autopct_func,
            startangle=90,
            pctdistance=0.72,
            textprops={"fontsize": 11, "color": "#111111"}
        )

        for t in texts:
            t.set_visible(False)

        ax.set_title("Витрати по категоріях", fontsize=13, pad=12)

        ax.legend(
            wedges,
            legend_labels,
            title="Категорії",
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            fontsize=10,
            title_fontsize=11,
            frameon=True
        )

        fig.tight_layout(pad=2)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def draw_income_pie(self, data, frame):
        self.clear_frame(frame)

        if not data:
            return

        labels = list(data.keys())
        values = list(data.values())
        total = sum(values)

        def autopct_func(pct):
            return f"{pct:.1f}%" if pct >= 6 else ""

        legend_labels = [
            f"{label} — {value / total * 100:.1f}%"
            for label, value in zip(labels, values)
        ]

        fig, ax = plt.subplots(figsize=(6.4, 4), dpi=110)

        wedges, texts, autotexts = ax.pie(
            values,
            autopct=autopct_func,
            startangle=90,
            pctdistance=0.72,
            textprops={"fontsize": 11, "color": "#111111"}
        )

        for t in texts:
            t.set_visible(False)

        ax.set_title("Доходи по категоріях", fontsize=13, pad=12)

        ax.legend(
            wedges,
            legend_labels,
            title="Категорії",
            loc="center left",
            bbox_to_anchor=(1.02, 0.5),
            fontsize=10,
            title_fontsize=11,
            frameon=True
        )

        fig.tight_layout(pad=2)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def draw_expenses_line(self, data, frame):
        self.clear_frame(frame)

        if not data:
            return

        months = list(data.keys())
        values = list(data.values())

        fig, ax = plt.subplots(figsize=(10, 3.5), dpi=110)

        ax.plot(months, values, marker="o", linewidth=2)

        ax.set_title("Динаміка витрат по місяцях", fontsize=12)
        ax.set_xlabel("Місяць")
        ax.set_ylabel("Сума витрат")
        ax.grid(True)

        fig.autofmt_xdate(rotation=45)
        fig.tight_layout(pad=2)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def draw_forecast_chart(self, history_df, forecast_df, frame):
        self.clear_frame(frame)

        if history_df is None or forecast_df is None:
            return

        fig, ax = plt.subplots(figsize=(10, 4), dpi=110)

        ax.plot(
            history_df["date"],
            history_df["amount"],
            marker="o",
            linewidth=2,
            label="Історичні витрати"
        )

        ax.plot(
            forecast_df["date"],
            forecast_df["forecast"],
            marker="o",
            linestyle="--",
            linewidth=2,
            label="Прогноз витрат"
        )

        if len(history_df) > 0:
            last_date = history_df["date"].max()
            ax.axvline(last_date, linestyle=":", linewidth=2)

        ax.set_title("Прогноз витрат на наступні 30 днів", fontsize=12)
        ax.set_xlabel("Дата")
        ax.set_ylabel("Сума витрат")
        ax.legend()
        ax.grid(True)

        fig.autofmt_xdate(rotation=45)
        fig.tight_layout(pad=2)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)