from datetime import datetime, timezone
from app.services.database import get_collection

deals_collection = get_collection('deals')

class Deal:
    def __init__(self, sku, start_time, promo_codes, price):
        #if start_time is a string, convert it to a datetime object
        if type(start_time) is str:
            start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
        self.sku = sku
        self.start_time = start_time
        self.promo_codes = promo_codes
        self.price = price
        self.created_at = datetime.now(timezone.utc)

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
            start_time = deal_info['start_time']
            if type(start_time) is str:
                start_time = datetime.fromisoformat(start_time.replace('Z', '+00:00'))
            deals_data.append({
                '_id': deal_id,
                'start_time': start_time,
                'promo_codes': list(deal_info['promo_codes']),
                'price': deal_info['price'],
                'created_at': datetime.now(timezone.utc)
            })
        return deals_collection.insert_many(deals_data)
    
    @staticmethod
    def all():
        return deals_collection.find()
    
    @staticmethod
    def find(sku):
        return deals_collection.find_one({'_id': sku})
    
    @staticmethod
    def destroy(sku):
        return deals_collection.delete_one({'_id': sku})
    
    # get all the deals starting on a specific day.
    # example: Deal.starting_on('2024-01-01')
    @staticmethod
    def starting_on(date):
        start_date = datetime.fromisoformat(date)
        end_date = start_date.replace(hour=23, minute=59, second=59)
        return deals_collection.find({'start_time': {'$gte': start_date, '$lte': end_date}})