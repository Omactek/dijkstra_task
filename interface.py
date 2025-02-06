import tkinter as tk
from tkinter import ttk

class ShortestPathApp:
    def __init__(self, root, algorithm):
        self.algorithm = algorithm
        self.root = root
        self.root.title("Shortest Path Finder")

        # Dropdowns for city selection
        self.start_city = tk.StringVar()
        self.end_city = tk.StringVar()

        ttk.Label(root, text="Start City:").grid(row=0, column=0, padx=10, pady=5)
        self.start_dropdown = ttk.Combobox(root, textvariable=self.start_city)
        self.start_dropdown.grid(row=0, column=1, padx=10, pady=5)

        ttk.Label(root, text="End City:").grid(row=1, column=0, padx=10, pady=5)
        self.end_dropdown = ttk.Combobox(root, textvariable=self.end_city)
        self.end_dropdown.grid(row=1, column=1, padx=10, pady=5)

        # Checkboxes for optional calculations
        self.run_bellman_ford = tk.BooleanVar()
        self.run_mst = tk.BooleanVar()
        self.run_all_pairs = tk.BooleanVar()

        self.bellman_ford_checkbox = ttk.Checkbutton(root, text="Run Bellman-Ford", variable=self.run_bellman_ford)
        self.bellman_ford_checkbox.grid(row=2, column=0, columnspan=2, pady=5)

        self.mst_checkbox = ttk.Checkbutton(root, text="Run MST", variable=self.run_mst)
        self.mst_checkbox.grid(row=3, column=0, columnspan=2, pady=5)

        self.all_pairs_checkbox = ttk.Checkbutton(root, text="Run All Pairs Combinations", variable=self.run_all_pairs)
        self.all_pairs_checkbox.grid(row=4, column=0, columnspan=2, pady=5)

        # Calculate button
        self.calculate_button = ttk.Button(root, text="Calculate Path", command=self.calculate_path)
        self.calculate_button.grid(row=5, column=0, columnspan=2, pady=10)

        # Result display
        self.result_label = ttk.Label(root, text="", wraplength=400)
        self.result_label.grid(row=6, column=0, columnspan=2, pady=10)

        self.populate_dropdowns()

    def populate_dropdowns(self):
        cities = list(self.algorithm.graph.cities.values())
        sorted_cities = sorted(cities)
        self.start_dropdown["values"] = sorted_cities
        self.end_dropdown["values"] = sorted_cities

    def calculate_path(self):
        start_name = self.start_city.get()
        end_name = self.end_city.get()

        if not start_name or not end_name:
            self.result_label.config(text="Please select both start and end cities.")
            return

        start_id = next((id for id, name in self.algorithm.graph.cities.items() if name == start_name), None)
        end_id = next((id for id, name in self.algorithm.graph.cities.items() if name == end_name), None)

        if start_id is None or end_id is None:
            self.result_label.config(text="Invalid city selection.")
            return
        
        self.result_label.config(text="Counting... Please wait.")
        self.root.update_idletasks()

        distance, parents = self.algorithm.dijkstra(start_id, end_id, mode="basic")
        path = self.algorithm.reconstruct_path(start_id, end_id, parents)
        time, parents_time = self.algorithm.dijkstra(start_id, end_id, mode="advanced")
        path_time = self.algorithm.reconstruct_path(start_id, end_id, parents_time)

        whole_hours = int(time)
        minutes = int((time - whole_hours) * 60)

        results = [
            f"Result for route between {start_name} and {end_name}:",
            f"Shortest distance (Dijkstra): {distance:.2f} km",
            f"Shortest Path: {path}",
            f"Fastest estimated travel time (Dijkstra): {whole_hours}:{minutes} h",
            f"Fastest Path: {path_time}"
        ]

        # Conditional calculations based on checkboxes
        if self.run_all_pairs.get():
            combinations_file = "combinations.json"
            self.algorithm.calculate_combinations(combinations_file, limit=10, mode="advanced")
            results.append(f"Combinations saved to: {combinations_file}")

        if self.run_bellman_ford.get():
            bell_dists, bell_parents = self.algorithm.bellman_ford(start_id, mode="basic")
            bell_distance = bell_dists[end_id]
            bell_path = self.algorithm.reconstruct_path(start_id, end_id, bell_parents)
            results.append(f"Shortest Distance (Bellman-Ford): {bell_distance:.2f} km")
            results.append(f"Path (Bellman-Ford): {bell_path}")

        if self.run_mst.get():
            mst = self.algorithm.kruskal(mode="basic")
            results.append(f"Minimum Spanning Tree: {mst}")

        self.result_label.config(text="\n".join(results))
