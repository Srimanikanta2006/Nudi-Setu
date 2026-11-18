# Public-source Kannada pairs

These files contain separately attributed public-source examples. They are not speaker contributions, consented data, or part of the training/collection dataset. Each row needs native-speaker review before it is treated as a correct dialect conversion.

- `mangaluru_wikipedia.csv`: three Mangaluru examples based on the Kannada Wikipedia article [ಮಂಗಳೂರು ಕನ್ನಡ](https://kn.wikipedia.org/wiki/ಮಂಗಳೂರು_ಕನ್ನಡ), accessed 18 November 2026. Attribute to Wikipedia contributors; the article is available under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). The adapted examples retain that license and must be shared alike.
- `tv9_mangaluru.csv`: one minimal sentence pair paraphrased from a TV9 Kannada article that explicitly describes the Mangaluru use of `ಕೂಗುತ್ತಿದೆ` for a child crying. The source's copyright status is not verified; do not redistribute it as CC BY-SA or include it in the collected-data release without checking terms.

The converter uses these pairs only when the input exactly matches a public-source example. It does not fuzzy-match these pairs or treat them as training rows. An exact match still carries a native-review warning.
