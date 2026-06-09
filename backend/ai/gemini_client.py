"""
gemini_client.py - Centralized Gemini API caller (Fixed & Production Ready)
Uses gemini-2.5-flash which has higher free tier limits.
Adds delay between calls to avoid rate limiting.
"""
import os
import time
import requests

# gemini-2.5-flash standard stable name use karein
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/{GEMINI_MODEL}:generateContent"

# Track last call time to enforce minimum gap between requests
_last_call_time = 0
MIN_CALL_GAP = 5  # seconds between calls


def call_gemini(prompt: str, max_retries: int = 3) -> str:
    """
    Call Gemini API with:
    - Minimum 5s gap between calls to avoid rate limiting
    - Auto retry with exponential backoff on 429
    - Explicit JSON formatting constraint
    """
    global _last_call_time

    api_key = os.getenv("GEMINI_API_KEY", "")
    if not api_key or api_key == "your-gemini-api-key-here":
        print("[Gemini] Error: API Key missing or default placeholder used.")
        return ""

    # 1. Enforce minimum gap between API calls BEFORE entering retry loop
    elapsed = time.time() - _last_call_time
    if elapsed < MIN_CALL_GAP:
        wait_gap = MIN_CALL_GAP - elapsed
        time.sleep(wait_gap)

    url = f"{GEMINI_URL}?key={api_key}"
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "maxOutputTokens": 1024,
            "temperature": 0.4,  # Temperature low rakhne se professional resume formats ache bante hain
            # Resume rewriter parser ke liye strict JSON enforce karein
            "responseMimeType": "application/json"
        }
    }

    for attempt in range(max_retries):
        try:
            # Request bhejne se theek pehle timestamp update karein
            _last_call_time = time.time()
            resp = requests.post(url, json=payload, timeout=30)

            # Rate limit handling (429)
            if resp.status_code == 429:
                wait_time = (attempt + 1) * 12
                print(
                    f"[Gemini] Rate limited (429). Waiting {wait_time}s (attempt {attempt+1}/{max_retries})...")
                time.sleep(wait_time)
                continue  # Retries remaining hain to dubara loop chalega

            # Fallback handling (404 / Model issues)
            if resp.status_code in [404, 400]:
                print(
                    f"[Gemini] Primary model issue ({resp.status_code}), trying fallback model...")
                return _call_with_fallback_model(prompt, api_key)

            # Baki kisi bhi server error (500, 503) par raise exception karein
            resp.raise_for_status()

            data = resp.json()
            return data["candidates"][0]["content"]["parts"][0]["text"]

        except Exception as e:
            print(
                f"[Gemini Exception] Attempt {attempt+1} failed with error: {e}")
            if attempt < max_retries - 1:
                time.sleep((attempt + 1) * 5)
                continue
            return ""

    print("[Gemini] All retries exhausted. Returning empty response.")
    return ""


def _call_with_fallback_model(prompt: str, api_key: str) -> str:
    """Try gemini-2.0-flash as secondary fallback model with matching JSON schema."""
    fallback = "gemini-2.0-flash"
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{fallback}:generateContent?key={api_key}"

    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json"
        }
    }

    try:
        resp = requests.post(url, json=payload, timeout=30)
        resp.raise_for_status()
        return resp.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print(f"[Gemini Fallback] Error: {e}")
        return ""
