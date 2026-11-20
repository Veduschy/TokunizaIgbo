"""Check a copy of TokunizaIgbo v1 is complete and works.

  python check.py            # run inside the copied folder (needs: pip install sentencepiece)

Exits non-zero if anything is wrong.
"""
import hashlib
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

SPECIAL = ["\n", "<|title|>", "<|keywords|>", "<|story|>", "<|text|>", "<|end|>"]
SAMPLES = [
    "Otu ụbọchị, Max hụrụ pusi n'elu osisi.",
    "Ọ na-enwe mmasị igwu egwu na ịgba ọsọ na ogige ntụrụndụ.\nHa ṅụrụ mmiri ahụ ma nwee nnọọ obi ụtọ.",
    "ỊỌỤṄ ịọụṅ 2026",
]


def main():
    problems = []
    for line in open(HERE / "SHA256SUMS"):
        digest, name = line.split()
        if hashlib.sha256((HERE / name).read_bytes()).hexdigest() != digest:
            problems.append(f"{name}: checksum differs (file changed or damaged)")

    import sentencepiece as spm
    from normalise import has_tone_marks, normalise

    sp = spm.SentencePieceProcessor(model_file=str(HERE / "tokenizer.model"))
    if sp.get_piece_size() != 8000:
        problems.append(f"vocab size {sp.get_piece_size()} != 8000")
    for s in SPECIAL:
        if sp.piece_to_id(s) == sp.unk_id():
            problems.append(f"special piece {s!r} missing")
    for t in SAMPLES:
        ids = sp.encode(t)
        if sp.decode(ids) != t:
            problems.append(f"roundtrip failed: {t!r}")
        if any(sp.is_byte(i) for i in ids):
            problems.append(f"byte fallback in: {t!r}")
    if normalise("Ìgbò añụrị") != "Igbo aṅụrị" or has_tone_marks(normalise("ákwà")):
        problems.append("normalise() does not strip tone marks / fix ñ")

    if problems:
        print("TokunizaIgbo v1: PROBLEMS\n  " + "\n  ".join(problems))
        sys.exit(1)
    print("TokunizaIgbo v1: OK")


if __name__ == "__main__":
    main()
