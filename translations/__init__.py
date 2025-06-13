import os
import locale
from importlib import import_module

LANGS = ["en", "fr", "es", "pt", "de", "nl"]
TRANSLATIONS = {"en": {}}
for c in LANGS[1:]:
    TRANSLATIONS[c] = import_module(f".{c}", __name__).TEXTS


def detect_lang():
    env = os.getenv("APP_LANG")
    if env and env != "auto":
        return env
    loc = locale.getdefaultlocale()[0]
    if loc:
        code = loc.split("_")[0]
        if code in LANGS:
            return code
    return "en"

LANG = detect_lang()

def tr(text: str) -> str:
    return TRANSLATIONS.get(LANG, {}).get(text, text)
