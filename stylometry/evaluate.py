"""Load the reference corpus and measure how well each method attributes unseen text."""

import json
from collections import defaultdict
from pathlib import Path

from .corpus import chunk_text, read_text
from .methods import METHODS


def load_config(path="references.json") -> dict:
    path = Path(path)
    config = json.loads(path.read_text(encoding="utf-8"))
    config["base"] = path.parent
    return config


def reference_chunks(config: dict, chunk_size: int) -> dict[str, list[tuple[str, list[str]]]]:
    """For every author: a list of (file, chunks) for each reference text."""
    out = defaultdict(list)
    for author, files in config["references"].items():
        for f in files:
            out[author].append((f, chunk_text(read_text(config["base"] / f), chunk_size)))
    return out


def train_samples(config: dict, chunk_size: int) -> list[tuple[str, str]]:
    return [
        (author, chunk)
        for author, texts in reference_chunks(config, chunk_size).items()
        for _, chunks in texts
        for chunk in chunks
    ]


def holdout_accuracy(config: dict, chunk_size: int = 2000, test_share: float = 0.3,
                     methods=None) -> dict[str, dict]:
    """
    Train on the first 70 % of every reference text, test on the last 30 %.

    The split is contiguous (not random), so test chunks never sit right next to a
    training chunk with the same scene or topic. This keeps the estimate honest.
    """
    train, test = [], []
    for author, texts in reference_chunks(config, chunk_size).items():
        for _, chunks in texts:
            if len(chunks) < 2:
                train += [(author, c) for c in chunks]
                continue
            cut = max(1, round(len(chunks) * (1 - test_share)))
            train += [(author, c) for c in chunks[:cut]]
            test += [(author, c) for c in chunks[cut:]]

    results = {}
    for name in methods or METHODS:
        model = METHODS[name]().fit(train)
        per_author = defaultdict(lambda: [0, 0])
        for author, chunk in test:
            per_author[author][1] += 1
            per_author[author][0] += model.predict(chunk) == author
        correct = sum(c for c, _ in per_author.values())
        results[name] = {
            "accuracy": correct / len(test),
            "per_author": {a: c / n for a, (c, n) in sorted(per_author.items())},
            "n_test": len(test),
        }
    return results


def test_file_predictions(config: dict, chunk_size: int = 2000, methods=None) -> dict:
    """Train on all reference texts and attribute the separate test files."""
    train = train_samples(config, chunk_size)
    models = {name: METHODS[name]().fit(train) for name in methods or METHODS}
    rows = []
    for item in config.get("tests", []):
        text = read_text(config["base"] / item["file"])
        rows.append({
            "file": item["file"],
            "author": item["author"],
            "predictions": {name: m.predict(text) for name, m in models.items()},
        })
    return rows
