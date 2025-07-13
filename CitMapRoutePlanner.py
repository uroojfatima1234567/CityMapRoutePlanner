import tkinter as tk
import math
from queue import PriorityQueue
import time

cities = {
    'Lahore': (100, 200),
    'Islamabad': (300, 100),
    'Multan': (180, 320),
    'Faisalabad': (140, 230),
    'Peshawar': (400, 80),
    'Quetta': (100, 400),
    'Karachi': (100, 500),
    'Rawalpindi': (310, 130),
    'Hyderabad': (120, 460),
    'Sialkot': (120, 170),
    'Sukkur': (150, 560),
    'Bahawalpur': (200, 370),
    'Gujranwala': (130, 190),
    'Okara': (160, 260),
    'Sargodha': (170, 210),
    'Mardan': (360, 90),
    'Dera Ghazi Khan': (160, 350)
}

roads = {
    'Lahore': {'Faisalabad': 80, 'Sialkot': 60, 'Islamabad': 280, 'Gujranwala': 50, 'Sukkur': 700},
    'Faisalabad': {'Lahore': 80, 'Multan': 160, 'Islamabad': 320, 'Sargodha': 110, 'Okara': 100},
    'Islamabad': {'Lahore': 280, 'Rawalpindi': 20, 'Peshawar': 180, 'Mardan': 70},
    'Rawalpindi': {'Islamabad': 20, 'Peshawar': 160},
    'Multan': {'Faisalabad': 160, 'Quetta': 400, 'Karachi': 600, 'Bahawalpur': 100, 'Dera Ghazi Khan': 100},
    'Quetta': {'Multan': 400, 'Karachi': 700},
    'Karachi': {'Multan': 600, 'Quetta': 700, 'Hyderabad': 150, 'Sukkur': 200},
    'Hyderabad': {'Karachi': 150, 'Sukkur': 180},
    'Sialkot': {'Lahore': 60, 'Gujranwala': 40},
    'Peshawar': {'Rawalpindi': 160, 'Islamabad': 180, 'Mardan': 50},
    'Sukkur': {'Lahore': 700, 'Karachi': 200, 'Hyderabad': 180},
    'Bahawalpur': {'Multan': 100},
    'Gujranwala': {'Lahore': 50, 'Sialkot': 40},
    'Okara': {'Faisalabad': 100},
    'Sargodha': {'Faisalabad': 110},
    'Mardan': {'Islamabad': 70, 'Peshawar': 50},
    'Dera Ghazi Khan': {'Multan': 100}
}

class CityMap:
    def __init__(self, root):
        self.root = root
        self.canvas = tk.Canvas(root, width=600, height=620, bg='lightyellow')
        self.canvas.pack()
        self.start = None
        self.end = None
        self.result_label = None
        self.path_lines = []

        self.draw_cities()
        self.canvas.bind("<Button-1>", self.choose_city)

        bottom_frame = tk.Frame(root)
        bottom_frame.pack(pady=10)

        find_button = tk.Button(bottom_frame, text="Find Shortest Path", command=self.find_path,
                                font=('Arial', 11, 'bold'), bg='lightblue', width=20, height=2)
        find_button.pack(side=tk.LEFT, padx=10)

        reset_button = tk.Button(bottom_frame, text="Reset", command=self.reset_selection,
                                 font=('Arial', 11, 'bold'), bg='lightcoral', width=15, height=2)
        reset_button.pack(side=tk.LEFT)

        self.result_label = tk.Label(root, text="", font=('Arial', 12, 'bold'), fg='green')
        self.result_label.pack(pady=5)

    def draw_cities(self):
        for city, (x, y) in cities.items():
            self.canvas.create_oval(x - 10, y - 10, x + 10, y + 10, fill='red')
            self.canvas.create_text(x, y - 15, text=city, font=('Arial', 9, 'bold'))
        for city, conns in roads.items():
            for dest in conns:
                x1, y1 = cities[city]
                x2, y2 = cities[dest]
                self.canvas.create_line(x1, y1, x2, y2)

    def choose_city(self, event):
        for city, (x, y) in cities.items():
            if abs(event.x - x) <= 10 and abs(event.y - y) <= 10:
                if not self.start:
                    self.start = city
                    self.canvas.create_text(x, y + 20, text='Start', fill='green')
                elif not self.end and city != self.start:
                    self.end = city
                    self.canvas.create_text(x, y + 20, text='End', fill='blue')
                return

    def heuristic(self, c1, c2):
        x1, y1 = cities[c1]
        x2, y2 = cities[c2]
        return math.hypot(x2 - x1, y2 - y1)

    def find_path(self):
        if not self.start or not self.end:
            return
        pq = PriorityQueue()
        pq.put((0, self.start))
        came = {}
        cost = {city: float('inf') for city in cities}
        cost[self.start] = 0
        while not pq.empty():
            _, current = pq.get()
            if current == self.end:
                self.draw_path(came)
                self.result_label.config(text=f"Total Cost from {self.start} to {self.end}: {cost[self.end]} units")
                return
            for next_city in roads.get(current, {}):
                new_cost = cost[current] + roads[current][next_city]
                if new_cost < cost[next_city]:
                    came[next_city] = current
                    cost[next_city] = new_cost
                    priority = new_cost + self.heuristic(next_city, self.end)
                    pq.put((priority, next_city))

    def draw_path(self, came):
        city = self.end
        while city in came:
            prev = came[city]
            x1, y1 = cities[city]
            x2, y2 = cities[prev]
            line = self.canvas.create_line(x1, y1, x2, y2, width=4, fill='blue')
            self.canvas.update()
            time.sleep(0.3)  # simple animation effect
            self.path_lines.append(line)
            city = prev

    def reset_selection(self):
        self.start = None
        self.end = None
        self.result_label.config(text="")
        for line in self.path_lines:
            self.canvas.delete(line)
        self.path_lines.clear()
        self.canvas.delete("all")
        self.draw_cities()

# Run the app
win = tk.Tk()
win.title("City Map Shortest Route (A*)")
win.resizable(False, False)
app = CityMap(win)
win.mainloop()
