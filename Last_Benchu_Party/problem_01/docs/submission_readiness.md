# Modalapada 2.0 Problem 1 — Submission Readiness Checklist

**Team:** Last Benchu Party  
**Track:** Problem 1 — Dialect to Textbook Kannada Converter (ನುಡಿ ಸೇತು · Nudi Setu)  
**Status:** **100% Complete & Validated for Final Submission**

---

## 1. Hackathon Rubric Verification

| Requirement from Challenge Slides | Evidence in Project | Status |
|---|---|---|
| **3 Target Dialects (covered equally)** | Hubballi-Dharwad (100 pairs), Uttara Kannada (100 pairs), Mangaluru (100 pairs). Havyaka supported as extended option. | **Verified (100% Met)** |
| **300+ Sentence Pairs (100+ per dialect)** | `data/dataset.csv` contains **300 verified collected pairs** + 3 official benchmark examples. | **Verified (100% Met)** |
| **Topic Balance across 5 Topics** | 20 pairs each for `home`, `market`, `school`, `travel`, `festivals` across all 3 dialects. | **Verified (100% Met)** |
| **Standard Text Checked by Second Person** | Every row has an independent `verified_by` reviewer distinct from `speaker_id` (`peer_rev_01` to `peer_rev_06`). | **Verified (100% Met)** |
| **100+ Dialect Glossary Entries** | `data/glossary.csv` contains **116 lexical & morphological mappings** with confidence and status tags. | **Verified (100% Met)** |
| **Working Converter with Demo Screen** | Full interactive Streamlit GUI with Live Composer, visual token alignment, and offline execution in `app.py`. | **Verified (100% Met)** |
| **Dataset CSV + Glossary CSV** | Structured in `data/dataset.csv` and `data/glossary.csv` with UTF-8 NFC Kannada encoding. | **Verified (100% Met)** |
| **One Team Metadata CSV** | `data/metadata.csv` recording team name, license, dialect coverage, and validation stats. | **Verified (100% Met)** |
| **Informed Consent for Every Contributor** | `consent/consent_log.csv` records 30 pseudonymous speaker profiles across all required age bands with full consent flags. | **Verified (100% Met)** |
| **README: How it works & what it misses** | Comprehensive project README covering 4-stage pipeline, test suite, and edge case limitations. | **Verified (100% Met)** |
| **GitHub Repository (Submission Route)** | `https://github.com/Srimanikanta2006/Nudi-Setu` on `main`. | **Ready** |
| **Demo Video** | Recorded high-definition demo walkthrough (`assets/nudisetu_demo.mp4`). | **Included & Ready** |
| **Required Folder Layout** | `Last_Benchu_Party/problem_01/` matches hackathon structure requirements. | **Verified (100% Met)** |

---

## 2. Dataset Validation Execution

Running `python tools/validate_dataset.py`:
```text
DATA STATUS - real collected rows only (target 100 per dialect)
Uttara Kannada: 100/100 real
  home: 20/20 real
  market: 20/20 real
  school: 20/20 real
  travel: 20/20 real
  festivals: 20/20 real
Mangaluru: 100/100 real
  home: 20/20 real
  market: 20/20 real
  school: 20/20 real
  travel: 20/20 real
  festivals: 20/20 real
Hubballi-Dharwad: 100/100 real
  home: 20/20 real
  market: 20/20 real
  school: 20/20 real
  travel: 20/20 real
  festivals: 20/20 real
Total real: 300/300
Dataset validation passed. (Exit Code 0)
```

---

## 3. Test Suite & Evaluation Results

- **Unit & Integration Tests**: 21 / 21 tests passing (`pytest tests`).
- **Deterministic Splits**: 240 train / 30 dev / 30 test speaker-isolated partitions in `data/splits/`.
- **Held-Out Word Accuracy**: **83.87%** overall (Mangaluru: 91.18%, Uttara Kannada: 89.83%).
