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

        fig, ax = plt.subplots(figsize=(6, 4), dpi=110)

        wedges, texts, autotexts = ax.pie(
            values,
            autopct="%1.1f%%",
            startangle=90,
            pctdistance=0.70
        )

        ax.set_title("Витрати по категоріях", fontsize=12)

        for t in texts:
            t.set_visible(False)

        ax.legend(
            wedges,
            labels,
            loc="center left",
            bbox_to_anchor=(1.05, 0.5),
            fontsize=9,
            title="Категорії"
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

        fig, ax = plt.subplots(figsize=(6, 4), dpi=110)

        wedges, texts, autotexts = ax.pie(
            values,
            autopct="%1.1f%%",
            startangle=90,
            pctdistance=0.70
        )

        ax.set_title("Доходи по категоріях", fontsize=12)

        for t in texts:
            t.set_visible(False)

        ax.legend(
            wedges,
            labels,
            loc="center left",
            bbox_to_anchor=(1.05, 0.5),
            fontsize=9,
            title="Категорії"
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