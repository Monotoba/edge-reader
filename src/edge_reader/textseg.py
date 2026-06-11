from __future__ import annotations

import re
from dataclasses import replace

from .models import SentenceSpan

# Common abbreviations that should not usually terminate a sentence.
_ABBREVIATIONS = {
    "mr.", "mrs.", "ms.", "dr.", "prof.", "sr.", "jr.", "st.", "mt.", "ft.",
    "vs.", "etc.", "e.g.", "i.e.", "fig.", "eq.", "no.", "inc.", "ltd.", "co.",
    "u.s.", "u.k.", "a.m.", "p.m.",
}
_TERMINATORS = set(".!?…")
_CLOSERS = set('"\'”’)]}')


def normalize_document_text(text: str) -> str:
    """Normalize line endings and collapse excessive blank lines without destroying offsets too much."""
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+\n", "\n", text)
    text = re.sub(r"\n{4,}", "\n\n\n", text)
    return text


def _previous_token_lower(text: str, dot_index: int) -> str:
    start = dot_index
    while start > 0 and (text[start - 1].isalpha() or text[start - 1] == "."):
        start -= 1
    return text[start : dot_index + 1].lower()


def _looks_like_decimal(text: str, index: int) -> bool:
    return (
        text[index] == "."
        and index > 0
        and index + 1 < len(text)
        and text[index - 1].isdigit()
        and text[index + 1].isdigit()
    )


def _is_abbreviation(text: str, index: int) -> bool:
    return text[index] == "." and _previous_token_lower(text, index) in _ABBREVIATIONS


def _next_nonspace(text: str, index: int) -> int | None:
    j = index
    while j < len(text) and text[j].isspace():
        j += 1
    return j if j < len(text) else None


def split_sentences(text: str, *, min_chunk_chars: int = 1, max_chunk_chars: int = 900) -> list[SentenceSpan]:
    """Split display text into sentence spans.

    This is deliberately dependency-free. It is not a full natural-language parser, but it handles
    common prose, abbreviations, decimal values, quoted sentence endings, and documents with weak
    punctuation. Long spans are further split on paragraph/line boundaries so edge-tts calls stay
    manageable.
    """
    text = normalize_document_text(text)
    spans: list[SentenceSpan] = []
    start = 0
    i = 0
    n = len(text)

    while i < n:
        char = text[i]
        should_end = False

        if char in _TERMINATORS and not _looks_like_decimal(text, i) and not _is_abbreviation(text, i):
            end = i + 1
            while end < n and text[end] in _CLOSERS:
                end += 1
            next_i = _next_nonspace(text, end)
            if next_i is None:
                should_end = True
            else:
                # End at whitespace after punctuation. This avoids splitting URLs and initials.
                should_end = end < n and text[end].isspace()
        elif char == "\n" and i + 1 < n and text[i + 1] == "\n":
            # Paragraph break fallback for headings, lists, and OCR-ish text.
            should_end = True
            end = i
        elif i - start >= max_chunk_chars and char in {"\n", ";", ":", ","}:
            should_end = True
            end = i + 1

        if should_end:
            raw_start = start
            raw_end = end
            while raw_start < raw_end and text[raw_start].isspace():
                raw_start += 1
            while raw_end > raw_start and text[raw_end - 1].isspace():
                raw_end -= 1
            if raw_end - raw_start >= min_chunk_chars:
                spans.append(SentenceSpan(len(spans), raw_start, raw_end, text[raw_start:raw_end]))
            start = end
            while start < n and text[start].isspace():
                start += 1
            i = start
            continue

        i += 1

    raw_start = start
    raw_end = n
    while raw_start < raw_end and text[raw_start].isspace():
        raw_start += 1
    while raw_end > raw_start and text[raw_end - 1].isspace():
        raw_end -= 1
    if raw_end - raw_start >= min_chunk_chars:
        spans.append(SentenceSpan(len(spans), raw_start, raw_end, text[raw_start:raw_end]))

    if not spans and text.strip():
        start = text.index(text.strip()[0])
        end = start + len(text.strip())
        spans.append(SentenceSpan(0, start, end, text[start:end]))

    return [replace(span, index=i) for i, span in enumerate(spans)]
