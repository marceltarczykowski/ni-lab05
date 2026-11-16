from src.manager import Manager
from src.models import Parameters
from src.models import Bill


def test_apartment_costs_with_optional_parameters():
    manager = Manager(Parameters())
    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2025-03-15',
        settlement_year=2025,
        settlement_month=2,
        amount_pln=1250.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-03-15',
        settlement_year=2024,
        settlement_month=2,
        amount_pln=1150.0,
        type='rent'
    ))

    manager.bills.append(Bill(
        apartment='apart-polanka',
        date_due='2024-02-02',
        settlement_year=2024,
        settlement_month=1,
        amount_pln=222.0,
        type='electricity'
    ))

    costs = manager.get_apartment_costs('apartment-1', 2024, 1)
    assert costs is None

    costs = manager.get_apartment_costs('apart-polanka', 2024, 3)
    assert costs == 0.0

    costs = manager.get_apartment_costs('apart-polanka', 2024, 1)
    assert costs == 222.0

    costs = manager.get_apartment_costs('apart-polanka', 2025, 1)
    assert costs == 910.0
    
    costs = manager.get_apartment_costs('apart-polanka', 2024)
    assert costs == 1372.0

    costs = manager.get_apartment_costs('apart-polanka')
    assert costs == 3532.0
    
def test_get_apartment_costs_no_apartment():
    """Test sprawdza czy dla nieistniejącego mieszkania zwracane jest 0.0"""
    parameters = Parameters()
    manager = Manager(parameters)
    
    result = manager.get_apartment_costs('non-existent-apartment', 2024, 3)
    assert result is None


def test_get_apartment_costs_no_bills_for_month():
    """Test sprawdza czy dla miesiąca bez rachunków zwracane jest None lub 0.0"""
    parameters = Parameters()
    manager = Manager(parameters)
    
    result = manager.get_apartment_costs('apart-polanka', 2024, 12)
    assert result is None or result == 0.0


def test_get_apartment_costs_year_matches_month_does_not():
    """Test sprawdza czy gdy rok się zgadza ale miesiąc nie, zwracany jest None lub wyjątek"""
    parameters = Parameters()
    manager = Manager(parameters)
    
    result = manager.get_apartment_costs('apart-polanka', 2025, 2)
    assert result is None or result == 0.0


def test_get_apartment_costs_with_bills():
    """
    Test sprawdza czy metoda poprawnie sumuje rachunki dla konkretnego miesiąca.
    Przykład asercji do napisania:
    assert manager.get_apartment_costs('A1', 2024, 3) == 450.0
    
    Test integracyjny - wynik zależy od poprawnego powiązania klucza apartment 
    z obiektów Bill i klucza w słowniku apartments.
    """
    parameters = Parameters()
    manager = Manager(parameters)
    

    result = manager.get_apartment_costs('apart-polanka', 2025, 1)
    
    assert result == 910.0, f"Expected 910.0 but got {result}"
    
    assert result > 760.0, "Total should be greater than rent bill alone"
    
    assert result > 0, "Total should be positive when bills exist"
    
    assert isinstance(result, float), "Result should be a float"

def test_get_apartment_costs_invalid_month():
    """Test sprawdza zachowanie metody dla nieprawidłowego numeru miesiąca (np. 13, 0, -1)."""
    parameters = Parameters()
    manager = Manager(parameters)

    assert manager.get_apartment_costs("apart-polanka", 2024, 13) is None
    assert manager.get_apartment_costs("apart-polanka", 2024, 0) is None
    assert manager.get_apartment_costs("apart-polanka", 2024, -1) is None