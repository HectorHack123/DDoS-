import threading
import requests
import time
from tkinter import Tk, Frame, Label, Entry, Button, ttk
from tkinter import messagebox
import random
from tkinter import Canvas

class StressTestApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Stress Test Tool")
        self.running = False

        # Configurarea interfeței
        self.create_widgets()

    def create_widgets(self):
        # Secțiunea de configurare
        config_frame = Frame(self.root, padx=10, pady=10, bg="black")
        config_frame.pack(fill="x")

        Label(config_frame, text="Target URL/IP:", fg="red", bg="black").grid(row=0, column=0, sticky="w")
        self.target_entry = Entry(config_frame, width=30, bg="black", fg="white", insertbackground="white")
        self.target_entry.grid(row=0, column=1, pady=5)

        Label(config_frame, text="Threads:", fg="red", bg="black").grid(row=1, column=0, sticky="w")
        self.threads_entry = Entry(config_frame, width=10, bg="black", fg="white", insertbackground="white")
        self.threads_entry.grid(row=1, column=1, pady=5, sticky="w")

        Label(config_frame, text="Duration (s):", fg="red", bg="black").grid(row=2, column=0, sticky="w")
        self.duration_entry = Entry(config_frame, width=10, bg="black", fg="white", insertbackground="white")
        self.duration_entry.grid(row=2, column=1, pady=5, sticky="w")

        self.start_button = Button(config_frame, text="Start Test", command=self.start_test, bg="darkred", fg="white")
        self.start_button.grid(row=3, column=0, pady=10, sticky="w")

        self.stop_button = Button(config_frame, text="Stop Test", command=self.stop_test, bg="red", fg="white")
        self.stop_button.grid(row=3, column=1, pady=10, sticky="w")

        # Secțiunea tabelului
        self.tree = ttk.Treeview(self.root, columns=("#1", "#2"), show="headings", height=10)
        self.tree.heading("#1", text="Target")
        self.tree.heading("#2", text="Status")
        self.tree.pack(fill="x", padx=10, pady=10)

        # Personalizare stil tabel
        style = ttk.Style()
        style.configure("Treeview", background="black", foreground="white", fieldbackground="black", rowheight=25)
        style.map("Treeview", background=[("selected", "red")])

        # Secțiunea graficului
        self.canvas = Canvas(self.root, width=500, height=300, bg="black", highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)
        self.success_count = 0
        self.error_count = 0

    def send_request(self, target):
        try:
            if not target.startswith("http"):
                target = f"http://{target}"
            response = requests.get(target, timeout=5)
            self.update_table(target, f"Success ({response.status_code})")
            self.success_count += 1
        except requests.exceptions.RequestException as e:
            self.update_table(target, f"Error ({str(e)})")
            self.error_count += 1

        self.update_graph()

    def update_table(self, target, status):
        self.tree.insert("", "end", values=(target, status))

    def update_graph(self):
        self.canvas.delete("all")
        total = self.success_count + self.error_count
        if total > 0:
            success_height = (self.success_count / total) * 300
            error_height = (self.error_count / total) * 300

            # Bar for success
            self.animate_bar(100, 300 - success_height, 200, 300, fill="darkgreen", outline="white", label=f"Success: {self.success_count}", label_color="white")

            # Bar for error
            self.animate_bar(300, 300 - error_height, 400, 300, fill="darkred", outline="white", label=f"Error: {self.error_count}", label_color="white")

    def animate_bar(self, x1, y1, x2, y2, fill, outline, label, label_color):
        current_height = 300
        target_height = y1
        steps = 20
        delta = (current_height - target_height) / steps

        for i in range(steps):
            self.canvas.delete("bar")
            self.canvas.create_rectangle(x1, current_height - delta * (i + 1), x2, 300, fill=fill, outline=outline, tags="bar")
            self.canvas.update()
            time.sleep(0.02)

        self.canvas.create_text((x1 + x2) / 2, target_height - 10, text=label, fill=label_color, font=("Arial", 12, "bold"))

    def stress_test(self, target, num_threads, duration):
        start_time = time.time()
        threads = []
        while self.running and (time.time() - start_time) < duration:
            for _ in range(num_threads):
                if not self.running:
                    break
                thread = threading.Thread(target=self.send_request, args=(target,))
                thread.start()
                threads.append(thread)
            time.sleep(0.05)

        for thread in threads:
            thread.join()

    def start_test(self):
        target = self.target_entry.get().strip()
        try:
            num_threads = int(self.threads_entry.get().strip())
            duration = int(self.duration_entry.get().strip())
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter valid numbers for threads and duration.")
            return

        if not target:
            messagebox.showerror("Invalid Input", "Please enter a target URL or IP.")
            return

        self.running = True
        threading.Thread(target=self.stress_test, args=(target, num_threads, duration), daemon=True).start()

    def stop_test(self):
        self.running = False

if __name__ == "__main__":
    root = Tk()
    app = StressTestApp(root)

    # Add dramatic flicker effect to the window
    def flicker_effect():
        colors = ["#400000", "#800000", "#000000"]
        while True:
            color = random.choice(colors)
            root.configure(bg=color)
            time.sleep(0.1)

    threading.Thread(target=flicker_effect, daemon=True).start()
    root.mainloop()
