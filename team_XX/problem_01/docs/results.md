# Held-out evaluation results

Test rows: **0** (only collected, non-synthetic rows are accepted).

No metrics are reported because there are no eligible collected rows in the held-out split.
Synthetic bootstraps and official examples are excluded from reported evaluation.
The error-analysis CSV contains headers only. Add consented, independently reviewed data, rebuild speaker-separated splits, then rerun this command.

## Method and limits

Word accuracy is 1-WER using the project's Unicode word tokenizer. CER is character edit distance divided by reference length. chrF is sacreBLEU chrF (character order 6, beta 2), averaged per sentence.

The optional Gemini ablation sends each held-out sentence to Google's API. Run only when the consent/usage basis permits external processing; otherwise leave `--with-llm` off. The rules-only engine remains offline.
