from datetime import datetime
from app.services.database import get_collection

deals_collection = get_collection('deals')

class Deal:
    def __init__(self, sku, start_time, promo_codes, price):
        self.sku = sku
        self.start_time = start_time
        self.promo_codes = promo_codes
        self.price = price
        self.created_at = datetime.now(datetime.UTC)

    def save(self):
        deal_data = {
            '_id': self.sku,
            'start_time': self.start_time,
            'promo_codes': list(self.promo_codes),
            'price': self.price,
            'created_at': self.created_at
        }
        return deals_collection.insert_one(deal_data)

    @staticmethod
    def insert_deals(deals):
        deals_data = []
        for deal_id, deal_info in deals.items():
            deals_data.append({
                '_id': deal_id,
                'start_time': deal_info['start_time'],
                'promo_codes': list(deal_info['promo_codes']),
                'price': deal_info['price'],
                'created_at': datetime.now(datetime.UTC)
            })
        return deals_collection.insert_many(deals_data)