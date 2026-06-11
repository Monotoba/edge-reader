from __future__ import annotations

import asyncio
import json
import shutil
from pathlib import Path
from typing import Any

from .bundle import create_workdir, pack_bundle, write_document_text, write_manifest, write_timings
from .models import SentenceSpan, VoiceInfo


def rate_percent_to_edge(rate_percent: int) -> str:
    """Convert an integer percent to the edge-tts rate format, e.g. +10% or -20%."""
    rate_percent = max(-90, min(200, int(rate_percent)))
    return f"{rate_percent:+d}%"


def _event_to_ms(value: Any) -> int:
    """edge-tts offsets/durations are 100 ns units in current releases."""
    try:
        return int(round(int(value) / 10_000))
    except Exception:
        return 0


async def list_edge_voices() -> list[VoiceInfo]:
    import edge_tts

    voices = await edge_tts.list_voices()
    infos = [VoiceInfo.from_edge_dict(v) for v in voices]
    infos = [v for v in infos if v.short_name]
    infos.sort(key=lambda v: (v.locale, v.short_name))
    return infos


async def synthesize_sentence_to_file(
    *,
    text: str,
    voice: str,
    rate: str,
    audio_path: Path,
) -> list[dict[str, Any]]:
    """Synthesize one sentence and return API sync events in millisecond units."""
    import edge_tts

    text = text.strip()
    if not text:
        raise ValueError("Cannot synthesize empty text")

    events: list[dict[str, Any]] = []
    audio_path.parent.mkdir(parents=True, exist_ok=True)

    communicate = edge_tts.Communicate(text, voice=voice, rate=rate)
    with audio_path.open("wb") as audio_file:
        async for chunk in communicate.stream():
            kind = chunk.get("type")
            if kind == "audio":
                audio_file.write(chunk["data"])
            elif kind in {"WordBoundary", "SentenceBoundary"}:
                events.append(
                    {
                        "type": kind,
                        "offset_ms": _event_to_ms(chunk.get("offset", 0)),
                        "duration_ms": _event_to_ms(chunk.get("duration", 0)),
                        "text": str(chunk.get("text", "")),
                    }
                )
    return events


async def synthesize_bundle(
    *,
    document_text: str,
    title: str,
    source_name: str,
    sentences: list[SentenceSpan],
    voice: str,
    locale: str,
    rate_percent: int,
    output_bundle: str | Path,
    progress_cb: Any | None = None,
    cancel_event: asyncio.Event | None = None,
) -> Path:
    """Generate an offline replay bundle.

    The bundle stores one MP3 per display sentence. This avoids long-document service limits,
    gives exact sentence-level highlighting during replay, and still preserves edge-tts boundary
    events for future word-level or subtitle features.
    """
    if not sentences:
        raise RuntimeError("No sentences to synthesize.")

    rate = rate_percent_to_edge(rate_percent)
    workdir = create_workdir()
    audio_dir = workdir / "audio"
    audio_dir.mkdir(parents=True, exist_ok=True)
    segments: list[dict[str, Any]] = []

    try:
        write_document_text(workdir, document_text)
        write_manifest(
            workdir,
            title=title,
            source_name=source_name,
            voice=voice,
            locale=locale,
            rate=rate,
            sentences=sentences,
        )

        for sentence in sentences:
            if cancel_event and cancel_event.is_set():
                raise asyncio.CancelledError
            if progress_cb:
                progress_cb(sentence.index + 1, len(sentences), sentence.text[:90])
            audio_path = audio_dir / f"{sentence.index:06d}.mp3"
            try:
                events = await synthesize_sentence_to_file(
                    text=sentence.text,
                    voice=voice,
                    rate=rate,
                    audio_path=audio_path,
                )
            except ValueError as e:
                raise RuntimeError(
                    f"Sentence {sentence.index + 1} is empty or contains no synthesizable text. "
                    f"Text preview: {sentence.text[:100]!r}"
                ) from e
            segments.append(
                {
                    "sentence_index": sentence.index,
                    "audio": f"audio/{sentence.index:06d}.mp3",
                    "events": events,
                }
            )
            # Be polite to the unofficial endpoint on very long books.
            await asyncio.sleep(0.02)

        write_timings(workdir, segments)
        return pack_bundle(workdir, output_bundle)
    except Exception:
        raise
    finally:
        # The generated bundle is self-contained. If an exception occurs, remove temp partials.
        shutil.rmtree(workdir, ignore_errors=True)


def dump_debug_timing(timings: dict[str, Any], path: str | Path) -> None:
    Path(path).write_text(json.dumps(timings, indent=2, ensure_ascii=False), encoding="utf-8")
