from datetime import datetime, timezone
from app.services.database import get_collection

collection = get_collection('promos')

class Promo:
    def __init__(self, promo_id, kind, value, expired):
        self.promo_id = promo_id
        self.kind = kind
        self.value = value
        self.expired = expired

    def save(self):
        collection.insert_one({
            '_id': self.promo_id,
            'kind': self.kind,
            'value': self.value,
            'expired': self.expired
        })

    @staticmethod
    def insert_promos(promos):
        promos_data = []
        for promo_id, promo_info in promos.items():
            promos_data.append({
                '_id': promo_id,
                'kind': promo_info['kind'],
                'value': promo_info['value'],
                'expired': promo_info['expired']
            })
        return collection.insert_many(promos_data)
    
    @staticmethod
    def all():
        return collection.find()
    
    @staticmethod
    def find(promo_id):
        return collection.find_one({'_id': promo_id})
    
    @staticmethod
    def destroy(promo_id):
        return collection.delete_one({'_id': promo_id})
    
    @staticmethod
    def valid():
        return collection.find({'expired': False})