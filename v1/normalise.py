"""TokunizaIgbo v1: text normalisation. Run every text through normalise() BEFORE tokenizing.

Never edit in a released version: change it in a new version.

Rule: Standard Igbo, dots only (ị ọ ụ ṅ), no tone marks.
"""
import re
import unicodedata

# Tone marks: grave, acute, circumflex, macron, caron,
# plus double acute/grave, which turn up occasionally in web text.
TONE_MARKS = {"̀", "́", "̂", "̄", "̌", "̋", "̏"}

DOTTED = set("ịọụṅỊỌỤṄ")

# Double-encoded UTF-8 (curly quotes read as cp1252 twice), seen in TinyStories_igbo.
_MOJIBAKE = [
    ("Ã¢â‚¬Å“", '"'), ("Ã¢â‚¬Â\x9d", '"'), ("Ã¢â‚¬â„¢", "'"), ("Ã¢â‚¬Ëœ", "'"),
    ("Ã¢â‚¬Â", '"'), ("Ã¢â‚¬", '"'),
    ("â€œ", '"'), ("â€\x9d", '"'), ("â€™", "'"), ("â€˜", "'"), ("â€", '"'),
    ("Ëœ", ""),
]


def fix_mojibake(s: str) -> str:
    for bad, good in _MOJIBAKE:
        s = s.replace(bad, good)
    return s


def strip_tone_marks(s: str) -> str:
    d = unicodedata.normalize("NFD", s)
    return unicodedata.normalize("NFC", "".join(c for c in d if c not in TONE_MARKS))


def has_tone_marks(s: str) -> bool:
    return any(c in TONE_MARKS for c in unicodedata.normalize("NFD", s))


def normalise(s: str) -> str:
    """Apply the orthography rule and light punctuation clean-up to a piece of Igbo text."""
    s = unicodedata.normalize("NFC", s)
    s = fix_mojibake(s)
    s = strip_tone_marks(s)
    # Old spelling of ṅ, and ü/ö used for ụ/ọ in some web text.
    s = s.replace("ñ", "ṅ").replace("Ñ", "Ṅ")
    s = s.replace("ü", "ụ").replace("Ü", "Ụ").replace("ö", "ọ").replace("Ö", "Ọ")
    # Curly quotes -> straight.
    s = s.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    # Elision and hyphen glued to the next word: "n' ebe" -> "n'ebe", "na- eme" -> "na-eme".
    s = re.sub(r"\b([nNkKmM])' (?=\w)", r"\1'", s)
    s = re.sub(r"\b(na|Na|ga|Ga|a|A|e|E)- (?=\w)", r"\1-", s)
    # No space before punctuation.
    s = re.sub(r" +([,.;:!?])", r"\1", s)
    s = re.sub(r"[ \t]+", " ", s)
    return s.strip()


def capitalise_sentences(s: str) -> str:
    """Upper-case the first letter of the text and of each sentence (after . ! ? and an optional quote)."""
    return re.sub(r'(^|[.!?]["\']?\s+["\']?)(\w)', lambda m: m.group(1) + m.group(2).upper(), s)
