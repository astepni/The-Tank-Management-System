import pytest
from main import Tank

@pytest.fixture
def setup_tanks():
    Tank.all_tanks = []  # Resetujemy listę przed każdym testem
    tank1 = Tank("Tank1", 100)
    tank2 = Tank("Tank2", 200)
    tank3 = Tank("Tank3", 150)
    return tank1, tank2, tank3

def test_init(setup_tanks):
    tank1, _, _ = setup_tanks
    assert tank1.name == "Tank1"
    assert tank1.capacity == 100
    assert tank1.current_volume == 0

def test_pour_water(setup_tanks):
    tank1, _, _ = setup_tanks
    tank1.pour_water(50)
    assert tank1.current_volume == 50

def test_pour_out_water(setup_tanks):
    tank1, _, _ = setup_tanks
    tank1.pour_water(80)
    tank1.pour_out_water(30)
    assert tank1.current_volume == 50

def test_transfer_water(setup_tanks):
    tank1, tank2, _ = setup_tanks

    # Nalanie wody do Tank2 (zbiornik źródłowy)
    tank2.pour_water(100)

    # Transfer 50 jednostek z Tank2 do Tank1 (zbiornik docelowy)
    tank1.transfer_water(tank2, 50)

    # Sprawdzamy poziomy wody po transferze
    assert tank1.current_volume == 50  # Tank1 powinien mieć 50 jednostek po transferze
    assert tank2.current_volume == 50  # Tank2 powinien mieć 50 jednostek po transferze

def test_find_empty_tanks(setup_tanks):
    _, _, _ = setup_tanks
    empty_tanks = Tank.find_empty_tanks()
    
    assert len(empty_tanks) == len(Tank.all_tanks)  # Wszystkie są puste na początku

def test_check_state(setup_tanks):
    tank1, _, _ = setup_tanks
    
    # Nalewanie i odlewanie wody - poprawny stan końcowy powinien być zgodny z historią operacji.
    tank1.pour_water(50)
    
    assert tank1.check_state() is True
    

