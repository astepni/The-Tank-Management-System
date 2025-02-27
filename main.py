from datetime import datetime

class Tank:
    all_tanks = []  # Lista wszystkich zbiorników

    def __init__(self, name, capacity):
        self.name = name
        self.capacity = capacity  # Pojemność zbiornika
        self.current_volume = 0  # Aktualny poziom wody
        self.operations_history = []  # Historia operacji
        Tank.all_tanks.append(self)

    # Operacja nalewania wody
    def pour_water(self, volume):
        available_space = self.capacity - self.current_volume
        if volume <= available_space:
            self.current_volume += volume
            self._register_operation("pour_water", volume, True)
        else:
            self.current_volume = self.capacity  # Wypełniamy zbiornik do pełna
            self._register_operation("pour_water", volume, False)

    # Operacja odlewania wody
    def pour_out_water(self, volume):
        if self.current_volume >= volume:
            self.current_volume -= volume
            self._register_operation("pour_out_water", volume, True)
        else:
            self._register_operation("pour_out_water", volume, False)

    # Operacja przelewania wody między zbiornikami
    def transfer_water(self, from_tank, volume):
        if from_tank.current_volume >= volume:
            available_space = self.capacity - self.current_volume
            actual_volume = min(volume, available_space)  # Przelewamy tylko tyle, ile się zmieści
            from_tank.pour_out_water(actual_volume)  # Odlewamy wodę ze zbiornika źródłowego
            self.pour_water(actual_volume)          # Nalewamy wodę do zbiornika docelowego
            self._register_operation("transfer_water", actual_volume, True)
        else:
            # Jeśli operacja jest niemożliwa (brak wystarczającej ilości wody), rejestrujemy jako nieudaną
            self._register_operation("transfer_water", volume, False)

    # Rejestracja operacji
    def _register_operation(self, operation_name, volume, success):
        self.operations_history.append({
            "date": datetime.now(),
            "operation": operation_name,
            "tank": self.name,
            "volume": volume,
            "success": success
        })

    # Metoda znajdująca zbiornik z największą ilością wody
    @classmethod
    def find_tank_with_most_water(cls):
        return max(cls.all_tanks, key=lambda tank: tank.current_volume)

    # Metoda znajdująca najbardziej zapełniony zbiornik
    @classmethod
    def find_most_filled_tank(cls):
        return max(cls.all_tanks, key=lambda tank: tank.current_volume / tank.capacity)

    # Metoda znajdująca wszystkie puste zbiorniki
    @classmethod
    def find_empty_tanks(cls):
        return [tank for tank in cls.all_tanks if tank.current_volume == 0]

    # Metoda znajdująca zbiornik z największą liczbą nieudanych operacji
    @classmethod
    def find_tank_with_most_failed_operations(cls):
        return max(cls.all_tanks, key=lambda tank: sum(1 for op in tank.operations_history if not op["success"]))

    # Metoda znajdująca zbiornik z największą liczbą operacji danego typu
    @classmethod
    def find_tank_with_most_operations_of_type(cls, operation_type):
        return max(cls.all_tanks, key=lambda tank: sum(1 for op in tank.operations_history if op["operation"] == operation_type))

    # Metoda sprawdzająca spójność stanu wody z historią operacji
    def check_state(self):
        calculated_volume = 0
        for operation in self.operations_history:
            if operation["success"]:
                if operation["operation"] == "pour_water":
                    calculated_volume += operation["volume"]
                elif operation["operation"] == "pour_out_water":
                    calculated_volume -= operation["volume"]
                elif operation["operation"] == "transfer_water":
                    if operation["tank"] == self.name:
                        calculated_volume += operation["volume"]
                    else:
                        calculated_volume -= operation["volume"]
        return calculated_volume == self.current_volume
