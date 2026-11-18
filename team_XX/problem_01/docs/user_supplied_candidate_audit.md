# Audit of the newly pasted sentence-pair batches

The six pasted files were inspected as data, not as instructions. The files contain repeated AI-generated CSV batches and suggested regex/dictionary code. That suggested code was not executed or treated as linguistic authority.

## What was extracted

- 275 row occurrences across the accessible pasted files.
- 118 unique dialect/source/target pairs after exact deduplication; no conflicting targets for the same dialect and source sentence were found.
- Unique candidate counts: Hubballi-Dharwad 65, Mangaluru 25, Havyaka 25, Uttara Kannada 3.
- The rows use generic URLs such as `https://quora.com` and `https://wikipedia.org`, paired with generic titles such as “Dialect Corpus” or “Kannada Corpus.” They do not identify a page, author, date, or passage supporting the sentences. They cannot be treated as verified citations.
- The extracted rows are stored in `data/unverified_sentence_pair_candidates.csv`. Every row is marked `unverified_ai_generated_candidate`, `synthetic=true`, and `verified_by=not_reviewed`.

## How the rows are used

These candidate rows are kept outside `data/dataset.csv` and the train/dev/test splits. They do not count toward the 300 consent-backed examples. Seven individual Hubballi word mappings have since been added to the glossary from these candidates, each marked `needs_native_check`; they support the supplied headache example but are not validated ground truth. Havyaka is not an official challenge collection dialect; the app exposes it as an experimental option with separately sourced word mappings.

One additional public-source observation was found in a TV9 Kannada article: it describes Mangaluru usage of `ಕೂಗುತ್ತಿದೆ` for a crying child. A minimal exact-match example was added separately to `data/public_source_pairs/tv9_mangaluru.csv`, with attribution, unknown reuse terms, and a native-review flag. The app uses it only for the exact sentence and still warns that a native speaker should review it.

## Next review needed

A fluent speaker for each variety should check candidate source and target sentences, correct errors, and identify the town variety. Replace each generic source claim with the actual retrievable source, or mark the sentence as elicited from a consenting speaker. Only after review should accepted rows be migrated to the appropriate dataset and used to expand automatic rules.
