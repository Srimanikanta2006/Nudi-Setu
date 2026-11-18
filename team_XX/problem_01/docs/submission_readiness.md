# Modalapada 2.0 Problem 1 — submission readiness

**Status: not ready for final submission.** The screenshots specify the deliverables and scoring criteria; this checklist records what is actually present in the project folder. It does not treat synthetic or public-source examples as consented speaker data.

## Rubric check

| Requirement from the slides | Current evidence | Status |
|---|---|---|
| Three target dialects | Converter's challenge choices are Uttara Kannada, Mangaluru, and Hubballi-Dharwad. Havyaka is a separate experimental option. | Implemented |
| At least 300 real sentence pairs, 100 per dialect | `data/dataset.csv` has 3 official challenge examples and 60 synthetic examples; real collected rows are 0/300. | **Missing** |
| Topic balance: home, market, school, travel, festivals | Required 20 real reviewed pairs per topic per dialect; currently 0/20 in every cell. | **Missing** |
| Textbook Kannada reviewed by a second person / another team | No review records or real collected pairs are present. | **Missing** |
| 100+ dialect glossary entries | `data/glossary.csv` has 116 entries, of which 61 are marked `needs_native_check`. | Present; 61 need review |
| Working converter demo | `app.py` runs the automatic, offline Streamlit converter; `docs/demo_script.md` gives a walkthrough. Accuracy is limited to known rules/examples. | Implemented; no benchmark claim |
| Dataset CSV, glossary CSV, README | `data/dataset.csv`, `data/glossary.csv`, and `README.md` exist. | Present |
| One team metadata CSV | `data/metadata.csv` exists and records the current team-number placeholder. | Present; assigned team number and member credits missing |
| Signed consent for every speaker and writer | Only a blank template and header-only `consent/consent_log.csv` exist. | **Missing** |
| 16 kHz mono WAV audio (bonus) | No audio files are in this project. The supplied external MP3 folder lacks transcripts and dialect labels. | Not included |
| JPEG images at least 1280 px | No image dataset is included; the converter is text-only. | Not included |
| UTF-8 Kannada text | Project CSVs are UTF-8; dataset validation reports schema/privacy/Unicode checks pass but collection targets are unmet. | Present |
| No personal contacts, songs, films, or book text | No speaker collection is present. Continue to enforce these rules when collecting. | No collected content to assess |
| Dataset source and license information | `data/source_manifest.csv` and the per-source notes document current origins, terms, and limitations. | Present; source dataset is not a trained model corpus |
| README explaining how it works and what it misses | `README.md` and `docs/limitations.md` cover the offline pipeline and limits. | Present |
| GitHub repository link (only submission route) | Published at `https://github.com/Srimanikanta2006/Nudi-Setu` on branch `main`. | Published |
| Demo video and dataset/source links on Google Drive | A current 45-second MP4 and poster are included at `assets/nudisetu_demo.mp4` and `assets/demo-poster.jpg`, linked from the repository README. No Google Drive links are present. | Video present; Drive upload/link still needed |
| Required folder layout `team_XX/problem_01/` | Current path is `team_XX/problem_01/`. `XX` is still a placeholder. | Layout present; replace team number |

## Validator result

`python tools/validate_dataset.py` was run against the current files. It reports **0/300 real rows** and 18 shortfall issues: 100 missing rows plus 20 missing rows in each of five topics for each of the three challenge dialects. It does not report schema or privacy errors. A nonzero result is expected until the real data targets are met.

## Submission route shown in the slides

1. Put the completed project in the correctly numbered `team_NN/problem_01/` folder.
2. Create and push the repository to GitHub. The hackathon accepts the GitHub repository link as the project submission.
3. Record a product demo, upload it to Google Drive, and include its share link where organizers request it.
4. Upload the permitted dataset source files and consent records to the team's Google Drive folder and include the source link. Keep provider licenses and consent with each file.
5. Before submission, make sure the repository README, dataset CSV, glossary CSV, team metadata CSV, and consent material are present. Do not claim the 300-row target or peer-review criteria as complete until verified.

## Human inputs still required

- Assigned team number and member credits.
- Adult speakers from each target dialect, voluntary original everyday sentences, and their completed consent forms; no local code can create these ethically.
- A second fluent reviewer for each textbook Kannada target, an external peer-review team and its review scores.
- Upload the included product demo and permitted dataset/source material to the team's Google Drive and add final read-only share links.

Deadline shown in the attached slide: **18 November 2026**. The current system date is also 18 November 2026, so check the organizer's submission portal immediately for any late-submission window.
