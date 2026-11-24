"""
Attribution methods.

Every method is trained on labelled text chunks (author, text) and then ranks the
authors for an unknown text by distance: the smallest distance is the best match.
"""

import math
from collections import Counter, defaultdict
from statistics import mean, pstdev

from .features import (
    CLASSIC_FEATURES,
    char_ngram_frequencies,
    classic_features,
    word_frequencies,
)
from .corpus import count_clauses, split_sentences, tokenize


# ---------------------------------------------------------------- helpers

def _zscore_fit(vectors: list[list[float]]) -> tuple[list[float], list[float]]:
    columns = list(zip(*vectors))
    means = [mean(col) for col in columns]
    stds = [pstdev(col) or 1.0 for col in columns]
    return means, stds


def _zscore(vector, means, stds) -> list[float]:
    return [(v - m) / s for v, m, s in zip(vector, means, stds)]


def _centroids(labels: list[str], vectors: list[list[float]]) -> dict[str, list[float]]:
    by_author = defaultdict(list)
    for label, vec in zip(labels, vectors):
        by_author[label].append(vec)
    return {a: [mean(col) for col in zip(*vecs)] for a, vecs in by_author.items()}


def _manhattan(a, b) -> float:
    return sum(abs(x - y) for x, y in zip(a, b)) / len(a)


def _cosine_distance(a, b) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    norm = math.sqrt(sum(x * x for x in a)) * math.sqrt(sum(y * y for y in b))
    return 1.0 - dot / norm if norm else 1.0


class Method:
    name = "method"

    def fit(self, samples: list[tuple[str, str]]) -> "Method":
        raise NotImplementedError

    def rank(self, text: str) -> list[tuple[str, float]]:
        raise NotImplementedError

    def predict(self, text: str) -> str:
        return self.rank(text)[0][0]


# ---------------------------------------------------------------- methods

class WeightedBaseline(Method):
    """
    The original course solution: five features of the whole text,
    compared with fixed hand-picked weights. Kept as a baseline.
    """

    name = "baseline"
    weights = [11, 33, 50, 0.4, 4]

    @staticmethod
    def _signature(text: str) -> list[float]:
        tokens = tokenize(text)
        sentences = split_sentences(text) or [text]
        counts = Counter(tokens)
        n = len(tokens) or 1
        return [
            sum(len(t) for t in tokens) / n,
            len(counts) / n,  # plain TTR: depends on text length
            sum(1 for c in counts.values() if c == 1) / n,
            n / len(sentences),
            sum(count_clauses(s) for s in sentences) / len(sentences),
        ]

    def fit(self, samples):
        texts = defaultdict(list)
        for author, text in samples:
            texts[author].append(text)
        self.profiles = {a: self._signature(" ".join(t)) for a, t in texts.items()}
        return self

    def rank(self, text):
        sig = self._signature(text)
        scores = {
            a: sum(w * abs(x - y) for w, x, y in zip(self.weights, sig, prof))
            for a, prof in self.profiles.items()
        }
        return sorted(scores.items(), key=lambda kv: kv[1])


class ClassicZ(Method):
    """Same five features, but z-scored on the training chunks instead of hand weights."""

    name = "classic-z"

    def fit(self, samples):
        labels = [a for a, _ in samples]
        raw = [[classic_features(t)[f] for f in CLASSIC_FEATURES] for _, t in samples]
        self.means, self.stds = _zscore_fit(raw)
        z = [_zscore(v, self.means, self.stds) for v in raw]
        self.profiles = _centroids(labels, z)
        return self

    def rank(self, text):
        feats = classic_features(text)
        v = _zscore([feats[f] for f in CLASSIC_FEATURES], self.means, self.stds)
        return sorted(((a, _manhattan(v, p)) for a, p in self.profiles.items()),
                      key=lambda kv: kv[1])


class BurrowsDelta(Method):
    """
    Burrows' Delta (2002): z-scored relative frequencies of the most frequent words.

    The most frequent words are mostly function words (und, der, nicht, sich, ...).
    Authors use them unconsciously and consistently, independent of topic,
    which makes them the standard signal in stylometry.
    """

    name = "delta"

    def __init__(self, mfw: int = 150):
        self.mfw = mfw

    def _distance(self, a, b):
        return _manhattan(a, b)

    def fit(self, samples):
        labels = [a for a, _ in samples]
        freqs = [word_frequencies(t) for _, t in samples]
        total = Counter()
        for f in freqs:
            total.update(f)
        self.vocabulary = [w for w, _ in total.most_common(self.mfw)]
        raw = [[f.get(w, 0.0) for w in self.vocabulary] for f in freqs]
        self.means, self.stds = _zscore_fit(raw)
        z = [_zscore(v, self.means, self.stds) for v in raw]
        self.profiles = _centroids(labels, z)
        return self

    def rank(self, text):
        f = word_frequencies(text)
        v = _zscore([f.get(w, 0.0) for w in self.vocabulary], self.means, self.stds)
        return sorted(((a, self._distance(v, p)) for a, p in self.profiles.items()),
                      key=lambda kv: kv[1])


class CosineDelta(BurrowsDelta):
    """Cosine Delta (Smith & Aldridge 2011): same features, cosine distance. Usually more robust."""

    name = "cosine-delta"

    def _distance(self, a, b):
        return _cosine_distance(a, b)


class CharNgrams(Method):
    """Profiles of the most frequent character 3-grams, compared by cosine distance."""

    name = "char-ngrams"

    def __init__(self, n: int = 3, top: int = 1000):
        self.n, self.top = n, top

    def fit(self, samples):
        labels = [a for a, _ in samples]
        freqs = [char_ngram_frequencies(t, self.n) for _, t in samples]
        total = Counter()
        for f in freqs:
            total.update(f)
        self.vocabulary = [g for g, _ in total.most_common(self.top)]
        raw = [[f.get(g, 0.0) for g in self.vocabulary] for f in freqs]
        self.means, self.stds = _zscore_fit(raw)
        z = [_zscore(v, self.means, self.stds) for v in raw]
        self.profiles = _centroids(labels, z)
        return self

    def rank(self, text):
        f = char_ngram_frequencies(text, self.n)
        v = _zscore([f.get(g, 0.0) for g in self.vocabulary], self.means, self.stds)
        return sorted(((a, _cosine_distance(v, p)) for a, p in self.profiles.items()),
                      key=lambda kv: kv[1])


METHODS = {
    m.name: m
    for m in (WeightedBaseline, ClassicZ, BurrowsDelta, CosineDelta, CharNgrams)
}
DEFAULT_METHOD = "cosine-delta"
