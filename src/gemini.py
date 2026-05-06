import os
from typing import Any
import google.generativeai as genai

SYSTEM_PROMPT = """あなたは楽天ROOMのインフルエンサーです。
収納・整理整頓が好きなユーザーに向けて、おしゃれで共感を呼ぶ投稿文を書くのが得意です。
絵文字を適度に使い、親しみやすいトーンで書いてください。"""


def analyze_products(products: list[dict[str, Any]]) -> str:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_PROMPT,
    )

    product_list = "\n".join([
        f"【商品{i+1}】\n"
        f"  名前: {p['name']}\n"
        f"  価格: ¥{p['price']:,}\n"
        f"  ショップ: {p['shop_name']}\n"
        f"  レビュー: {p['review_average']}点 ({p['review_count']}件)\n"
        f"  URL: {p['url']}"
        for i, p in enumerate(products)
    ])

    prompt = f"""以下の収納商品の中から特におすすめの3商品を選び、
楽天ROOMに投稿する紹介文を生成してください。

条件:
- 各商品に見出し（商品名）を付ける
- 商品の魅力・使い道を2〜3文で説明
- 価格とレビュー情報を自然に盛り込む
- 最後に楽天ROOMのアフィリエイトURLを記載
- 全体を1つのLINEメッセージとして読みやすくまとめる
- 冒頭に今日のおすすめ収納アイテムとして一言添える

商品一覧:
{product_list}
"""

    response = model.generate_content(prompt)
    return response.text
