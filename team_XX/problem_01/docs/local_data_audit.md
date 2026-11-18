# Audit of locally supplied data

Reviewed 18 November 2026. This note describes resources present on the development machine; it does not claim that they are included in the submission or that their usage rights have been cleared.

## Indian Languages Audio Dataset

- Local folder supplied by the team: `Downloads/archive (1)/Indian_Languages_Audio_Dataset/Kannada`.
- Local inventory: 1,000 `.mp3` files. The folder contains numeric filenames and no transcripts, speaker IDs, town labels, dialect labels, topic labels, consent records, or per-file source URLs.
- The Kaggle dataset is described in a published paper as five-second audio segments drawn from regional YouTube videos. See the [Kaggle dataset page](https://www.kaggle.com/datasets/hmsolanki/indian-languages-audio-dataset) and [paper describing the dataset](https://link.springer.com/article/10.1007/s00034-024-02733-y).
- Possible use: manually selected, permission-cleared clips for an audio upload/player or speech-processing demonstration, if licensing and source attribution are established.
- Not suitable as-is for Nudi Setu's 300 dialect-to-standard sentence pairs: there is no transcript to align, no dialect/town identity, no topic, no reviewer, and no Nudi Setu-specific participant consent. Do not transcribe and relabel clips as Uttara Kannada, Mangaluru, or Hubballi-Dharwad based on inference. Do not copy these clips into `data/audio` or redistribute them until the Kaggle terms and underlying YouTube rights have been checked.

## Kannada Text Corpus

The separately supplied Kannada Text Corpus is used only by `tools/evaluate_written_kannada_baseline.py` for aggregate text-preservation checks. It is general written Kannada, not target-dialect text; its licensing notes are in the README. It does not supply dialect-to-standard pairs and is not counted in the dataset target.

## OpenSLR SLR79 transcript indexes

The supplied indexes remain in `data/public_sources/openslr79/`, with attribution and license notes in that folder. They provide general Kannada read-speech transcripts, without the target dialect/town labels or Nudi Setu-specific consent required for the conversion dataset.
