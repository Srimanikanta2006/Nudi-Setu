# Public-source research notes

**Research context only. Nothing on this page is team-collected speaker data.** Do not merge `data/public_source_research.csv` into `data/dataset.csv` or use it to claim speaker counts. These sources can help shape neutral interview questions; dialect identity, town, meaning, current usage and textbook rendering need native-speaker review.

## What the sources support

- The News Minute article describes broad North Karnataka patterns, including final `e` to `i`, its transliterated example `mani` against `mane`, `byaeḍa` against `beḍa`, and several Marathi-origin loanwords. It explicitly cautions that North Karnataka contains multiple subregional varieties. These are regional reports, not Hubballi-specific recordings or complete sentences. ([article](https://www.thenewsminute.com/karnataka/marathi-lambadi-north-karnataka-has-rich-linguistic-diversity-145391))
- The Havigannada page reports examples such as `wale/yele`, `iddu`, and `banju/baindu`, and identifies Havigannada as associated with Havyaka communities. It also distinguishes forms by region. Treat this as a low-confidence secondary lead; Havigannada is not interchangeable with all Kannada spoken in Uttara Kannada. ([overview](https://en.wikipedia.org/wiki/Havigannada_dialect))
- A library catalog confirms the existence and bibliographic details of U. P. Upadhyaya’s 1976 comparative study, which includes Kumta among four dialects. The catalog does not verify any sentence in this project. ([catalog record](https://ge.nii.ac.jp/ncid/BA69792318))
- This research batch supplies no source-supported, town-specific Mangaluru Kannada sentence or glossary form. Its general claims about coastal language contact are not enough to add lexical mappings. Record this as a research gap, not as evidence that such forms do not exist.
- The additional Hubballi phrase table supplied later gives several possible examples, but only as Latin transliteration and with alternate standard forms. They are added to the research CSV as low-confidence leads, not as converter inputs. The Wikipedia URL was not retrievable during this check; a third-party copy of the article content reproduces the comparison table, so provenance still needs review. ([copy of the table](https://en-academic.com/dic.nsf/enwiki/508686))
- The supplied Talkpal claims are excluded: that page is a commercial learner resource with no citations for its dialect claims, and some glosses may be overgeneralized. The two Udayavani Mangaluru expressions remain unverified because the cited page could not be retrieved and the supplied notes do not provide their meanings or context.

## Use in the project

`data/public_source_research.csv` is deliberately separate from the required dataset and glossary. Its rows are leads, not conversion pairs. Most examples are transliterated in Latin script, and some are broad regional claims. Do not convert them into Kannada script by guesswork or add them to the glossary until a fluent speaker from the stated locality confirms the form, meaning, context and standard rendering. Do not count them toward the 100-per-dialect real-speaker target.

## Neutral elicitation prompts

Ask a consenting speaker to answer in their own words; do not suggest the online forms first.

1. How would you naturally say “I am going home” in your everyday speech?
2. What would you say to a friend to ask what they are doing? What changes when speaking to an elder?
3. How would you casually say “I don’t want that” or “Don’t do that”?
4. What words do people around you use for common rooms, household items, market goods or food stalls?
5. Can you tell a short, original story about a market visit, cooking, travel, school or a festival?
6. Do nearby towns or different generations use different words or endings? Which town or community variety are you describing?
7. Is there a local word you use that is difficult to translate directly into standard Kannada? Please explain it in context.

Record the participant’s own self-description only if they volunteer it; use a pseudonymous speaker ID, obtain consent first, and have a second reviewer check the standard Kannada sentence. Keep any public-source URL in research/provenance fields, never as a claim of team collection.
