"""
Command-line interface.

    python -m stylometry identify texte/faust-test.txt
    python -m stylometry identify mein_text.txt --method delta --top 5
    python -m stylometry features texte/autor1.txt
    python -m stylometry evaluate
"""

import argparse
import sys

from .corpus import read_text, tokenize
from .evaluate import holdout_accuracy, load_config, test_file_predictions, train_samples
from .features import CLASSIC_FEATURES, classic_features
from .methods import DEFAULT_METHOD, METHODS


def cmd_identify(args):
    config = load_config(args.config)
    text = read_text(args.file)
    n_words = len(tokenize(text))
    if n_words < 500:
        print(f"Warning: only {n_words} words. Attribution below ~1,000 words is unreliable.\n",
              file=sys.stderr)

    model = METHODS[args.method]().fit(train_samples(config, args.chunk_size))
    ranking = model.rank(text)

    print(f"Text: {args.file} ({n_words:,} words) – method: {args.method}\n")
    print(f"{'Rank':<6}{'Author':<16}{'Distance':>10}")
    for i, (author, dist) in enumerate(ranking[:args.top], 1):
        print(f"{i:<6}{author:<16}{dist:>10.3f}")

    (best, d1), (_, d2) = ranking[0], ranking[1]
    margin = (d2 - d1) / d2 if d2 else 0.0
    verdict = "clear" if margin >= 0.15 else "uncertain"
    print(f"\nMost likely author: {best} (margin to 2nd place {margin:.0%}, {verdict})")


def cmd_features(args):
    feats = classic_features(read_text(args.file))
    for name in CLASSIC_FEATURES:
        print(f"{name:<22}{feats[name]:.3f}")


def cmd_evaluate(args):
    config = load_config(args.config)
    print(f"Hold-out evaluation (train: first 70 % of each text, test: last 30 %, "
          f"chunks of {args.chunk_size} words)\n")
    results = holdout_accuracy(config, args.chunk_size)
    print(f"{'Method':<15}{'Accuracy':>10}")
    for name, r in sorted(results.items(), key=lambda kv: -kv[1]["accuracy"]):
        print(f"{name:<15}{r['accuracy']:>10.1%}")
    print(f"\n({next(iter(results.values()))['n_test']} test chunks)\n")

    print("Separate test files (trained on all reference texts)\n")
    rows = test_file_predictions(config, args.chunk_size)
    names = list(METHODS)
    print(f"{'File':<42}{'True':<10}" + "".join(f"{n:<14}" for n in names))
    for row in rows:
        cells = "".join(
            f"{('✓ ' if row['predictions'][n] == row['author'] else '✗ ') + row['predictions'][n]:<14}"
            for n in names
        )
        print(f"{row['file']:<42}{row['author']:<10}{cells}")


def main(argv=None):
    parser = argparse.ArgumentParser(prog="stylometry", description="Authorship attribution.")
    parser.add_argument("--config", default="references.json", help="reference corpus definition")
    parser.add_argument("--chunk-size", type=int, default=2000, help="words per training chunk")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("identify", help="attribute an unknown text")
    p.add_argument("file")
    p.add_argument("--method", choices=METHODS, default=DEFAULT_METHOD)
    p.add_argument("--top", type=int, default=3)
    p.set_defaults(func=cmd_identify)

    p = sub.add_parser("features", help="show the classic style features of a text")
    p.add_argument("file")
    p.set_defaults(func=cmd_features)

    p = sub.add_parser("evaluate", help="compare all methods on held-out data")
    p.set_defaults(func=cmd_evaluate)

    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()
