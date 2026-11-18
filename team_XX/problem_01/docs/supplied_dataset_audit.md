# Audit of supplied sentence-pair files

Reviewed 18 November 2026. The CSVs below were supplied as research outputs. Their rows are not participant submissions and are not included in `data/dataset.csv` or in the 300-row collection count.

## `kannada_dialect_sentence_pairs.csv` (22 rows)

- 9 rows are labeled Havyaka/Siddapur and cite a Quora question that could not be independently retrieved. Do not treat the attribution, location, or paired translations as verified.
- 5 Mangaluru rows reproduce the examples on the cited Kannada Wikipedia page. Three source entries give explicit parenthetical glosses that support the comparison pairs. Those three are kept in `data/public_source_pairs/mangaluru_wikipedia.csv`, with CC BY-SA 4.0 attribution and a native-review flag. The other two require interpretation beyond the source gloss and were left out.
- 6 Dharwad rows cite a OneIndia article. Its dialect examples are published there, but the article does not provide full textbook rewrites for these complete sentences. The supplied target sentences remain unreviewed drafts, and the article is marked © All Rights Reserved, so its text was not copied into the project dataset.
- 2 rows cite a Quora question and could not be independently verified.

## `kannada_dialect_sentence_pairs-v3.csv` (69 rows)

The file has 18 Havyaka, 10 generic Uttara Kannada, 7 Mangaluru, 31 Dharwad, and 3 Hubballi-Dharwad rows. It adds no speaker, consent, reviewer, or recording provenance. Its source labels do not verify the sentence pairs: several Mangaluru sentences are attributed to a Wikipedia page that contains different examples; Quora entries could not be retrieved; and the 27 OneIndia rows have assistant-supplied textbook rewrites rather than source-provided parallel targets. One row points to TranslateSwift, which is not an authoritative dialect source. The source licenses also do not support treating the full file as an open dataset.

## How to use these files

Use them as leads for fluent-speaker review or for finding potential public references. Do not import their unverified rows as collected, consented, reviewed, or gold-standard data. Only the three source-gloss-supported Wikipedia examples are included as a separately licensed, explicitly public-source supplement; they still need native review and cannot replace participant collection.
