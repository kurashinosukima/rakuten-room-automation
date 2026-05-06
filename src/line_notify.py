import os
import requests

LINE_API = "https://api.line.me/v2/bot/message/push"


def send_line_message(text: str) -> None:
    token = os.environ["LINE_CHANNEL_ACCESS_TOKEN"]
    user_id = os.environ["LINE_USER_ID"]

    # LINEの1メッセージ上限は5000文字
    chunks = _split_text(text, limit=4000)

    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json",
    }

    for chunk in chunks:
        payload = {
            "to": user_id,
            "messages": [{"type": "text", "text": chunk}],
        }
        resp = requests.post(LINE_API, headers=headers, json=payload, timeout=15)
        resp.raise_for_status()


def _split_text(text: str, limit: int) -> list[str]:
    if len(text) <= limit:
        return [text]
    chunks = []
    while text:
        chunks.append(text[:limit])
        text = text[limit:]
    return chunks
