# Copy-ready remote collection form

Use two Google Forms (or equivalent). Disable email collection, sign-in requirements, and automatic name capture. Do not request a phone number or address. Give each consenting adult a random code such as `S001`; keep consent records separate from sentence responses.

## Form 1 — Consent and speaker setup

**Description:** Nudi Setu is a student educational project that studies how everyday Kannada sentences vary by region and how to express the same meaning in textbook Kannada. Taking part is voluntary. Participants must be 18 or older. The form collects a pseudonymous code, self-described Kannada variety, optional town, broad age band, and separate text/audio consent choices. Do not enter names, email addresses, phone numbers, or home addresses. Read the full bilingual consent form before answering.

Add these required questions:

1. Are you 18 or older? — Yes / No. End the form for “No.”
2. Do you agree to participate and provide text sentences? — Yes / No. End the form for “No.”
3. Do you agree to publish your sentences and reviewed textbook Kannada versions under CC BY 4.0? — Yes / No. End the form for “No.”
4. Speaker code — short answer; assigned by the team, never the participant's name.
5. Which Kannada variety do you identify with? — Uttara Kannada / Mangaluru / Hubballi-Dharwad / another or unsure (free text). Keep “another/unsure” responses out of the three-target dataset until reviewed.
6. Town or area — short answer; if the participant declines, enter `not_provided` in the project CSV and never infer a town.
7. Age band — 18–25 / 26–40 / 41–60 / 60+.
8. Do you agree to an optional voice recording? — Yes / No.
9. If recorded, do you agree to public audio sharing under CC BY 4.0? — Yes / No.

Do not record a speaker in the project unless the recording-consent choice is “Yes.” Do not publish audio unless the audio-release choice is also “Yes.”

## Form 2 — One sentence per response

**Description:** Submit one sentence you would naturally say in your everyday Kannada. Do not copy a sentence from a movie, song, book, website, or the examples below. Submit as many responses as you like. Skip anything you do not want to answer.

Add these required questions:

1. Speaker code — short answer, matching Form 1.
2. Kannada variety — same options as Form 1.
3. Town or area — use the speaker's own description; if declined, enter `not_provided` and do not infer it.
4. Topic — Home / Market / School / Travel / Festivals.
5. Write one original sentence exactly as you naturally say it — paragraph; Kannada script preferred.

Use neutral situations to prompt original wording, one at a time: inviting someone to eat; asking the price of an item; asking when a bus leaves; telling someone you are going home; inviting someone to a festival. Do not show a generated dialect sentence to copy. The speaker supplies only their natural sentence. A separate fluent reviewer adds `standard_text` and records their reviewer code.

## Add the returned responses to Nudi Setu

Map each sentence response to `dialect,town,dialect_text,standard_text,age_band,sentence_id,topic,speaker_id,synthetic,verified_by,source,audio_file` in `tools/collect_template.csv`. Set `synthetic=false`, `source=collected`, and a unique `sentence_id`; leave `audio_file` empty unless separately consented audio is collected. Copy consent choices into `consent/consent_log.csv`, not into the public dataset. The age band and dialect in the log must match the sentence row.

Ask a second fluent Kannada reviewer to check each textbook version and meaning before running `python tools/validate_dataset.py`. The Kannada consent wording is a draft; have a fluent local speaker check it before sharing the form.
