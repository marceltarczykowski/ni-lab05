from src.models import Parameters, ApartmentSettlement
from src.manager import Manager


def test_create_apartment_settlement_nonexistent_apartment():
    """Test sprawdza czy dla nieistniejącego mieszkania zwracane jest None"""
    parameters = Parameters()
    manager = Manager(parameters)
    
    result = manager.create_apartment_settlement('non-existent-apartment', 2025, 1)
    assert result is None


def test_create_apartment_settlement_no_bills():
    """Test sprawdza poprawność bilansu dla mieszkania, które nie ma rachunków w danym miesiącu"""
    parameters = Parameters()
    manager = Manager(parameters)
    
    result = manager.create_apartment_settlement('apart-polanka', 2024, 12)
    
    assert result is not None
    assert isinstance(result, ApartmentSettlement)
    assert result.apartment == 'apart-polanka'
    assert result.year == 2024
    assert result.month == 12
    assert result.total_rent_pln == 4200.0
    assert result.total_bills_pln == 0.0
    assert result.total_due_pln == 4200.0


def test_create_apartment_settlement_with_bills():
    """
    Test sprawdza poprawność bilansu dla mieszkania, które ma rachunki.
    """
    parameters = Parameters()
    manager = Manager(parameters)
    
    result = manager.create_apartment_settlement('apart-polanka', 2025, 1)
    
    assert result is not None
    
    assert isinstance(result, ApartmentSettlement)
    
    assert result.apartment == 'apart-polanka'
    
    assert result.year == 2025
    
    assert result.month == 1
    
    assert result.total_rent_pln == 4200.0
    
    assert result.total_bills_pln == 910.0
    
    assert result.total_due_pln == 3290.0
    
    assert result.total_rent_pln > result.total_bills_pln
    
    assert result.total_due_pln == result.total_rent_pln - result.total_bills_pln
    
    assert isinstance(result.total_rent_pln, float)
    
    assert result.total_bills_pln > 0
    
    assert result.total_due_pln > 0
