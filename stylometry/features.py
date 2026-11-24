"""Stylometric features of a text."""

from collections import Counter

from .corpus import count_clauses, split_sentences, tokenize

CLASSIC_FEATURES = [
    "mean_word_length",
    "mattr",
    "hapax_ratio",
    "words_per_sentence",
    "clauses_per_sentence",
]


def mattr(tokens: list[str], window: int = 500) -> float:
    """
    Moving-average type-token ratio.

    The plain TTR falls with text length, so texts of different length are not
    comparable. MATTR averages the TTR over a sliding window of fixed size.
    """
    if not tokens:
        return 0.0
    if len(tokens) <= window:
        return len(set(tokens)) / len(tokens)
    counts = Counter(tokens[:window])
    total = len(counts)
    for i in range(window, len(tokens)):
        old, new = tokens[i - window], tokens[i]
        counts[old] -= 1
        if counts[old] == 0:
            del counts[old]
        counts[new] += 1
        total += len(counts)
    return total / ((len(tokens) - window + 1) * window)


def classic_features(text: str) -> dict[str, float]:
    """The five features of the original program, made robust against text length."""
    tokens = tokenize(text)
    sentences = split_sentences(text) or [text]
    counts = Counter(tokens)
    n = len(tokens) or 1
    return {
        "mean_word_length": sum(len(t) for t in tokens) / n,
        "mattr": mattr(tokens),
        "hapax_ratio": sum(1 for c in counts.values() if c == 1) / n,
        "words_per_sentence": n / len(sentences),
        "clauses_per_sentence": sum(count_clauses(s) for s in sentences) / len(sentences),
    }


def word_frequencies(text: str) -> dict[str, float]:
    """Relative frequency of every word."""
    tokens = tokenize(text)
    n = len(tokens) or 1
    return {w: c / n for w, c in Counter(tokens).items()}


def char_ngram_frequencies(text: str, n: int = 3) -> dict[str, float]:
    """Relative frequency of character n-grams (spaces included, case folded)."""
    s = " " + " ".join(tokenize(text)) + " "
    grams = Counter(s[i:i + n] for i in range(len(s) - n + 1))
    total = sum(grams.values()) or 1
    return {g: c / total for g, c in grams.items()}
