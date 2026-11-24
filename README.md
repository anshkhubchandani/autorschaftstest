# Autorschaftstest – stylometric authorship attribution (Python)

Who wrote this text? The tool compares an unknown German text with reference works by Goethe, Schiller,
Eichendorff, Thomas Mann, Wittgenstein, Busoni and Joyce and ranks the most likely authors.

> Started as the final project of *Algorithmic Foundations in Python* (FSU Jena, team project).
> **Version 2** is a rewrite of the attribution method with an evaluation. The original course solution is kept in
> [`legacy/`](legacy/) and used as the baseline.

## Results

Evaluated on unseen text: each reference work is split into 2,000-word chunks; methods are trained on the
first 70 % of every work and tested on the last 30 % (64 test chunks, 7 authors, chance level ≈ 14 %).

| Method | Accuracy |
|---|---|
| **Burrows' Delta** (150 most frequent words) | **89.1 %** |
| Cosine Delta | 85.9 % |
| Character 3-grams | 82.8 % |
| Original 5 features, z-scored | 59.4 % |
| Original course solution (hand-weighted 5 features) | 7.8 % |

Separate test excerpts (*Faust*, *Italienische Reise*, Schiller letters): all three are attributed correctly
by every word- and character-based method; the original solution got one of three right.

## What changed compared with the course version

| Problem in v1 | Fix in v2 |
|---|---|
| Only 5 global features (word length, TTR, …) – too little signal | **Burrows' Delta** on the most frequent words. Function words (*und, der, nicht, sich* …) are used unconsciously and independent of topic – the standard signal in stylometry |
| Features on different scales combined with hand-picked weights (11, 33, 50, 0.4, 4) | **z-score normalization** learned from the reference corpus, no magic numbers |
| Type-token ratio depends on text length, so short and long texts are not comparable | **Equal-sized chunks** and **MATTR** (moving-average TTR) |
| One reference signature per author | Many chunks per author → robust author profiles and a measurable accuracy |
| No evaluation | Hold-out **evaluation** of all methods against the original baseline |
| English Project Gutenberg licence text counted as part of the books | Gutenberg header and footer are **stripped** |
| Naive tokenizer, O(n²) word counting, file encoding not set | Unicode-aware regex tokenizer, `Counter`, explicit UTF-8 |
| Hard-coded file names, interactive `input()` | **Command-line interface**, corpus defined in `references.json` |
| Goethe split into two "authors" by work | References grouped **per author** |

## Usage
No external dependencies – Python 3.10+ standard library only.

```bash
python -m stylometry identify texte/faust-test.txt            # rank the most likely authors
python -m stylometry identify my_text.txt --method delta --top 5
python -m stylometry features texte/faust-test.txt            # the classic style features
python -m stylometry evaluate                                 # reproduce the table above
python -m unittest discover tests                             # run the tests
```

Example:
```
Text: texte/faust-test.txt (11,388 words) – method: cosine-delta

Rank  Author            Distance
1     Goethe               0.094
2     Eichendorff          0.237
3     Schiller             0.260

Most likely author: Goethe (margin to 2nd place 60%, clear)
```

To add authors, put their texts in `texte/` and list them in `references.json`.

## Project structure
```
stylometry/corpus.py     reading, Gutenberg stripping, tokenizing, sentence splitting, chunking
stylometry/features.py   classic features, MATTR, word and character n-gram frequencies
stylometry/methods.py    baseline, classic-z, Burrows' Delta, Cosine Delta, character n-grams
stylometry/evaluate.py   hold-out evaluation and test-file predictions
stylometry/__main__.py   command-line interface
tests/                   unit tests
legacy/                  original course solution
```

## Limitations
- The Schiller reference (*Briefe Schillers und Goethes an A. W. Schlegel*) also contains letters by Goethe,
  so the Schiller profile is partly mixed.
- The Wittgenstein reference contains German and English text (bilingual edition).
- Texts below ~1,000 words cannot be attributed reliably; the tool warns about this.
- `texte/autor1.txt` is a short excerpt that also appears in the Busoni reference, so it is not used for evaluation.

## Tech
Python · stylometry · Burrows' Delta · z-scores · cosine distance · n-grams · unittest
