from src.models import Apartment, ApartmentSettlement, Bill, Parameters, Tenant, TenantSettlement, Transfer


class Manager:
    def __init__(self, parameters: Parameters):
        self.parameters = parameters 

        self.apartments = {}
        self.tenants = {}
        self.transfers = []
        self.bills = []
       
        self.load_data()

    def load_data(self):
        self.apartments = Apartment.from_json_file(self.parameters.apartments_json_path)
        self.tenants = Tenant.from_json_file(self.parameters.tenants_json_path)
        self.transfers = Transfer.from_json_file(self.parameters.transfers_json_path)
        self.bills = Bill.from_json_file(self.parameters.bills_json_path)

    def check_tenants_apartment_keys(self) -> bool:
        for tenant in self.tenants.values():
            if tenant.apartment not in self.apartments:
                return False
        return True

    def get_apartment_costs(
        self, apartment_key: str, year: int | None = None, month: int | None = None
    ) -> float | None:
        if apartment_key not in self.apartments:
            return None

        if month is not None and not (1 <= month <= 12):
            return None

        return sum(
            bill.amount_pln
            for bill in self.bills
            if bill.apartment == apartment_key
            and (year is None or bill.settlement_year == year)
            and (month is None or bill.settlement_month == month)
        )


    def create_apartment_settlement(self, apartment_key: str, year: int, month: int) -> ApartmentSettlement | None:
        if apartment_key not in self.apartments:
            return None
        
        total_rent_pln = sum(
            tenant.rent_pln 
            for tenant in self.tenants.values() 
            if tenant.apartment == apartment_key
        )
        
        total_bills_pln = self.get_apartment_costs(apartment_key, year, month) or 0.0
        
        total_due_pln = total_rent_pln - total_bills_pln
        
        return ApartmentSettlement(
            apartment=apartment_key,
            month=month,
            year=year,
            total_rent_pln=total_rent_pln,
            total_bills_pln=total_bills_pln,
            total_due_pln=total_due_pln
        )

    def create_tenant_settlement(self, tenant_key: str, year: int, month: int) -> TenantSettlement | None:
        if tenant_key not in self.tenants:
            return None
        
        tenant = self.tenants[tenant_key]
        apartment_key = tenant.apartment
        
        total_rent_pln = sum(
            t.rent_pln 
            for t in self.tenants.values() 
            if t.apartment == apartment_key
        )
        
        total_bills_pln = self.get_apartment_costs(apartment_key, year, month) or 0.0
        
        bills_pln = (tenant.rent_pln / total_rent_pln) * total_bills_pln if total_rent_pln > 0 else 0.0
        
        total_due_pln = tenant.rent_pln - bills_pln
        
        transfers_sum = sum(
            transfer.amount_pln
            for transfer in self.transfers
            if transfer.tenant == tenant_key
            and transfer.settlement_year == year
            and transfer.settlement_month == month
        )
        
        balance_pln = transfers_sum - total_due_pln
        
        return TenantSettlement(
            tenant=tenant_key,
            apartment_settlement=apartment_key,
            month=month,
            year=year,
            rent_pln=tenant.rent_pln,
            bills_pln=bills_pln,
            total_due_pln=total_due_pln,
            balance_pln=balance_pln
        )