from __future__ import annotations

import asyncio
import traceback
from pathlib import Path

from PySide6.QtCore import QThread, Signal

from .models import SentenceSpan, VoiceInfo
from .tts_edge import list_edge_voices, synthesize_bundle, synthesize_sentence_to_file, rate_percent_to_edge


class VoiceListWorker(QThread):
    voices_ready = Signal(list)
    failed = Signal(str)

    def run(self) -> None:  # pragma: no cover - GUI thread wrapper
        try:
            voices = asyncio.run(list_edge_voices())
            self.voices_ready.emit(voices)
        except Exception as exc:
            self.failed.emit(f"{exc}\n\n{traceback.format_exc()}")


class SynthesisWorker(QThread):
    progress = Signal(int, int, str)
    finished_ok = Signal(str)
    failed = Signal(str)

    def __init__(
        self,
        *,
        document_text: str,
        title: str,
        source_name: str,
        sentences: list[SentenceSpan],
        voice: str,
        locale: str,
        rate_percent: int,
        output_bundle: Path,
    ) -> None:
        super().__init__()
        self.document_text = document_text
        self.title = title
        self.source_name = source_name
        self.sentences = sentences
        self.voice = voice
        self.locale = locale
        self.rate_percent = rate_percent
        self.output_bundle = output_bundle
        self._cancel_requested = False

    def cancel(self) -> None:
        self._cancel_requested = True

    def run(self) -> None:  # pragma: no cover - GUI thread wrapper
        async def runner() -> Path:
            cancel_event = asyncio.Event()

            def progress_cb(done: int, total: int, preview: str) -> None:
                if self._cancel_requested:
                    cancel_event.set()
                self.progress.emit(done, total, preview)

            return await synthesize_bundle(
                document_text=self.document_text,
                title=self.title,
                source_name=self.source_name,
                sentences=self.sentences,
                voice=self.voice,
                locale=self.locale,
                rate_percent=self.rate_percent,
                output_bundle=self.output_bundle,
                progress_cb=progress_cb,
                cancel_event=cancel_event,
            )

        try:
            out = asyncio.run(runner())
            self.finished_ok.emit(str(out))
        except asyncio.CancelledError:
            self.failed.emit("Synthesis cancelled.")
        except Exception as exc:
            self.failed.emit(f"{exc}\n\n{traceback.format_exc()}")


class LivePlaybackWorker(QThread):
    finished_ok = Signal(str)
    failed = Signal(str)

    def __init__(
        self,
        *,
        sentence: SentenceSpan,
        voice: str,
        rate_percent: int,
        audio_dir: Path,
    ) -> None:
        super().__init__()
        self.sentence = sentence
        self.voice = voice
        self.rate_percent = rate_percent
        self.audio_dir = audio_dir

    def run(self) -> None:  # pragma: no cover - GUI thread wrapper
        async def runner() -> str:
            rate = rate_percent_to_edge(self.rate_percent)
            audio_path = self.audio_dir / f"{self.sentence.index:06d}.mp3"
            await synthesize_sentence_to_file(
                text=self.sentence.text,
                voice=self.voice,
                rate=rate,
                audio_path=audio_path,
            )
            return str(audio_path)

        try:
            audio_path = asyncio.run(runner())
            self.finished_ok.emit(audio_path)
        except Exception as exc:
            self.failed.emit(f"{exc}\n\n{traceback.format_exc()}")


FALLBACK_VOICES = [
    VoiceInfo("en-US-AriaNeural", "en-US", "Female", "Aria"),
    VoiceInfo("en-US-GuyNeural", "en-US", "Male", "Guy"),
    VoiceInfo("en-US-JennyNeural", "en-US", "Female", "Jenny"),
    VoiceInfo("en-GB-SoniaNeural", "en-GB", "Female", "Sonia"),
    VoiceInfo("en-GB-RyanNeural", "en-GB", "Male", "Ryan"),
    VoiceInfo("es-MX-DaliaNeural", "es-MX", "Female", "Dalia"),
    VoiceInfo("fr-FR-DeniseNeural", "fr-FR", "Female", "Denise"),
    VoiceInfo("de-DE-KatjaNeural", "de-DE", "Female", "Katja"),
]
