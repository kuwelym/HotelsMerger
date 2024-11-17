from typing import List
from models import Hotel
from suppliers import Acme, Patagonia, Paperflies
import json

class HotelsService:
    def __init__(self):
        self.hotels = {}

    def merge_and_save(self, supplier_data: List[Hotel]):
        for hotel in supplier_data:
            if hotel.id not in self.hotels:
                self.hotels[hotel.id] = hotel
            else:
                self.hotels[hotel.id].merge(hotel)

    def find(self, hotel_ids: List[str], destination_ids: List[str]) -> List[Hotel]:
        return [
            hotel for hotel in self.hotels.values()
            if (not hotel_ids or hotel.id in hotel_ids) and (not destination_ids or hotel.destination_id in destination_ids)
        ]

def fetch_hotels(hotel_ids: List[str], destination_ids: List[str]):
    suppliers = [Acme(), Patagonia(), Paperflies()]

    # Fetch data from all suppliers
    all_supplier_data = []
    for supplier in suppliers:
        all_supplier_data.extend(supplier.fetch())

    # Merge all data and save it
    svc = HotelsService()
    svc.merge_and_save(all_supplier_data)

    # Fetch filtered data
    filtered = svc.find(hotel_ids, destination_ids)

    # Return as JSON
    return json.dumps([hotel.__dict__ for hotel in filtered], default = lambda o: o.__dict__, indent = 2)
