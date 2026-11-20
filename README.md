# TokunizaIgbo

A shared Igbo tokenizer. One home, numbered versions, every project takes a copy.

## Versions
| Version | Date | Pieces | Built by | Notes |
|---|---|---|---|---|
| [v1](v1/CARD.md) | 2026-11-20 | 8,000 | SentencePiece unigram | first release; title/keywords/story markers |

## Rules
1. **A released version never changes.** Any change (retrain, new pieces, normaliser fix) is a new version folder.
2. **Projects copy, never link.** `python copy_to.py path/to/<Project>` puts a checked copy in
   `<Project>/models/tokenizer/tokunizaigbo-v1/`. A project that wants a newer version copies it alongside and
   switches deliberately (a model trained with v1 must keep using v1).
3. **Always normalise first:** each version ships its own `normalise.py`; use the one from the same version.
4. **What is open, what is not:** the code, cards and metrics here are open source (Apache-2.0, see `LICENSE` and
   `NOTICE`). The tokenizer files themselves (`tokenizer.model`, `tokenizer.vocab`) are not in this repository and
   not yet released: that is a separate decision by the owner (Veduschy), after checking the training texts' rights.

## Check a copy
`python v1/check.py` (needs `pip install sentencepiece`): checksums, vocab size, special pieces, roundtrip, dots.

## Licence
Code and documentation: [Apache License 2.0](LICENSE), copyright 2026 Veduschy. See [NOTICE](NOTICE).
