"""Reading, cleaning, tokenizing and chunking of texts."""

import re
import unicodedata
from pathlib import Path

# Project Gutenberg wraps every book in a long English licence text.
# It must be removed, otherwise all Gutenberg books look alike.
_GUTENBERG_START = re.compile(
    r"\*\*\*\s*START OF (?:THE|THIS) PROJECT GUTENBERG[^\n]*\*\*\*"
    r"|\*END\*THE SMALL PRINT[^\n]*",
    re.IGNORECASE,
)
_GUTENBERG_END = re.compile(
    r"\*\*\*\s*END OF (?:THE|THIS) PROJECT GUTENBERG"
    r"|End of (?:the )?Project Gutenberg",
    re.IGNORECASE,
)

# A word is a run of letters (incl. ä, ö, ü, ß, accents), optionally with an apostrophe.
_WORD = re.compile(r"[^\W\d_]+(?:['’][^\W\d_]+)?")
# Sentence boundary: ., ! or ? (possibly repeated) followed by whitespace.
_SENTENCE_END = re.compile(r"(?<=[.!?])[\"»«“”')\]]*\s+")
_CLAUSE_MARK = re.compile(r"[,;:]")


def strip_gutenberg(text: str) -> str:
    """Remove Project Gutenberg header and licence footer if present."""
    start = _GUTENBERG_START.search(text)
    if start:
        text = text[start.end():]
    end = _GUTENBERG_END.search(text)
    if end:
        text = text[:end.start()]
    return text


def normalize(text: str) -> str:
    """Unicode-normalize, unify dashes/whitespace and drop stage-direction underscores."""
    text = unicodedata.normalize("NFC", text)
    text = text.replace("﻿", "")
    text = text.replace("--", " – ").replace("_", " ")
    return re.sub(r"\s+", " ", text).strip()


def read_text(path) -> str:
    """Read a UTF-8 text file (with or without BOM) and return the cleaned text."""
    raw = Path(path).read_text(encoding="utf-8-sig", errors="replace")
    return normalize(strip_gutenberg(raw))


def tokenize(text: str) -> list[str]:
    """Lower-cased word tokens."""
    return _WORD.findall(text.lower())


def split_sentences(text: str) -> list[str]:
    """Split a text into non-empty sentences."""
    return [s.strip() for s in _SENTENCE_END.split(text) if _WORD.search(s)]


def count_clauses(sentence: str) -> int:
    """Number of clauses, approximated by punctuation that separates clauses."""
    return 1 + len(_CLAUSE_MARK.findall(sentence))


def chunk_text(text: str, size: int = 2000) -> list[str]:
    """
    Cut a text into consecutive chunks of about `size` words, at sentence boundaries.

    Equal-sized chunks make length-dependent measures (type-token ratio, hapax ratio)
    comparable and give several samples per author instead of one.
    A final chunk shorter than half the size is dropped.
    """
    chunks, current, n_words = [], [], 0
    for sentence in split_sentences(text):
        current.append(sentence)
        n_words += len(tokenize(sentence))
        if n_words >= size:
            chunks.append(" ".join(current))
            current, n_words = [], 0
    if current and n_words >= size // 2:
        chunks.append(" ".join(current))
    return chunks
