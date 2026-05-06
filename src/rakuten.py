import os
import requests
from typing import Any

SEARCH_API = "https://openapi.rakuten.co.jp/ichibams/api/IchibaItem/Search/20220601"


def fetch_storage_products(hits: int = 10) -> list[dict[str, Any]]:
    headers = {
        "Authorization": f"Bearer {os.environ['RAKUTEN_ACCESS_KEY']}",
    }
    params = {
        "applicationId": os.environ["RAKUTEN_APP_ID"],
        "keyword": "収納",
        "hits": hits,
        "sort": "-reviewCount",
        "imageFlag": 1,
        "formatVersion": 2,
    }
    resp = requests.get(SEARCH_API, headers=headers, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    products = []
    for item in data.get("Items", []):
        products.append({
            "name": item["itemName"],
            "price": item["itemPrice"],
            "url": item["itemUrl"],
            "shop": item["shopName"],
            "review_count": item["reviewCount"],
            "review_average": item["reviewAverage"],
            "image_url": item["mediumImageUrls"][0] if item["mediumImageUrls"] else "",
            "catch_copy": item.get("catchcopy", ""),
        })
    return products
