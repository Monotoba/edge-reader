from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class SentenceSpan:
    """A sentence and its character range in the displayed document text."""

    index: int
    start: int
    end: int
    text: str


@dataclass(frozen=True)
class LoadedDocument:
    """Document text plus source metadata."""

    path: Path
    title: str
    text: str


@dataclass(frozen=True)
class VoiceInfo:
    """Reduced edge-tts voice information for the GUI."""

    short_name: str
    locale: str
    gender: str = ""
    friendly_name: str = ""

    @classmethod
    def from_edge_dict(cls, data: dict[str, Any]) -> "VoiceInfo":
        return cls(
            short_name=str(data.get("ShortName") or data.get("Name") or ""),
            locale=str(data.get("Locale") or ""),
            gender=str(data.get("Gender") or ""),
            friendly_name=str(data.get("FriendlyName") or data.get("LocalName") or ""),
        )

    @property
    def display_name(self) -> str:
        bits = [self.short_name]
        if self.gender:
            bits.append(self.gender)
        if self.friendly_name and self.friendly_name not in bits[0]:
            bits.append(self.friendly_name)
        return " — ".join(bits)
