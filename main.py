from flask import Flask
from app.api.routes import default_routes
import threading
import time
import requests
from datetime import datetime, time as dt_time
from datetime import timezone

db_hash = {}

def evalute_and_notifiy_promo(promo, asin):
    # if there is at least one promo_codes, calculate the actual price subratcting from price, all the discount present in promo codes if the kind is amount subtract it directly otherwhise calculate the amount based on base_price
    # ignore percent discount of 100
    discounted_price = promo['price']
    for promo_code in promo['promos']:
        if promo['promos'][promo_code]['kind'] == 'amount':
            discounted_price = discounted_price - promo['promos'][promo_code]['value']
        else:
            if promo['promos'][promo_code]['value'] < 100:
                discounted_price = discounted_price - (promo['base_price'] * promo['promos'][promo_code]['value'] / 100)
    # calculate the effective discount percentage between the price and the discounted price and print promo if it's greater than 30%
    discounted_price = round(discounted_price, 2)
    effective_discount = (promo['price'] - discounted_price) / promo['price'] * 100
    if effective_discount > 35:
        effective_discount = round(effective_discount, 2)
        url = "https://www.amazon.it/dp/" + asin
        print(str(promo) + " effective discount: " + str(effective_discount))
        # send telegram message with the promo using this endpoint include also the promos with kind and value
        promo_text = ""
        for promo_code in promo['promos']:
            promo_text += f"{promo_code} {promo['promos'][promo_code]['kind']} {promo['promos'][promo_code]['value']}\n"
        text = f"[{discounted_price} €]({url}) {effective_discount}%\n {promo_text}\n {url}"
        url = 'https://api.telegram.org/bot%s/sendMessage?chat_id=%s&parse_mode=markdown&text=%s' % ('1047409995:AAFLiq9WK5kbd-W34bFQ3HHPkrbE6aR08R8', '-1001328797925', text)
        requests.get(url)

def parse_promos(promo_json):
    promotions = promo_json['rankedPromotions']
    app.logger.info(len(promotions))
    for promotion in promotions:
        try:
            product = promotion['product']['entity']
            title = product['title']
            asin = product['asin']
            price = product['buyingOptions'][0]['price']['entity']['priceToPay']['moneyValueOrRange']['value']['amount']
            base_price = product['buyingOptions'][0]['price']['entity']['basisPrice']['moneyValueOrRange']['value']['amount']
            promo_codes = product['buyingOptions'][0]['promotionsUnified']['entity']['displayablePromotions']
            start_time = product['buyingOptions'][0]['dealDetails']['entity']['startTime']
            promo_hash = {}
            for promo_code in promo_codes:
                promo_id = promo_code['unifiedId'].split('/')[-1]
                if 'combinedSavings' in promo_code:
                    combined_savings = promo_code['combinedSavings']
                    # if combined saving has key percentageBasedSavings
                    if 'percentageBasedSavings' in combined_savings:
                        promo_hash[promo_id] = {'kind':'percentage', 'value': float(combined_savings['percentageBasedSavings'])}
                    else:
                        promo_hash[promo_id] = {'kind':'amount', 'value': float(combined_savings['savingsAmount']['amount'])}
            
            if asin not in db_hash:
                db_hash[asin] = {'price':float(price),'base_price': float(base_price), 'start_time':start_time, 'promos': promo_hash}
                evalute_and_notifiy_promo(db_hash[asin], asin)
                print("sku: " + asin + " price: " + price + " base price: " + base_price + " promo_codes: " + str(promo_hash) + " start_time: " + start_time)  
        except Exception as e:
            print("ex")
            continue  

