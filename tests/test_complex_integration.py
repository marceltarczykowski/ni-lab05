from src.models import Parameters
from src.manager import Manager


def test_get_apartment_costs_no_apartment():
    """Test sprawdza czy dla nieistniejącego mieszkania zwracane jest 0.0"""
    parameters = Parameters()
    manager = Manager(parameters)
    
    result = manager.get_apartment_costs('non-existent-apartment', 2024, 3)
    assert result == 0.0


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
