import json
import os
from datetime import datetime, timezone
from typing import Any
from urllib.parse import urlsplit, urlunsplit

HISTORY_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "posted_items.json")


def load_posted_items() -> set[str]:
    if not os.path.exists(HISTORY_PATH):
        return set()
    with open(HISTORY_PATH, encoding="utf-8") as f:
        data = json.load(f)
    return set(data.get("posted_item_codes", []))


def save_posted_items(item_codes: list[str]) -> None:
    existing = load_posted_items()
    merged = sorted(existing | set(c for c in item_codes if c))
    os.makedirs(os.path.dirname(HISTORY_PATH), exist_ok=True)
    with open(HISTORY_PATH, "w", encoding="utf-8") as f:
        json.dump(
            {
                "posted_item_codes": merged,
                "last_updated": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
            },
            f,
            ensure_ascii=False,
            indent=2,
        )


def _strip_query(url: str) -> str:
    parts = urlsplit(url)
    return urlunsplit((parts.scheme, parts.netloc, parts.path, "", ""))


def filter_unposted_products(products: list[dict[str, Any]]) -> list[dict[str, Any]]:
    posted = {_strip_query(u) for u in load_posted_items()}
    return [p for p in products if _strip_query(p.get("item_code", "")) not in posted]