def get_new_deals():
    old_burp0_url = "https://data.amazon.it:443/api/marketplaces/APJ6JRA9NG5V4/promotions?pageSize=300&startIndex=0&calculateRefinements=true&_enableNestedRefs=true&rankingContext=%7B%22pageTypeId%22%3A%22deals%22%2C%22rankGroup%22%3A%22PARENT_ASIN_RANKING%22%7D&filters=%7B%22includedDepartments%22%3A%5B%5D%2C%22excludedDepartments%22%3A%5B%5D%2C%22includedTags%22%3A%5B%5D%2C%22excludedTags%22%3A%5B%22restrictedcontent%22%2C%22Restrictedcontent%22%2C%22restrictedContent%22%2C%22RestrictedContent%22%2C%22RESTRICTEDCONTENT%22%2C%22wrong%22%2C%22OIH%22%2C%22itoutlet%22%2C%22contentOnlyOrSlappedDeal%22%2C%22noprime%22%2C%22GS_DEAL%22%2C%22StudentDeal%22%5D%2C%22promotionTypes%22%3A%5B%22LIGHTNING_DEAL%22%5D%2C%22accessTypes%22%3A%5B%5D%7D&sortOrder=DEFAULT&pinnedPromotionGroups=%5B%5B%22B09F7RS7LC%22%5D%2C%5B%22B08F6S99YB%22%5D%5D"
    burp0_url = "https://data.amazon.it:443/api/marketplaces/APJ6JRA9NG5V4/promotions?pageSize=10000&startIndex=0&calculateRefinements=true&_enableNestedRefs=true&rankingContext=%7B%22pageTypeId%22%3A%22deals%22%2C%22rankGroup%22%3A%22PARENT_ASIN_RANKING%22%7D&filters=%7B%22includedDepartments%22%3A%5B%5D%2C%22excludedDepartments%22%3A%5B%5D%2C%22includedTags%22%3A%5B%5D%2C%22excludedTags%22%3A%5B%22restrictedcontent%22%2C%22contentOnlyOrSlappedDeal%22%2C%22noprime%22%2C%22GS_DEAL%22%2C%22StudentDeal%22%2C%22wrong%22%2C%22OIH%22%5D%2C%22promotionTypes%22%3A%5B%22TOP_DEAL%22%2C%22LIGHTNING_DEAL%22%2C%22BEST_DEAL%22%5D%2C%22accessTypes%22%3A%5B%5D%7D&sortOrder=DEFAULT&pinnedPromotionGroups=%5B%5B%22B09F7RS7LC%22%5D%2C%5B%22B08F6S99YB%22%5D%5D"
    burp0_cookies = {"session-id": "260-5599670-2998421", "session-id-time": "2082787201l", "i18n-prefs": "EUR", "ubid-acbit": "257-3149305-1960132", "session-token": "KftvlvIghKdnw6bCWFsGcOk2UczlSnoRZv3YoL8nfy+bJk7dxPA1RTjnVToPRfB9km+NYYP8zb96a4pwm7XI0tsziyNVi5oHabJZm5F6f6ZMHF3N2qSldQ/bT5NBKXFqxC4zarLNk0oA2RWGDLdpmivo32QHldtwsxT0Ky02DOO2mVnTid9rKsTqKj8opirpyXD4V5xOXXDN8frVEvzBxkRa5T/kJGSL7qFQe+y95/hOGqETjQfW0T5nx8VeuDpfgEW/ACZJeEiUOjkr7xjn6A49GPxuaZViXO4vPdkSuBiycw5jAk8AZBbtgx3abaFUMhPqPBXJ3xzWYNGl4jE6kblP10jw6c7I"}
    burp0_headers = {"Sec-Ch-Ua": "\"Not-A.Brand\";v=\"99\", \"Chromium\";v=\"124\"", "X-Api-Csrf-Token": "1@g4kNZYlro6YWhw7TCas7n002QM6BK2uGUJDN9kcgXjPuAAAAAQAAAABmRgcacmF3AAAAAGfA1H5nd8xGEcC33NuKVw==@RQ2CWZ", "X-Cc-Currency-Of-Preference": "EUR", "Accept-Language": "it-IT", "Sec-Ch-Ua-Mobile": "?0", "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.118 Safari/537.36", "Content-Type": "application/json", "Accept": "application/vnd.com.amazon.api+json; type=\"promotions.search.result/v1\"; expand=\"rankedPromotions[].product(product/v2).title(product.offer.title/v1),rankedPromotions[].product(product/v2).links(product.links/v2),rankedPromotions[].product(product/v2).energyEfficiency(product.energy-efficiency/v2),rankedPromotions[].product(product/v2).buyingOptions[].dealBadge(product.deal-badge/v1),rankedPromotions[].product(product/v2).buyingOptions[].dealDetails(product.deal-details/v1),rankedPromotions[].product(product/v2).buyingOptions[].price(product.price/v1),rankedPromotions[].product(product/v2).buyingOptions[].promotionsUnified(product.promotions-unified/v1),rankedPromotions[].product(product/v2).productImages(product.product-images/v2),rankedPromotions[].product(product/v2).twisterVariations(product.twister-variations/v2)\"; experiments=\"newEnergyEfficiencyRegulation_adh3j34sa,BadgeColors_4da10b4,slotName_72rvpj15,insightTypes_72rvpj15\"", "X-Amzn-Encrypted-Slate-Token": "AnYxzfAmKg4nFcYztaT/IsR+F6XOcMm5P54MiWaRK0rNPQpBlUzbSymIG95di4gVz7reRop4t/+f9tEAjvHBARZwap+7ftp56iBFuYXzJ4uu25Evo+5pdegZy2QmzA9f48dlBdEMk7ap3cciWhZDFFcbqSrF07p/A1X0j3BQwDUHEGe/TIz0po8yta/NxBbybO5/RQ+yvl13J5O1VgeS74jvxO54FtevUADxOoj2HSEv4284lIC+kVL+jM811r2AFNfgShkdgd6l", "Sec-Ch-Ua-Platform": "\"Windows\"", "Origin": "https://www.amazon.it", "Sec-Fetch-Site": "same-site", "Sec-Fetch-Mode": "cors", "Sec-Fetch-Dest": "empty", "Referer": "https://www.amazon.it/", "Accept-Encoding": "gzip, deflate, br", "Priority": "u=1, i"}
    resp = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies).json()['entity']
    parse_promos(resp)

def run_schedule():
    # log starting check

    while True:
        current_time = datetime.utcnow().time()
        if current_time >= dt_time(5, 0) and current_time <= dt_time(18, 0):
            get_new_deals()
            time.sleep(300)  # Sleep for 5 minutes
        else:
            # Sleep for 1 sec before checking the time again
            time.sleep(1)

app = Flask(__name__)
app.register_blueprint(default_routes)

if __name__ == '__main__':
    # Run the schedule in a separate thread
    scheduler_thread = threading.Thread(target=run_schedule)
    scheduler_thread.daemon = True  # Daemonize thread
    scheduler_thread.start()

    app.run(host='0.0.0.0', port=5000, debug=True)
