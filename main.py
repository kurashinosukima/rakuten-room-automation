import sys
from dotenv import load_dotenv

from src.rakuten import fetch_storage_products
from src.gemini import analyze_products
from src.line_notify import send_line_message
from src.history import filter_unposted_products, save_posted_items


def main() -> None:
    load_dotenv()

    print("楽天市場から収納商品を取得中...")
    products = fetch_storage_products(hits=20)
    if not products:
        print("商品が取得できませんでした", file=sys.stderr)
        sys.exit(1)
    print(f"{len(products)}件取得完了")

    products = filter_unposted_products(products)
    print(f"重複除外後: {len(products)}件")
    if len(products) < 3:
        print("新規商品が不足しています", file=sys.stderr)
        sys.exit(1)

    print("Geminiで商品分析・投稿文生成中...")
    message, selected_item_codes = analyze_products(products)
    print("生成完了:\n", message[:200], "...")

    save_posted_items(selected_item_codes)
    print(f"履歴保存完了: {selected_item_codes}")

    print("LINEに通知送信中...")
    send_line_message(message)
    print("送信完了")


if __name__ == "__main__":
    main()
