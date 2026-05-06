import os
import requests

def fetch_storage_products(hits=10):
    url = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20220601"

    params = {
        "applicationId": os.environ["RAKUTEN_APP_ID"],
        "accessKey": os.environ["RAKUTEN_ACCESS_KEY"],
        "keyword": "収納",
        "hits": hits,
        "sort": "-reviewCount",
        "imageFlag": 1,
        "formatVersion": 2
    }

    resp = requests.get(url, params=params)
    resp.raise_for_status()
    data = resp.json()

    products = []
    for item in data.get("Items", []):
        products.append({
            "name": item.get("itemName", ""),
            "price": item.get("itemPrice", 0),
            "url": item.get("itemUrl", ""),
            "image": item.get("mediumImageUrls", [""])[0] if item.get("mediumImageUrls") else "",
            "review_count": item.get("reviewCount", 0),
            "review_average": item.get("reviewAverage", 0),
            "shop_name": item.get("shopName", "")
        })

    return products
