"""Thin OpenAI-compatible client for the lab vLLM endpoint. Reads .env (INF_API_KEY, INF_BASE_URL, INF_MODEL)."""
import os, time, pathlib
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv(pathlib.Path(__file__).resolve().parents[1] / ".env")

BASE_URL = os.environ["INF_BASE_URL"].rstrip("/") + "/v1"
API_KEY = os.environ["INF_API_KEY"]
MODEL = os.environ.get("INF_MODEL", "Qwen3.8-27B")

_client = OpenAI(base_url=BASE_URL, api_key=API_KEY, timeout=180, max_retries=2)


def chat(messages, temperature=0.0, n=1, max_tokens=600, thinking=False, model=MODEL, retries=4):
    """Return a list of n dicts: {content, reasoning, finish_reason}."""
    extra = {"chat_template_kwargs": {"enable_thinking": bool(thinking)}}
    for attempt in range(retries):
        try:
            r = _client.chat.completions.create(
                model=model, messages=messages, temperature=temperature, n=n,
                max_tokens=max_tokens, extra_body=extra,
            )
            return [{
                "content": c.message.content or "",
                "reasoning": getattr(c.message, "reasoning_content", None) or getattr(c.message, "reasoning", None),
                "finish_reason": c.finish_reason,
            } for c in r.choices]
        except Exception as e:  # noqa: BLE001
            if attempt == retries - 1:
                raise
            time.sleep(2 ** attempt)
