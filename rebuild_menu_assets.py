#!/usr/bin/env python3
import json
import re
import time
import unicodedata
from pathlib import Path
from typing import Dict, List

import fitz  # PyMuPDF
from deep_translator import GoogleTranslator

APP_LANGS = ["en", "de", "zh"]

TRANSLATOR_LANG_MAP = {
    "en": "en",
    "de": "de",
    "zh": "zh-CN",   # important
}

PDF_PATH = Path("/Users/anirudhchawla/Downloads/ming_group_website/static/m1/m1-menu.pdf")

OUT_MENU_INDEX = Path("menu_index.json")
OUT_MENU_SEARCH_INDEX = Path("menu_search_index.json")
OUT_MENU_SEARCH_READY = Path("menu_search_ready.json")

TARGET_LANGS = ["en", "de", "zh-cn"]
MIN_TEXT_LEN_FOR_TRANSLATION = 20
TRANSLATION_SLEEP_SECONDS = 1.2
RETRY_SLEEP_SECONDS = 4
MAX_RETRIES = 3


def clean_pdf_text(text: str) -> str:
    text = text.replace("\u00a0", " ")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def guess_title(text: str) -> str:
    lines = [line.strip() for line in text.splitlines() if line.strip()]
    for line in lines[:8]:
        if 2 <= len(line) <= 100:
            return line
    return ""


def contains_cjk(text: str) -> bool:
    return bool(re.search(r"[\u4e00-\u9fff]", text))


def strip_accents(text: str) -> str:
    return "".join(
        ch for ch in unicodedata.normalize("NFKD", text)
        if not unicodedata.combining(ch)
    )


