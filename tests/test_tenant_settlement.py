from src.models import Parameters, TenantSettlement
from src.manager import Manager


def test_create_tenant_settlement_with_multiple_tenants():
    """
    Test sprawdza poprawność udziału najemców w kosztach, gdy mieszkanie ma 2 lub więcej najemców.
    Zawiera przynajmniej 10 asercji.
    """
    parameters = Parameters()
    manager = Manager(parameters)
    
    # apart-polanka ma 3 najemców, rachunki w styczniu 2025: 910 PLN
    # Najemca 1: czynsz 1500, powierzchnia pokoju: 20m2
    # Najemca 2: czynsz 1400, powierzchnia pokoju: 18m2  
    # Najemca 3: czynsz 1300, powierzchnia pokoju: 15m2
    # Suma czynszów: 4200 PLN
    # Udział najemcy 1 w kosztach: (1500 / 4200) * 910 = 325 PLN
    
    result = manager.create_tenant_settlement('tenant-1', 2025, 1)
    
    assert result is not None
    
    assert isinstance(result, TenantSettlement)
    
    assert result.tenant == 'tenant-1'
    
    assert result.apartment_settlement == 'apart-polanka'
    
    assert result.year == 2025
    
    assert result.month == 1
    
    assert result.rent_pln == 1500.0
    
    assert result.bills_pln == 325.0
    
    assert result.total_due_pln == 1175.0
    
    assert result.balance_pln == 1325.0
    
    assert result.bills_pln > 0
    
    assert result.rent_pln > result.bills_pln
    
    assert result.total_due_pln == result.rent_pln - result.bills_pln


def test_create_tenant_settlement_single_tenant():
    """Test sprawdza poprawność udziału najemców w kosztach, gdy mieszkanie ma tylko 1 najemcę"""
    parameters = Parameters()
    manager = Manager(parameters)
    
    manager.tenants = {'tenant-1': manager.tenants['tenant-1']}
    
    result = manager.create_tenant_settlement('tenant-1', 2025, 1)
    
    assert result is not None
    assert result.bills_pln == 910.0
    assert result.rent_pln == 1500.0
    assert result.total_due_pln == 1500.0 - 910.0


def test_create_tenant_settlement_no_tenants():
    """Test sprawdza poprawność gdy mieszkanie nie ma żadnych najemców (rozliczenia najemców nie powinny być tworzone)"""
    parameters = Parameters()
    manager = Manager(parameters)
    
    manager.tenants.clear()
    
    result = manager.create_tenant_settlement('tenant-1', 2025, 1)
    
    assert result is None
