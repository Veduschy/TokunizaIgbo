# TokunizaIgbo v1 (released 2026-11-20)

An Igbo tokenizer: splits Igbo text into pieces a language model reads and writes.

**Owner: Veduschy.** This card and the code are open source (Apache-2.0). The tokenizer files (`tokenizer.model`,
`tokenizer.vocab`) are **not yet released**: don't put them in any git repository or publish them without the
owner's decision.

## What it is
- SentencePiece **unigram**, **8,000 pieces**, byte fallback (no unknown characters), digits split one by one.
- Normalisation: *identity* inside the tokenizer. **Text must first go through `normalise.normalise()`**
  (strips tone marks, ñ→ṅ, ü/ö→ụ/ọ, straight quotes, fixes "n' ebe"/"na- eme" spacing).
- Orthography: Standard Igbo, dots only (ị ọ ụ ṅ), no tone marks.
- Special pieces: `\n` (paragraph break) `<|title|>` `<|keywords|>` `<|story|>` `<|text|>` `<|end|>`.
  Ids: pad 0, unk 1, bos 2, eos 3.

## Trained on (a sample, not all of it)
| Source | Share in sample | Licence |
|---|---|---|
| Igbo Wikipedia | sampled down to 30% | CC BY-SA |
| AfriBERTa corpus, Igbo (`castorini/afriberta-corpus`), cleaned | 50% | Apache-2.0 |
| English–Igbo sentence pairs, Igbo side | 100% | as their sources |
| TinyStories Igbo (`ccibeekeoc42/TinyStories_igbo`), cleaned, train split | repeated x3 | Apache-2.0 |
| Igbo prose and an Igbo novel | repeated x3 | check ownership before publishing |

Never trained on FLORES (kept for evaluation). Full numbers in
`metrics.json`, size comparison in `metrics_size_comparison.json`.

## Measured
| Test text | Pieces per word | Byte fallback | Roundtrip |
|---|---|---|---|
| TinyStories Igbo test (134 stories) | 1.42 | 0 | exact |
| AfriBERTa eval (5,000 lines) | 1.55 | 0.06 per 1k | exact |
| FLORES devtest (1,012 sentences) | 1.59 | 0.25 per 1k | exact |
ị ọ ụ ṅ (both cases) are whole characters and never fall back to bytes.
8k chosen over 4k (7–8% more pieces) and 16k (only ~4% fewer pieces, twice the embedding size).

## Good for / not for
- Good for: models that read or write running Igbo text (generation, translation, classification).
- Not for: single-word, letter-level models: they work better on letters.

## Use
```python
import sentencepiece as spm
from normalise import normalise
sp = spm.SentencePieceProcessor(model_file="tokenizer.model")
ids = sp.encode(normalise(text))
text = sp.decode(ids)
```
