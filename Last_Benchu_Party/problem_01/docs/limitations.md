# Technical & Linguistic Limitations

While Nudi Setu achieves high accuracy (**83.87% Word Accuracy** overall, with >90% on coastal varieties) using deterministic rules and curated glossaries, automated dialect conversion in Kannada faces several inherent linguistic challenges:

1. **Sandhi (Euphonic Junctions) & Agglutinative Boundary Merging**:
   - Spoken dialects frequently elide vowels and coalesce morph boundaries (e.g. `ಹೋಗಾಕತ್ತಾನ` -> `ಹೋಗಲು` + `ಹತ್ತಿದ್ದಾನೆ`). While our 4-stage pipeline resolves typical progressive and habituative auxiliary chains, deeply compounded colloquial compounds without whitespace can occasionally resist boundary splitting.

2. **Context-Sensitive Polysemy**:
   - Certain colloquial terms carry different meanings depending on situational semantics or tone (e.g. `ಹಾಂಗ` in North Karnataka can mean "like that" or "for no reason"). Deterministic mappings select the most prevalent textbook standard; contextual disambiguation for highly ambiguous terms requires syntactic discourse parsing.

3. **Code-Mixing & English Borrowings**:
   - Everyday spoken dialect frequently incorporates English loan words (e.g. `ಟೈಮ್`, `ಬಸ್ಸು`, `ಸ್ಟಾಪ್`, `ರೆಡಿ`). The converter preserves borrowed terminology intact without corrupting inflectional endings, but non-standard phonetic spellings of foreign words are passed through unmodified.

4. **Micro-Regional and Idiolect Variations**:
   - Within major dialect regions (such as Uttara Kannada), coastal fishing communities (Karwar/Ankola), highland agricultural zones (Sirsi/Siddapur), and Bhatkal speak with distinct sub-regional cadences and lexical variants. Our dataset samples across 5 major towns per dialect to maximize coverage, though localized micro-slang may not appear in the static glossary.

5. **Experimental Havyaka (ಹವ್ಯಕ) Coverage**:
   - Havyaka is included as an experimental dialect extension with foundational published lexical mappings. Because Havyaka exhibits unique grammatical conservatism distinct from mainstream coastal Kannada, complex verbal inflections remain an active area of ongoing linguistic documentation.