def replace_german_chars(text: str) -> str:
    replacements = {
        "ä": "ae", "ö": "oe", "ü": "ue", "ß": "ss",
        "Ä": "Ae", "Ö": "Oe", "Ü": "Ue",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text


def normalize_latin_text(text: str) -> str:
    text = text.lower()
    text = replace_german_chars(text)
    text = strip_accents(text)
    text = text.replace("&", " and ")
    text = text.replace("/", " ")
    text = text.replace("-", " ")
    text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\b[a-z]\b", " ", text)
    text = re.sub(r"\b\d+[.,]\d{1,2}\b", " ", text)
    text = re.sub(r"\b\d+\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def normalize_multilingual_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    text = text.replace("&", " and ")
    text = text.replace("/", " ")
    text = text.replace("-", " ")
    text = re.sub(r"[^\w\s\u4e00-\u9fff]", " ", text, flags=re.UNICODE)
    text = re.sub(r"\b[a-z]\b", " ", text)
    text = re.sub(r"\b\d+[.,]\d{1,2}\b", " ", text)
    text = re.sub(r"\b\d+\b", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def tokenize(text: str) -> List[str]:
    words = text.split()
    seen = set()
    out = []
    for w in words:
        if len(w) < 2:
            continue
        if w not in seen:
            seen.add(w)
            out.append(w)
    return out


from langdetect import detect

def detect_language(text: str) -> str:
    text = (text or "").strip()

    if not text:
        return "en"

    if contains_cjk(text):
        return "zh"

    try:
        lang = detect(text)
        if lang.startswith("de"):
            return "de"
        if lang.startswith("zh"):
            return "zh"
        return "en"
    except Exception:
        return "en"
def chunk_text(text: str, max_len: int = 3500) -> List[str]:
    """
    Break long text into smaller pieces to reduce translator failures.
    """
    text = text.strip()
    if len(text) <= max_len:
        return [text]

    parts = re.split(r"(\n\n+|\.\s+)", text)
    chunks = []
    current = ""

    for part in parts:
        if len(current) + len(part) <= max_len:
            current += part
        else:
            if current.strip():
                chunks.append(current.strip())
            current = part

    if current.strip():
        chunks.append(current.strip())

    return chunks


def translate_text_google(text: str, src: str, dest: str) -> str:
    if not text.strip():
        return ""

    pieces = chunk_text(text)
    translated_parts = []

    for piece in pieces:
        success = False
        last_error = None

        for attempt in range(1, MAX_RETRIES + 1):
            try:
                translated = GoogleTranslator(source=src, target=dest).translate(piece)
                translated_parts.append(translated.strip())
                time.sleep(TRANSLATION_SLEEP_SECONDS)
                success = True
                break
            except Exception as e:
                last_error = e
                if attempt < MAX_RETRIES:
                    time.sleep(RETRY_SLEEP_SECONDS * attempt)

        if not success:
            raise RuntimeError(f"Translation failed {src}->{dest}: {last_error}")

    return "\n".join(translated_parts).strip()

def build_translations(text: str) -> Dict[str, object]:
    source_lang = detect_language(text)

    translations = {lang: "" for lang in APP_LANGS}
    translations[source_lang] = text

    if len(text.strip()) < MIN_TEXT_LEN_FOR_TRANSLATION:
        return {
            "detected_source_lang": source_lang,
            "translations": translations,
        }

    src_for_translator = TRANSLATOR_LANG_MAP[source_lang]

    for target_lang in APP_LANGS:
        if target_lang == source_lang:
            continue

        dest_for_translator = TRANSLATOR_LANG_MAP[target_lang]

        try:
            translations[target_lang] = translate_text_google(
                text=text,
                src=src_for_translator,
                dest=dest_for_translator,
            )
        except Exception as e:
            print(f"Warning: translation failed {source_lang} -> {target_lang}: {e}")
            translations[target_lang] = ""

    return {
        "detected_source_lang": source_lang,
        "translations": translations,
    }

def extract_menu_index() -> List[Dict]:
    if not PDF_PATH.exists():
        raise SystemExit(f"PDF not found: {PDF_PATH}")

    doc = fitz.open(PDF_PATH)
    pages = []

    for i, page in enumerate(doc, start=1):
        raw_text = page.get_text("text")
        cleaned = clean_pdf_text(raw_text)

        lang_bundle = build_translations(cleaned)

        pages.append({
            "page": i,
            "title": guess_title(cleaned),
            "text": cleaned,
            "char_count": len(cleaned),
            "needs_ocr": len(cleaned) < 80,
            "detected_source_lang": lang_bundle["detected_source_lang"],
            "translations": lang_bundle["translations"],
        })

        print(f"Processed page {i}/{len(doc)}")

    output = {
        "source_pdf": str(PDF_PATH),
        "total_pages": len(pages),
        "pages": pages,
    }

    OUT_MENU_INDEX.write_text(
        json.dumps(output, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Created: {OUT_MENU_INDEX}")
    return pages


def build_search_index(pages: List[Dict]) -> List[Dict]:
    out = []

    for p in pages:
        t = p["translations"]
        out.append({
            "page": p["page"],
            "detected_source_lang": p["detected_source_lang"],
            "text": p["text"],
            "en": t.get("en", ""),
            "de": t.get("de", ""),
            "zh": t.get("zh-cn", ""),
        })

    OUT_MENU_SEARCH_INDEX.write_text(
        json.dumps(out, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Created: {OUT_MENU_SEARCH_INDEX}")
    return out


def build_search_ready(search_pages: List[Dict]) -> List[Dict]:
    out = []

    for p in search_pages:
        en_text = p.get("en", "") or ""
        de_text = p.get("de", "") or ""
        zh_text = p.get("zh", "") or ""
        raw_text = p.get("text", "") or ""

        en_norm = normalize_latin_text(en_text)
        de_norm = normalize_latin_text(de_text)
        zh_norm = normalize_multilingual_text(zh_text)
        raw_norm = normalize_multilingual_text(raw_text)

        combined_search = " ".join(
            x for x in [en_norm, de_norm, zh_norm, raw_norm] if x
        ).strip()
        combined_search = re.sub(r"\s+", " ", combined_search)

        out.append({
            "page": p["page"],
            "detected_source_lang": p["detected_source_lang"],
            "raw_text": raw_text,
            "translations": {
                "en": en_text,
                "de": de_text,
                "zh": zh_text,
            },
            "normalized": {
                "en": en_norm,
                "de": de_norm,
                "zh": zh_norm,
                "raw": raw_norm,
            },
            "tokens": tokenize(combined_search),
            "search_text": combined_search,
        })

    OUT_MENU_SEARCH_READY.write_text(
        json.dumps(out, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"Created: {OUT_MENU_SEARCH_READY}")
    return out


def main() -> None:
    pages = extract_menu_index()
    search_pages = build_search_index(pages)
    build_search_ready(search_pages)
    print("Done. Existing JSON files were overwritten.")


if __name__ == "__main__":
    main()