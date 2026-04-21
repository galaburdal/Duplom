import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.patches import Rectangle
from datetime import datetime


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

    def _prepare_pie_data(self, data, top_n=6):
        """
        Сортує категорії за спаданням.
        Якщо категорій забагато — залишає найбільші,
        решту об'єднує в 'Інші'.
        """
        if not data:
            return [], []

        sorted_items = sorted(data.items(), key=lambda x: x[1], reverse=True)

        if len(sorted_items) <= top_n:
            labels = [item[0] for item in sorted_items]
            values = [item[1] for item in sorted_items]
            return labels, values

        main_items = sorted_items[:top_n]
        other_items = sorted_items[top_n:]

        other_sum = sum(value for _, value in other_items)

        labels = [item[0] for item in main_items]
        values = [item[1] for item in main_items]

        if other_sum > 0:
            labels.append("Інші")
            values.append(other_sum)

        return labels, values

    def _autopct_visible_only(self, pct):
        """
        Показує відсоток тільки для відносно помітних секторів,
        щоб текст не злипався.
        """
        return f"{pct:.1f}%" if pct >= 5 else ""

    def _draw_side_legend(self, ax, labels, values, colors, title="Категорії"):
        """
        Малює власну 'легенду' у правій частині фігури,
        щоб нічого не обрізалось і не накладалось на діаграму.
        """
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.axis("off")

        total = sum(values)
        ax.text(
            0.0, 0.95, title,
            fontsize=11, fontweight="bold",
            ha="left", va="top"
        )

        y = 0.85
        line_step = 0.10 if len(labels) <= 6 else 0.085

        for label, value, color in zip(labels, values, colors):
            percent = (value / total) * 100 if total else 0

            ax.add_patch(
                Rectangle((0.0, y - 0.03), 0.06, 0.03, facecolor=color, edgecolor="none")
            )

            ax.text(
                0.09, y - 0.005,
                f"{label} — {percent:.1f}%",
                fontsize=9,
                ha="left",
                va="center"
            )
            y -= line_step

    def _draw_pie_with_side_legend(self, data, frame, title):
        self.clear_frame(frame)

        if not data:
            return

        labels, values = self._prepare_pie_data(data, top_n=6)

        fig = plt.figure(figsize=(6.8, 4.2), dpi=110)
        gs = fig.add_gridspec(1, 2, width_ratios=[1.55, 1.0], wspace=0.02)

        ax_pie = fig.add_subplot(gs[0, 0])
        ax_legend = fig.add_subplot(gs[0, 1])

        wedges, texts, autotexts = ax_pie.pie(
            values,
            autopct=self._autopct_visible_only,
            startangle=90,
            pctdistance=0.68
        )

        for t in texts:
            t.set_visible(False)

        ax_pie.set_title(title, fontsize=12)
        ax_pie.axis("equal")

        colors = [w.get_facecolor() for w in wedges]
        self._draw_side_legend(ax_legend, labels, values, colors, title="Категорії")

        fig.subplots_adjust(left=0.04, right=0.98, top=0.88, bottom=0.08)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def draw_expenses_pie(self, data, frame):
        self._draw_pie_with_side_legend(data, frame, "Витрати по категоріях")

    def draw_income_pie(self, data, frame):
        self._draw_pie_with_side_legend(data, frame, "Доходи по категоріях")

    def draw_expenses_line(self, data, frame):
        self.clear_frame(frame)

        if not data:
            return

        try:
            parsed = []
            for month, value in data.items():
                parsed.append((datetime.strptime(month, "%Y-%m"), value))
            parsed.sort(key=lambda x: x[0])

            months = [dt.strftime("%Y-%m") for dt, _ in parsed]
            values = [value for _, value in parsed]
        except Exception:
            months = list(data.keys())
            values = list(data.values())

        fig, ax = plt.subplots(figsize=(10, 3.8), dpi=110)

        ax.plot(months, values, marker="o", linewidth=2)

        ax.set_title("Динаміка витрат по місяцях", fontsize=12)
        ax.set_xlabel("Місяць")
        ax.set_ylabel("Сума витрат")
        ax.grid(True)

        plt.setp(ax.get_xticklabels(), rotation=40, ha="right")

        fig.subplots_adjust(left=0.08, right=0.98, top=0.88, bottom=0.28)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)

    def draw_forecast_chart(self, history_df, forecast_df, frame):
        self.clear_frame(frame)

        if history_df is None or forecast_df is None or len(history_df) == 0 or len(forecast_df) == 0:
            return

        fig, ax = plt.subplots(figsize=(10, 4.2), dpi=110)

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

        last_date = history_df["date"].max()
        ax.axvline(last_date, linestyle=":", linewidth=2)

        ax.set_title("Прогноз витрат на наступні 30 днів", fontsize=12)
        ax.set_xlabel("Дата")
        ax.set_ylabel("Сума витрат")
        ax.legend()
        ax.grid(True)

        plt.setp(ax.get_xticklabels(), rotation=40, ha="right")

        fig.subplots_adjust(left=0.08, right=0.98, top=0.88, bottom=0.28)

        canvas = FigureCanvasTkAgg(fig, master=frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="both", expand=True)