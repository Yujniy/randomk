import random
import tkinter as tk
import tkinter.messagebox

class ActivationWindow:
    def __init__(self, master):
        self.master = master
        master.title("Активация")
        master.geometry("300x250")

        self.frame = tk.Frame(master)
        self.frame.pack(expand=True)

        self.label = tk.Label(self.frame, text="Введите ключ активации:")
        self.label.grid(row=0, column=0, columnspan=2, sticky="ew")

        self.entry = tk.Entry(self.frame, show="*")
        self.entry.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.activate_button = tk.Button(self.frame, text="Активировать", command=self.check_activation)
        self.activate_button.grid(row=2, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        self.frame.grid_rowconfigure(1, weight=1)  # Make the entry row expand vertically
        self.frame.grid_columnconfigure(0, weight=1)  # Make the first column expand horizontally

        self.entry.bind("<Return>", self.check_activation_enter)

    def check_activation(self):
        activation_key = self.entry.get()
        self.activate(activation_key)

    def check_activation_enter(self, event):
        activation_key = self.entry.get()
        self.activate(activation_key)

    def activate(self, key):
        key_lower = key.lower()
        if key_lower == "тесторобот" or key_lower == "тесторобот".upper():
            self.master.destroy()

            root = tk.Tk()
            app = RandomNumberGenerator(root)
            root.mainloop()

        else:
            tk.messagebox.showerror("Ошибка", "Неверный ключ активации.")

class RandomNumberGenerator:
    def __init__(self, master):
        self.master = master
        master.title("Генератор случайных чисел")

        self.label = tk.Label(master, text="Введите диапазон для генерации числа:")
        self.label.pack()

        self.min_label = tk.Label(master, text="Минимальное значение:")
        self.min_label.pack()

        self.min_entry = tk.Entry(master)
        self.min_entry.pack(fill="x", padx=10)

        self.max_label = tk.Label(master, text="Максимальное значение:")
        self.max_label.pack()

        self.max_entry = tk.Entry(master)
        self.max_entry.pack(fill="x", padx=10)

        self.num_results_label = tk.Label(master, text="Количество результатов (до 10):")
        self.num_results_label.pack()

        self.num_results_entry = tk.Entry(master)
        self.num_results_entry.pack(fill="x", padx=10)

        self.exclude_endpoints_var = tk.IntVar()
        self.exclude_endpoints_checkbutton = tk.Checkbutton(master, text="Игнорировать конечные числа", variable=self.exclude_endpoints_var)
        self.exclude_endpoints_checkbutton.pack(padx=10, pady=5)

        self.unique_var = tk.IntVar()
        self.unique_checkbutton = tk.Checkbutton(master, text="Не повторяться", variable=self.unique_var)
        self.unique_checkbutton.pack(padx=10, pady=5)

        self.generate_button = tk.Button(master, text="Сгенерировать", command=self.generate)
        self.generate_button.pack(fill="x", padx=10, pady=5)

        self.result_label = tk.Label(master, text="")
        self.result_label.pack()

        self.copy_button = tk.Button(master, text="Копировать", command=self.copy_result)
        self.copy_button.pack(fill="x", padx=10, pady=5)

        self.reset_button = tk.Button(master, text="Сброс параметров", command=self.reset)
        self.reset_button.pack(fill="x", padx=10, pady=5)

    def generate(self):
        try:
            min_value = int(self.min_entry.get())
            max_value = int(self.max_entry.get())
            num_results = int(self.num_results_entry.get())

            if min_value <= max_value and num_results > 0 and num_results <= max_value - min_value + 1:
                if self.exclude_endpoints_var.get() == 1 and min_value == max_value:
                    tk.messagebox.showerror("Ошибка", "Минимальное значение не может быть равно максимальному, если включена опция 'Игнорировать конечные числа'.")
                else:
                    results = []
                    if self.exclude_endpoints_var.get() == 1:
                        results = random.sample(range(min_value + 1, max_value), min(max_value - min_value - 1, num_results))
                    else:
                        results = random.sample(range(min_value, max_value + 1), min(max_value - min_value + 1, num_results))

                    if self.unique_var.get() == 1:
                        results = list(set(results))
                    self.result_label.config(text="\n".join(map(str, results)))
            else:
                tk.messagebox.showerror("Ошибка", "Пожалуйста, введите корректные значения для минимального значения, максимального значения и количества результатов (до 10).")
        except ValueError:
            tk.messagebox.showerror("Ошибка", "Пожалуйста, введите целые числа для минимального значения, максимального значения и количества результатов.")

    def copy_result(self):
        self.master.clipboard_clear()
        self.master.clipboard_append(self.result_label.cget("text"))

    def reset(self):
        self.min_entry.delete(0, tk.END)
        self.max_entry.delete(0, tk.END)
        self.num_results_entry.delete(0, tk.END)
        self.exclude_endpoints_var.set(0)  # Сброс состояния галочки "Игнорировать конечные числа"
        self.unique_var.set(0)  # Сброс состояния галочки "Не повторяться"
        self.result_label.config(text="")

root = tk.Tk()
app = ActivationWindow(root)
root.mainloop()