import os
from typing import Any
import google.generativeai as genai

SYSTEM_PROMPT = """あなたは楽天ROOM「暮らしのスキマ」のインフルエンサーです。
コンセプト: 賃貸の隙間15cmから始める収納改善
ターゲット: 賃貸住まいの20-30代女性
絵文字を適度に使い、親しみやすいトーンで書いてください。"""

SELECTION_PROMPT_TEMPLATE = """あなたは『暮らしのスキマ』ブランドのROOMインフルエンサーです。
以下の商品の中から、ブランドコンセプトに合う3商品を選んでください。

【絶対選んではいけない商品】
- 充電ケーブル、電子機器
- 布団、寝具（ただし収納方法に特化したものは可）
- ダイヤル錠、キーボックス
- 食品、化粧品
- 大型家電
- 収納と関係ない商品

【優先して選ぶべき商品】
- 隙間家具、隙間ラック
- 突っ張り棒、突っ張り棚
- クローゼット・押し入れ収納ボックス
- ドア裏フック、ドア掛け収納
- 石膏ボード対応の壁面収納
- 賃貸OKを謳う収納家具

商品一覧:
{product_list}

選んだ3商品の番号をカンマ区切りで答えてください（例: 1,3,5）。
番号のみ出力し、他のテキストは一切含めないでください。"""

POST_PROMPT_TEMPLATE = """以下の3商品を紹介する楽天ROOM投稿文を生成してください。

条件:
- 冒頭に「暮らしのスキマ」らしい一言を添える（賃貸・隙間・収納改善をテーマに）
- 各商品に見出し（商品名を要約）を付ける
- 商品の魅力・使い道を2〜3文で説明
- 価格とレビュー情報を自然に盛り込む
- 全体を1つのLINEメッセージとして読みやすくまとめる
- 本文の最後に以下の「📎 商品リンク一覧」セクションをそのまま追加すること（変更・省略禁止）

紹介する3商品:
{product_list}

本文末尾に必ず追加するセクション（一字一句変えずにそのまま出力）:
📎 商品リンク一覧

{product_links}"""


def analyze_products(products: list[dict[str, Any]]) -> str:
    genai.configure(api_key=os.environ["GEMINI_API_KEY"])
    model = genai.GenerativeModel(
        model_name="gemini-2.5-flash",
        system_instruction=SYSTEM_PROMPT,
    )

    # ステップ1: ブランドコンセプトに合う3商品を選定
    product_list_all = "\n".join([
        f"【商品{i+1}】\n"
        f"  名前: {p['name']}\n"
        f"  価格: ¥{p['price']:,}\n"
        f"  ショップ: {p['shop_name']}\n"
        f"  レビュー: {p['review_average']}点 ({p['review_count']}件)\n"
        f"  URL: {p['url']}"
        for i, p in enumerate(products)
    ])

    selection_response = model.generate_content(
        SELECTION_PROMPT_TEMPLATE.format(product_list=product_list_all)
    )
    raw = selection_response.text.strip()
    try:
        indices = [int(n.strip()) - 1 for n in raw.split(",")]
        selected = [products[i] for i in indices if 0 <= i < len(products)][:3]
    except Exception:
        selected = products[:3]

    # ステップ2: 選定した3商品で投稿文を生成
    product_list_selected = "\n".join([
        f"【商品{i+1}】\n"
        f"  名前: {p['name']}\n"
        f"  価格: ¥{p['price']:,}\n"
        f"  ショップ: {p['shop_name']}\n"
        f"  レビュー: {p['review_average']}点 ({p['review_count']}件)\n"
        f"  URL: {p['url']}"
        for i, p in enumerate(selected)
    ])

    product_links = "\n\n".join([
        f"【商品{i+1}】{p['name'][:30]}\n"
        f"💰 ¥{p['price']:,} | ⭐ {p['review_average']} ({p['review_count']:,}件)\n"
        f"🔗 {p['url']}"
        for i, p in enumerate(selected)
    ])

    post_response = model.generate_content(
        POST_PROMPT_TEMPLATE.format(
            product_list=product_list_selected,
            product_links=product_links,
        )
    )
    return post_response.text
