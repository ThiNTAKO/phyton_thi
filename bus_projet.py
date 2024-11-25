import tkinter as tk
from tkinter import messagebox

class Bus:
    def __init__(self, bus_id, capacity, status="En service"):
        self.bus_id = bus_id
        self.capacity = capacity
        self.status = status
        self.current_passengers = 0
        self.route = None

    def assign_route(self, route):
        self.route = route
        print(f"Bus {self.bus_id} assigné à la ligne {route.line_name}.")

    def board_passengers(self, num_passengers):
        if self.current_passengers + num_passengers <= self.capacity:
            self.current_passengers += num_passengers
            print(f"{num_passengers} passagers montés dans le bus {self.bus_id}.")
        else:
            print(f"Bus {self.bus_id} plein ! Seulement {self.capacity - self.current_passengers} places disponibles.")

    def __str__(self):
        return f"Bus {self.bus_id} - {self.status} - {self.current_passengers}/{self.capacity} passagers."


class Route:
    def __init__(self, line_name, stops):
        self.line_name = line_name
        self.stops = stops

    def __str__(self):
        return f"Ligne {self.line_name} : {', '.join(self.stops)}."


class Driver:
    def __init__(self, name, driver_id):
        self.name = name
        self.driver_id = driver_id
        self.assigned_bus = None

    def assign_bus(self, bus):
        self.assigned_bus = bus
        print(f"Conducteur {self.name} assigné au bus {bus.bus_id}.")

    def __str__(self):
        return f"Conducteur {self.name} - Bus assigné : {self.assigned_bus.bus_id if self.assigned_bus else 'Aucun'}."


class TransportSystem:
    def __init__(self):
        self.buses = []
        self.routes = []
        self.drivers = []

    def add_bus(self, bus):
        self.buses.append(bus)
        print(f"Bus {bus.bus_id} ajouté au système.")

    def add_route(self, route):
        self.routes.append(route)
        print(f"Ligne {route.line_name} ajoutée au système.")

    def add_driver(self, driver):
        self.drivers.append(driver)
        print(f"Conducteur {driver.name} ajouté au système.")

    def assign_driver_to_bus(self, driver_id, bus_id):
        driver = next((d for d in self.drivers if d.driver_id == driver_id), None)
        bus = next((b for b in self.buses if b.bus_id == bus_id), None)
        if driver and bus:
            driver.assign_bus(bus)
        else:
            print("Erreur : Conducteur ou bus non trouvé.")

    def __str__(self):
        return f"Transport System : {len(self.buses)} bus, {len(self.routes)} routes, {len(self.drivers)} conducteurs."


# Fonction d'interface pour ajouter un bus
def add_bus_interface():
    bus_id = bus_id_entry.get()
    capacity = int(capacity_entry.get())
    bus = Bus(bus_id, capacity)
    system.add_bus(bus)
    messagebox.showinfo("Bus ajouté", f"Bus {bus_id} ajouté avec une capacité de {capacity} passagers.")


# Fonction d'interface pour ajouter un conducteur
def add_driver_interface():
    name = driver_name_entry.get()
    driver_id = int(driver_id_entry.get())
    driver = Driver(name, driver_id)
    system.add_driver(driver)
    messagebox.showinfo("Conducteur ajouté", f"Conducteur {name} ajouté avec l'ID {driver_id}.")


# Fonction pour assigner un conducteur à un bus
def assign_driver_to_bus_interface():
    driver_id = int(assign_driver_id_entry.get())
    bus_id = int(assign_bus_id_entry.get())
    system.assign_driver_to_bus(driver_id, bus_id)
    messagebox.showinfo("Assignation réussie", f"Conducteur {driver_id} assigné au bus {bus_id}.")


# Fonction pour simuler la montée de passagers
def board_passengers_interface():
    bus_id = int(board_bus_id_entry.get())
    num_passengers = int(num_passengers_entry.get())
    bus = next((b for b in system.buses if b.bus_id == bus_id), None)
    if bus:
        bus.board_passengers(num_passengers)
        messagebox.showinfo("Passagers montés", f"{num_passengers} passagers montés dans le bus {bus_id}.")
    else:
        messagebox.showerror("Erreur", "Bus non trouvé.")


# Création du système de transport
system = TransportSystem()

# Interface graphique avec Tkinter
root = tk.Tk()
root.title("Système de Gestion de Bus")

# Ajout des bus
tk.Label(root, text="ID Bus :").grid(row=0, column=0)
bus_id_entry = tk.Entry(root)
bus_id_entry.grid(row=0, column=1)

tk.Label(root, text="Capacité :").grid(row=1, column=0)
capacity_entry = tk.Entry(root)
capacity_entry.grid(row=1, column=1)

add_bus_button = tk.Button(root, text="Ajouter un Bus", command=add_bus_interface)
add_bus_button.grid(row=2, column=0, columnspan=2)

# Ajout des conducteurs
tk.Label(root, text="Nom Conducteur :").grid(row=3, column=0)
driver_name_entry = tk.Entry(root)
driver_name_entry.grid(row=3, column=1)

tk.Label(root, text="ID Conducteur :").grid(row=4, column=0)
driver_id_entry = tk.Entry(root)
driver_id_entry.grid(row=4, column=1)

add_driver_button = tk.Button(root, text="Ajouter un Conducteur", command=add_driver_interface)
add_driver_button.grid(row=5, column=0, columnspan=2)

# Assignation conducteur à bus
tk.Label(root, text="ID Conducteur :").grid(row=6, column=0)
assign_driver_id_entry = tk.Entry(root)
assign_driver_id_entry.grid(row=6, column=1)

tk.Label(root, text="ID Bus :").grid(row=7, column=0)
assign_bus_id_entry = tk.Entry(root)
assign_bus_id_entry.grid(row=7, column=1)

assign_button = tk.Button(root, text="Assigner Conducteur au Bus", command=assign_driver_to_bus_interface)
assign_button.grid(row=8, column=0, columnspan=2)

# Simulation de la montée de passagers
tk.Label(root, text="ID Bus :").grid(row=9, column=0)
board_bus_id_entry = tk.Entry(root)
board_bus_id_entry.grid(row=9, column=1)

tk.Label(root, text="Nombre de passagers :").grid(row=10, column=0)
num_passengers_entry = tk.Entry(root)
num_passengers_entry.grid(row=10, column=1)

board_passengers_button = tk.Button(root, text="Monter des Passagers", command=board_passengers_interface)
board_passengers_button.grid(row=11, column=0, columnspan=2)

# Lancer l'interface
root.mainloop()
