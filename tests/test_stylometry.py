"""Unit tests. Run with:  python -m unittest discover tests   (or: pytest)"""

import random
import unittest

from stylometry.corpus import chunk_text, split_sentences, strip_gutenberg, tokenize
from stylometry.features import classic_features, mattr
from stylometry.methods import METHODS


class TestCorpus(unittest.TestCase):
    def test_tokenize_keeps_umlauts_and_drops_punctuation(self):
        self.assertEqual(tokenize("Größe, Mühle! Straße?"), ["größe", "mühle", "straße"])

    def test_split_sentences(self):
        self.assertEqual(len(split_sentences("Ein Satz. Noch einer! Und ein dritter?")), 3)

    def test_strip_gutenberg(self):
        raw = ("The Project Gutenberg EBook of X\nlicence...\n"
               "*** START OF THIS PROJECT GUTENBERG EBOOK X ***\nDer eigentliche Text.\n"
               "*** END OF THIS PROJECT GUTENBERG EBOOK X ***\nmore licence")
        self.assertEqual(strip_gutenberg(raw).strip(), "Der eigentliche Text.")

    def test_chunks_have_requested_size(self):
        text = " ".join(f"Das ist Satz {i} mit einigen Wörtern." for i in range(300))
        chunks = chunk_text(text, size=200)
        self.assertGreater(len(chunks), 3)
        for c in chunks:
            self.assertGreaterEqual(len(tokenize(c)), 100)


class TestFeatures(unittest.TestCase):
    def test_mattr_equals_ttr_for_short_text(self):
        tokens = ["a", "b", "a", "c"]
        self.assertAlmostEqual(mattr(tokens, window=10), 3 / 4)

    def test_mattr_independent_of_length(self):
        random.seed(0)
        vocab = [f"w{i}" for i in range(300)]
        short = random.choices(vocab, k=2000)
        long = random.choices(vocab, k=20000)
        self.assertAlmostEqual(mattr(short), mattr(long), delta=0.02)

    def test_classic_features(self):
        f = classic_features("Der Hund bellt, die Katze schläft. Der Vogel singt.")
        self.assertAlmostEqual(f["words_per_sentence"], 4.5)
        self.assertAlmostEqual(f["clauses_per_sentence"], 1.5)


class TestMethods(unittest.TestCase):
    """Two synthetic 'authors' with different function-word habits."""

    @staticmethod
    def _author_text(style_words, seed, n=600):
        rng = random.Random(seed)
        content = ["Haus", "Baum", "Weg", "Licht", "Stadt", "Feld"]
        sentences = []
        for _ in range(n // 8):
            words = rng.choices(style_words, k=5) + rng.choices(content, k=3)
            rng.shuffle(words)
            sentences.append(" ".join(words) + ".")
        return " ".join(sentences)

    def setUp(self):
        a = ["und", "der", "die", "nicht", "sich"]
        b = ["aber", "doch", "wohl", "ja", "eben"]
        self.train = [("A", self._author_text(a, s)) for s in range(5)] + \
                     [("B", self._author_text(b, s + 100)) for s in range(5)]
        self.unknown_a = self._author_text(a, 999)
        self.unknown_b = self._author_text(b, 998)

    def test_word_based_methods_separate_function_word_styles(self):
        # The classic features (word length, sentence length, ...) cannot see
        # function-word habits by design, so only the frequency-based methods are tested here.
        for name in ("delta", "cosine-delta", "char-ngrams"):
            with self.subTest(method=name):
                model = METHODS[name]().fit(self.train)
                self.assertEqual(model.predict(self.unknown_a), "A")
                self.assertEqual(model.predict(self.unknown_b), "B")

    def test_classic_z_separates_sentence_length_styles(self):
        rng = random.Random(1)
        words = ["und", "der", "Haus", "Weg", "nicht", "Licht", "Stadt", "sich"]

        def text(sentence_len, n=80):
            return " ".join(" ".join(rng.choices(words, k=sentence_len)) + "." for _ in range(n))

        train = [("Short", text(5)) for _ in range(4)] + [("Long", text(25)) for _ in range(4)]
        model = METHODS["classic-z"]().fit(train)
        self.assertEqual(model.predict(text(5)), "Short")
        self.assertEqual(model.predict(text(25)), "Long")


if __name__ == "__main__":
    unittest.main()
