# Nudi Setu completion status

Updated 18 November 2026.

## Ready in the workspace

- Streamlit demo with all three dialect options, converter trace, side-by-side word highlighting, batch CSV, overview, glossary explorer, and collection resources.
- Automatic offline rules pipeline, Unicode normalization, validation, speaker-separated split builder, and held-out evaluation tooling. The website does not require or call an AI service.
- The automated test suite is in `tests/`; its last full run had 21 passes before the latest data/rubric edits. Rerun it before publishing.
- Starter dataset has 3 official examples plus 60 explicitly synthetic examples. The glossary has 116 entries; 61 are marked `needs_native_check`.
- The UI offers the three challenge dialects plus experimental Havyaka. Seven mappings drawn from TV9's published regional-word examples are flagged `needs_native_check`; Havyaka is not counted as an official challenge collection dialect.
- External corpora are kept separate. The Kannada blog corpus is used only for an aggregate standard-text preservation check; it does not supply dialect pairs.
- Audited the locally supplied Kannada audio folder: it contains 1,000 MP3s, but the supplied files have no transcripts or dialect/town/speaker metadata and cannot count toward the conversion dataset.
- Audited the earlier supplied public-source sentence-pair files (22 and 69 rows). Three Mangaluru pairs had a retrievable source with explicit glosses and compatible reuse terms; those are kept separately under CC BY-SA 4.0 and still need native review.
- The chat screen auto-converts entered Kannada and explains when no known rule matched; the Overview labels public-source pairs separately.
- Audited the newly pasted batches: 275 row occurrences deduplicated to 118 unverified candidates. They are downloadable from Overview but excluded from conversion/training because the generic source links do not substantiate them.
- Added seven provisional Hubballi word mappings from the supplied candidates, including the headache sentence forms; they are marked for native-speaker review.
- Added one separately attributed Mangaluru exact-match example grounded in a TV9 Kannada report. It is flagged for local review; reuse terms are unverified.
- Added a rubric-by-rubric submission audit in `docs/submission_readiness.md` and a source/terms catalog in `data/source_manifest.csv`.
- Bilingual consent template, consent log, CSV template, copy-ready remote form guide, and audio validation tool are present.

## Still required before the submission can claim the data requirements are complete

- **Real speaker data: 0/300.** The current count is 0/100 each for Uttara Kannada, Mangaluru, and Hubballi-Dharwad. The project requires original sentences from consenting speakers; public, synthetic, and general Kannada corpora do not count.
- **Topic coverage: 0/20 real per topic for each dialect.** The 100-row target is 20 each for home, market, school, travel, and festivals.
- No consent records, second-person reviews, native-speaker glossary approvals, or optional audio recordings have been collected yet.
- The held-out split is empty, so no conversion metrics are reported. `python tools/validate_dataset.py` exits non-zero until data and topic targets are met.
- The bilingual consent wording still needs a fluent local Kannada reader to review it and the team must provide participants a withdrawal contact before sharing the form.
- Team number/credit and Google Drive links for the video and source data are still outstanding. The current 45-second demo video and poster are included in `assets/` and linked from the repository README. GitHub publishing is in progress.

## Next steps for the team

1. Review `consent/consent_form_template.md`, fill in a withdrawal contact, and use `docs/remote_collection_form.md` for remote contributions.
2. Collect original adult-speaker sentences and record each speaker's text-release choice in `consent/consent_log.csv`.
3. Have a second fluent reviewer create/check every `standard_text`; do not add unreviewed or synthetic rows as collected.
4. Run `python tools/validate_dataset.py`. Resolve all reported gaps before treating the dataset as complete.
5. Run `python tools/build_splits.py`, build/update the glossary from training data only, then run `python tools/run_evaluation.py`.
6. Replace the team placeholder in the repository path/credits, verify the GitHub repository, and add the approved Google Drive source/dataset links.
