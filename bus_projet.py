#Code Python : Modèle de gestion de bus

class Bus:
    def _init_(self, bus_id, capacity, status="En service"):
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
            print(f"Bus {self.bus_id} plein !")

    def _str_(self):
        return f"Bus {self.bus_id} - {self.status} - {self.current_passengers}/{self.capacity} passagers."


class Route:
    def _init_(self, line_name, stops):
        self.line_name = line_name
        self.stops = stops  # Liste des arrêts de bus

    def _str_(self):
        return f"Ligne {self.line_name} : {', '.join(self.stops)}."


class Driver:
    def _init_(self, name, driver_id):
        self.name = name
        self.driver_id = driver_id
        self.assigned_bus = None

    def assign_bus(self, bus):
        self.assigned_bus = bus
        print(f"Conducteur {self.name} assigné au bus {bus.bus_id}.")

    def _str_(self):
        return f"Conducteur {self.name} - Bus assigné : {self.assigned_bus.bus_id if self.assigned_bus else 'Aucun'}."


class TransportSystem:
    def _init_(self):
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

    def _str_(self):
        return f"Transport System : {len(self.buses)} bus, {len(self.routes)} routes, {len(self.drivers)} conducteurs."


# Exemple d'utilisation
if __name__ == "_main_":
    # Création du système
    system = TransportSystem()

    # Ajout des lignes
    route1 = Route("Ligne 1", ["Arrêt A", "Arrêt B", "Arrêt C"])
    system.add_route(route1)

    # Ajout des bus
    bus1 = Bus(bus_id=101, capacity=50)
    bus2 = Bus(bus_id=102, capacity=30)
    system.add_bus(bus1)
    system.add_bus(bus2)

    # Ajout des conducteurs
    driver1 = Driver(name="Alice", driver_id=1)
    driver2 = Driver(name="Bob", driver_id=2)
    system.add_driver(driver1)
    system.add_driver(driver2)

    # Assignation
    bus1.assign_route(route1)
    system.assign_driver_to_bus(driver_id=1, bus_id=101)

    # Simulation de montée de passagers
    bus1.board_passengers(20)
    bus1.board_passengers(35)

    # Affichage de l'état
    print(bus1)
    print(route1)
    print(driver1)
    print(system)