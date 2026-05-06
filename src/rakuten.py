import os
import requests
from typing import Any

SEARCH_API = "https://app.rakuten.co.jp/services/api/IchibaItem/Search/20220601"

# 収納カテゴリのジャンルID (楽天市場: インテリア・寝具・収納 > 収納家具)
STORAGE_GENRE_ID = "215831"


def fetch_storage_products(hits: int = 10) -> list[dict[str, Any]]:
    params = {
        "applicationId": os.environ["RAKUTEN_APP_ID"],
        "genreId": STORAGE_GENRE_ID,
        "hits": hits,
        "sort": "-reviewCount",
        "imageFlag": 1,
        "formatVersion": 2,
    }
    affiliate_id = os.environ.get("RAKUTEN_AFFILIATE_ID", "")
    if affiliate_id:
        params["affiliateId"] = affiliate_id

    resp = requests.get(SEARCH_API, params=params, timeout=15)
    resp.raise_for_status()
    data = resp.json()

    products = []
    for item in data.get("Items", []):
        products.append({
            "name": item["itemName"],
            "price": item["itemPrice"],
            "url": item.get("affiliateUrl") or item["itemUrl"],
            "shop": item["shopName"],
            "review_count": item["reviewCount"],
            "review_average": item["reviewAverage"],
            "image_url": item["mediumImageUrls"][0] if item["mediumImageUrls"] else "",
            "catch_copy": item.get("catchcopy", ""),
        })
    return products
