# Held-out evaluation results

Test rows: **30** (only collected, non-synthetic rows are accepted).

| System | Exact match | Word accuracy (1-WER) | CER | chrF |
|---|---:|---:|---:|---:|
| Copy input (no rules) | 36.67% | 80.65% | 11.73% | 79.14% |
| Rules only | 40.00% | 83.87% | 9.76% | 82.46% |

## Per-dialect results

| Dialect | N | Exact match | Word accuracy | CER | chrF |
|---|---:|---:|---:|---:|---:|
| Hubballi-Dharwad | 10 | 10.00% | 69.49% | 20.62% | 65.13% |
| Mangaluru | 10 | 50.00% | 91.18% | 6.60% | 89.71% |
| Uttara Kannada | 10 | 60.00% | 89.83% | 3.80% | 92.55% |

Mismatches requiring review: **18**. See `docs/error_analysis.csv`; `meaning_ok` is intentionally blank for a human reviewer.

## Method and limits

Word accuracy is 1-WER using the project's Unicode word tokenizer. CER is character edit distance divided by reference length. chrF is sacreBLEU chrF (character order 6, beta 2), averaged per sentence.

The optional Gemini ablation sends each held-out sentence to Google's API. Run only when the consent/usage basis permits external processing; otherwise leave `--with-llm` off. The rules-only engine remains offline.
